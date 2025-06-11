import pytest
import pandas as pd
import tempfile
import os
from faker import Faker
from click.testing import CliRunner
import sys
import uuid

# Add parent directory to path to import the script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import using importlib to handle hyphenated filename
import importlib.util

spec = importlib.util.spec_from_file_location(
    "create_testdata",
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "create-testdata.py",
    ),
)
create_testdata_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create_testdata_module)

# Extract the functions and constants we need
generate_server_migration_data = create_testdata_module.generate_server_migration_data
cli_generate_server_data = create_testdata_module.cli_generate_server_data
SERVER_PREFIXES = create_testdata_module.SERVER_PREFIXES
OS_TYPES = create_testdata_module.OS_TYPES
CPU_CORE_OPTIONS = create_testdata_module.CPU_CORE_OPTIONS
RAM_GB_OPTIONS = create_testdata_module.RAM_GB_OPTIONS
STORAGE_GB_OPTIONS = create_testdata_module.STORAGE_GB_OPTIONS
DATACENTER_LOCATIONS = create_testdata_module.DATACENTER_LOCATIONS
APPLICATION_NAMES = create_testdata_module.APPLICATION_NAMES
ENVIRONMENTS = create_testdata_module.ENVIRONMENTS
MIGRATION_STATUSES = create_testdata_module.MIGRATION_STATUSES
TARGET_CLOUD_PROVIDERS = create_testdata_module.TARGET_CLOUD_PROVIDERS
MIGRATION_WAVES = create_testdata_module.MIGRATION_WAVES
BUSINESS_CRITICALITY_LEVELS = create_testdata_module.BUSINESS_CRITICALITY_LEVELS


