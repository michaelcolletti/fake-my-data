#!/usr/bin/env  python

import random
from faker import Faker
from datetime import datetime
import pandas as pd
import click

# Constants for Server Migration Data
SERVER_PREFIXES = ["web", "app", "db", "cache", "rpt", "aux"]
OS_TYPES = [
    "Ubuntu 22.04 LTS",
    "RHEL 8",
    "Windows Server 2019",
    "CentOS 7",
    "Debian 11",
]
CPU_CORE_OPTIONS = [2, 4, 8, 16, 32, 64]
RAM_GB_OPTIONS = [8, 16, 32, 64, 128, 256]
STORAGE_GB_OPTIONS = [250, 500, 1000, 2000, 4000, 8000]
DATACENTER_LOCATIONS = [
    "us-east-1",
    "us-west-2",
    "eu-central-1",
    "ap-southeast-1",
    "eu-west-1",
]
APPLICATION_NAMES = [
    "E-commerce Backend",
    "CRM Suite",
    "Data Warehouse",
    "Internal Portal",
    "Payment API",
    "Reporting Service",
    "User Authentication",
]
ENVIRONMENTS = ["Production", "Staging", "Development", "Test", "QA"]
MIGRATION_STATUSES = [
    "Pending Assessment",
    "Planning",
    "Ready for Migration",
    "Migrating",
    "Completed",
    "On Hold",
    "Failed",
]
TARGET_CLOUD_PROVIDERS = ["AWS", "Azure", "GCP", "OCI"]
MIGRATION_WAVES = [1, 2, 3, 4, 5]
BUSINESS_CRITICALITY_LEVELS = ["High", "Medium", "Low"]


def generate_server_migration_data(num_rows, fake_instance):
    """
    Generates synthetic server migration data.
    """
    data = {
        "server_id": [fake_instance.uuid4() for _ in range(num_rows)],
        "server_name": [
            f"{random.choice(SERVER_PREFIXES)}-{random.choice(ENVIRONMENTS).lower()}-{fake_instance.word().lower()}-{random.randint(1, 99):02d}"
            for _ in range(num_rows)
        ],
        "os_type": [random.choice(OS_TYPES) for _ in range(num_rows)],
        "cpu_cores": [random.choice(CPU_CORE_OPTIONS) for _ in range(num_rows)],
        "ram_gb": [random.choice(RAM_GB_OPTIONS) for _ in range(num_rows)],
        "storage_gb": [random.choice(STORAGE_GB_OPTIONS) for _ in range(num_rows)],
        "ip_address": [fake_instance.ipv4() for _ in range(num_rows)],
        "datacenter_location": [
            random.choice(DATACENTER_LOCATIONS) for _ in range(num_rows)
        ],
        "application_name": [random.choice(APPLICATION_NAMES) for _ in range(num_rows)],
        "environment": [random.choice(ENVIRONMENTS) for _ in range(num_rows)],
        "migration_status": [
            random.choice(MIGRATION_STATUSES) for _ in range(num_rows)
        ],
        "target_cloud_provider": [
            random.choice(TARGET_CLOUD_PROVIDERS) for _ in range(num_rows)
        ],
        "migration_wave": [random.choice(MIGRATION_WAVES) for _ in range(num_rows)],
        "planned_migration_date": [
            fake_instance.date_between(start_date="-30d", end_date="+180d").strftime(
                "%Y-%m-%d"
            )
            for _ in range(num_rows)
        ],
        "business_criticality": [
            random.choice(BUSINESS_CRITICALITY_LEVELS) for _ in range(num_rows)
        ],
        "last_patch_date": [
            fake_instance.date_between(start_date="-365d", end_date="today").strftime(
                "%Y-%m-%d"
            )
            for _ in range(num_rows)
        ],
    }
    return data


# Initialize Faker for realistic text data
fake = Faker()


# If you want to use the server migration data generation, you can call it like this:
# num_server_rows = 100  # Or any number of rows you need
# server_data = generate_server_migration_data(num_server_rows, fake)
# server_df = pd.DataFrame(server_data)
# server_df.to_csv('server_migration_data.csv', index=False)
# print(f"Generated {num_server_rows} rows of server migration data into server_migration_data.csv")
@click.command()
@click.option(
    "--num-rows",
    default=100,
    help="Number of server migration data rows to generate.",
    type=int,
    show_default=True,
)
@click.option(
    "--output-file",
    default="server_migration_data.csv",
    help="Name of the output CSV file.",
    type=str,
    show_default=True,
)
def cli_generate_server_data(num_rows, output_file):
    """Generates synthetic server migration data and saves it to a CSV file."""
    fake_instance = Faker()
    server_data = generate_server_migration_data(num_rows, fake_instance)
    server_df = pd.DataFrame(server_data)
    server_df.to_csv(output_file, index=False)
    click.echo(f"Generated {num_rows} rows of server migration data into {output_file}")


if __name__ == "__main__":
    cli_generate_server_data()
