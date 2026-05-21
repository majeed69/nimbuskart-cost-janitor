import argparse
import json
from datetime import datetime

import boto3
from rich.console import Console
from rich.table import Table

from constants import (
    AWS_REGION,
    REPORT_FILE_JSON,
    REPORT_FILE_MD
)

console = Console()

ec2 = boto3.client(
    "ec2",
    region_name=AWS_REGION,
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)


def find_unattached_volumes():
    volumes = ec2.describe_volumes()["Volumes"]

    orphan_volumes = []

    for volume in volumes:
        if len(volume["Attachments"]) == 0:
            orphan_volumes.append({
                "volume_id": volume["VolumeId"],
                "size": volume["Size"],
                "state": volume["State"]
            })

    return orphan_volumes


def find_stopped_instances():
    reservations = ec2.describe_instances()["Reservations"]

    stopped_instances = []

    for reservation in reservations:
        for instance in reservation["Instances"]:

            state = instance["State"]["Name"]

            if state == "stopped":
                stopped_instances.append({
                    "instance_id": instance["InstanceId"],
                    "instance_type": instance["InstanceType"],
                    "state": state
                })

    return stopped_instances


def generate_report(orphan_volumes, stopped_instances):
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "orphan_ebs_volumes": orphan_volumes,
        "stopped_ec2_instances": stopped_instances
    }

    with open(REPORT_FILE_JSON, "w") as file:
        json.dump(report, file, indent=2)

    with open(REPORT_FILE_MD, "w") as file:
        file.write("# NimbusKart Cost Janitor Report\n\n")

        file.write("## Stopped EC2 Instances\n\n")

        if not stopped_instances:
            file.write("No stopped EC2 instances found.\n")
        else:
            for instance in stopped_instances:
                file.write(
                    f"- {instance['instance_id']} ({instance['instance_type']})\n"
                )

        file.write("\n## Orphan EBS Volumes\n\n")

        if not orphan_volumes:
            file.write("No orphan EBS volumes found.\n")
        else:
            for volume in orphan_volumes:
                file.write(
                    f"- {volume['volume_id']} ({volume['size']} GB)\n"
                )


def display_results(orphan_volumes, stopped_instances):
    ec2_table = Table(title="Stopped EC2 Instances")

    ec2_table.add_column("Instance ID")
    ec2_table.add_column("Type")
    ec2_table.add_column("State")

    for instance in stopped_instances:
        ec2_table.add_row(
            instance["instance_id"],
            instance["instance_type"],
            instance["state"]
        )

    console.print(ec2_table)

    ebs_table = Table(title="Orphan EBS Volumes")

    ebs_table.add_column("Volume ID")
    ebs_table.add_column("Size")
    ebs_table.add_column("State")

    for volume in orphan_volumes:
        ebs_table.add_row(
            volume["volume_id"],
            str(volume["size"]),
            volume["state"]
        )

    console.print(ebs_table)


def cleanup_resources(orphan_volumes, stopped_instances, dry_run):
    console.print("\n[bold yellow]Cleanup Phase[/bold yellow]\n")

    if dry_run:
        console.print("[bold cyan]DRY RUN MODE ENABLED[/bold cyan]\n")

    for volume in orphan_volumes:
        volume_id = volume["volume_id"]

        if dry_run:
            console.print(f"[yellow]Would delete EBS volume:[/yellow] {volume_id}")
        else:
            ec2.delete_volume(VolumeId=volume_id)
            console.print(f"[red]Deleted EBS volume:[/red] {volume_id}")

    for instance in stopped_instances:
        instance_id = instance["instance_id"]

        if dry_run:
            console.print(f"[yellow]Would terminate instance:[/yellow] {instance_id}")
        else:
            ec2.terminate_instances(InstanceIds=[instance_id])
            console.print(f"[red]Terminated instance:[/red] {instance_id}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview cleanup actions without deleting resources"
    )

    args = parser.parse_args()

    console.print("[bold cyan]Running NimbusKart Cost Janitor...[/bold cyan]\n")

    orphan_volumes = find_unattached_volumes()

    stopped_instances = find_stopped_instances()

    display_results(orphan_volumes, stopped_instances)

    generate_report(orphan_volumes, stopped_instances)

    cleanup_resources(
        orphan_volumes,
        stopped_instances,
        args.dry_run
    )

    console.print("\n[bold green]Report generated successfully.[/bold green]")


if __name__ == "__main__":
    main()