class TestGenerateServerMigrationData:
    """Test suite for server migration data generation functions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.fake = Faker()
        self.fake.seed_instance(42)  # For reproducible tests

    def test_generate_server_migration_data_basic(self):
        """Test basic functionality of generate_server_migration_data."""
        num_rows = 10
        data = generate_server_migration_data(num_rows, self.fake)

        # Check that we get the right number of rows
        assert len(data["server_id"]) == num_rows

        # Check that all required fields are present
        expected_fields = [
            "server_id",
            "server_name",
            "os_type",
            "cpu_cores",
            "ram_gb",
            "storage_gb",
            "ip_address",
            "datacenter_location",
            "application_name",
            "environment",
            "migration_status",
            "target_cloud_provider",
            "migration_wave",
            "planned_migration_date",
            "business_criticality",
            "last_patch_date",
        ]

        for field in expected_fields:
            assert field in data
            assert len(data[field]) == num_rows

    def test_generate_server_migration_data_field_values(self):
        """Test that generated data contains valid field values."""
        num_rows = 50
        data = generate_server_migration_data(num_rows, self.fake)

        # Test that all server_ids are valid UUIDs
        for server_id in data["server_id"]:
            assert isinstance(uuid.UUID(str(server_id)), uuid.UUID)

        # Test that OS types are from the predefined list
        for os_type in data["os_type"]:
            assert os_type in OS_TYPES

        # Test CPU cores are from valid options
        for cpu_cores in data["cpu_cores"]:
            assert cpu_cores in CPU_CORE_OPTIONS

        # Test RAM values are from valid options
        for ram_gb in data["ram_gb"]:
            assert ram_gb in RAM_GB_OPTIONS

        # Test storage values are from valid options
        for storage_gb in data["storage_gb"]:
            assert storage_gb in STORAGE_GB_OPTIONS

        # Test datacenter locations are valid
        for location in data["datacenter_location"]:
            assert location in DATACENTER_LOCATIONS

        # Test application names are valid
        for app_name in data["application_name"]:
            assert app_name in APPLICATION_NAMES

        # Test environments are valid
        for env in data["environment"]:
            assert env in ENVIRONMENTS

        # Test migration statuses are valid
        for status in data["migration_status"]:
            assert status in MIGRATION_STATUSES

        # Test cloud providers are valid
        for provider in data["target_cloud_provider"]:
            assert provider in TARGET_CLOUD_PROVIDERS

        # Test migration waves are valid
        for wave in data["migration_wave"]:
            assert wave in MIGRATION_WAVES

        # Test business criticality levels are valid
        for criticality in data["business_criticality"]:
            assert criticality in BUSINESS_CRITICALITY_LEVELS

    def test_generate_server_migration_data_server_names(self):
        """Test that server names follow the expected pattern."""
        num_rows = 20
        data = generate_server_migration_data(num_rows, self.fake)

        for server_name in data["server_name"]:
            # Server names should contain a prefix from SERVER_PREFIXES
            prefix_found = any(prefix in server_name for prefix in SERVER_PREFIXES)
            assert (
                prefix_found
            ), f"Server name '{server_name}' doesn't contain a valid prefix"

            # Should contain an environment name (lowercase)
            env_found = any(env.lower() in server_name for env in ENVIRONMENTS)
            assert (
                env_found
            ), f"Server name '{server_name}' doesn't contain a valid environment"

    def test_generate_server_migration_data_ip_addresses(self):
        """Test that IP addresses are valid."""
        num_rows = 10
        data = generate_server_migration_data(num_rows, self.fake)

        for ip_address in data["ip_address"]:
            # Basic IP address format validation
            parts = ip_address.split(".")
            assert len(parts) == 4
            for part in parts:
                assert 0 <= int(part) <= 255

    def test_generate_server_migration_data_dates(self):
        """Test that dates are in correct format."""
        num_rows = 10
        data = generate_server_migration_data(num_rows, self.fake)

        # Test planned migration dates
        for date_str in data["planned_migration_date"]:
            # Should be in YYYY-MM-DD format
            assert len(date_str) == 10
            assert date_str[4] == "-" and date_str[7] == "-"
            year, month, day = date_str.split("-")
            assert 1900 <= int(year) <= 2100
            assert 1 <= int(month) <= 12
            assert 1 <= int(day) <= 31

        # Test last patch dates
        for date_str in data["last_patch_date"]:
            assert len(date_str) == 10
            assert date_str[4] == "-" and date_str[7] == "-"


class TestCLIInterface:
    """Test suite for the CLI interface."""

    def test_cli_default_parameters(self):
        """Test CLI with default parameters."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, "test_output.csv")
            result = runner.invoke(
                cli_generate_server_data, ["--output-file", output_file]
            )

            assert result.exit_code == 0
            assert os.path.exists(output_file)

            # Read the generated CSV and verify structure
            df = pd.read_csv(output_file)
            assert len(df) == 100  # Default number of rows
            assert len(df.columns) == 16  # Expected number of columns

    def test_cli_custom_parameters(self):
        """Test CLI with custom parameters."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, "custom_output.csv")
            result = runner.invoke(
                cli_generate_server_data,
                ["--num-rows", "50", "--output-file", output_file],
            )

            assert result.exit_code == 0
            assert os.path.exists(output_file)

            # Read the generated CSV and verify structure
            df = pd.read_csv(output_file)
            assert len(df) == 50  # Custom number of rows

            # Verify all expected columns are present
            expected_columns = [
                "server_id",
                "server_name",
                "os_type",
                "cpu_cores",
                "ram_gb",
                "storage_gb",
                "ip_address",
                "datacenter_location",
                "application_name",
                "environment",
                "migration_status",
                "target_cloud_provider",
                "migration_wave",
                "planned_migration_date",
                "business_criticality",
                "last_patch_date",
            ]

            for col in expected_columns:
                assert col in df.columns

    def test_cli_help(self):
        """Test CLI help output."""
        runner = CliRunner()
        result = runner.invoke(cli_generate_server_data, ["--help"])

        assert result.exit_code == 0
        assert "Generates synthetic server migration data" in result.output
        assert "--num-rows" in result.output
        assert "--output-file" in result.output


class TestDataIntegrity:
    """Test suite for data integrity and consistency."""

    def setup_method(self):
        """Set up test fixtures."""
        self.fake = Faker()

    def test_data_consistency_multiple_generations(self):
        """Test that multiple generations produce consistent data structures."""
        num_rows = 25

        # Generate data multiple times
        data1 = generate_server_migration_data(num_rows, self.fake)
        data2 = generate_server_migration_data(num_rows, self.fake)

        # Both should have the same structure
        assert data1.keys() == data2.keys()

        # Both should have the same number of rows for each field
        for key in data1.keys():
            assert len(data1[key]) == len(data2[key]) == num_rows

    def test_csv_output_integrity(self):
        """Test that CSV output maintains data integrity."""
        num_rows = 30
        fake_instance = Faker()
        data = generate_server_migration_data(num_rows, fake_instance)
        df = pd.DataFrame(data)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name
            df.to_csv(temp_file_path, index=False)

        try:
            # Read back the CSV
            df_read = pd.read_csv(temp_file_path)

            # Verify the data integrity
            assert len(df_read) == num_rows
            assert list(df_read.columns) == list(df.columns)

            # Verify no null values in critical fields
            critical_fields = ["server_id", "server_name", "os_type"]
            for field in critical_fields:
                assert df_read[field].isnull().sum() == 0

        finally:
            # Clean up
            os.unlink(temp_file_path)


if __name__ == "__main__":
    pytest.main([__file__])
