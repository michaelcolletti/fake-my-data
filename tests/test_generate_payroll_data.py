import pytest
import pandas as pd
import tempfile
import os
import csv
from datetime import datetime, timedelta
import sys

# Add parent directory to path to import the script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import using importlib to handle hyphenated filename
import importlib.util

spec = importlib.util.spec_from_file_location(
    "generate_payroll_data",
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "generate-payroll-data.py",
    ),
)
generate_payroll_data_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_payroll_data_module)

# Extract the function we need
generate_fake_payroll = generate_payroll_data_module.generate_fake_payroll


class TestGeneratePayrollData:
    """Test suite for payroll data generation functions."""

    def test_generate_fake_payroll_file_creation(self):
        """Test that generate_fake_payroll creates a valid CSV file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            # Generate payroll data
            generate_fake_payroll(temp_file_path)

            # Verify file was created
            assert os.path.exists(temp_file_path)

            # Verify file is not empty
            assert os.path.getsize(temp_file_path) > 0

        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_payroll_data_structure(self):
        """Test that payroll data has the correct structure."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)

            # Read the CSV file
            df = pd.read_csv(temp_file_path)

            # Check number of rows (should be 200 employees)
            assert len(df) == 200

            # Check that all required columns are present
            expected_columns = [
                "EmployeeID",
                "FullName",
                "Department",
                "Position",
                "MonthlySalary",
                "HoursWorkedPerWeek",
                "DateOfJoining",
                "EmailAddress",
            ]

            for col in expected_columns:
                assert col in df.columns, f"Missing column: {col}"

            # Check that we have exactly the expected columns
            assert len(df.columns) == len(expected_columns)

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_employee_id_sequence(self):
        """Test that employee IDs are sequential from 1 to 200."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            # Check employee IDs are sequential
            expected_ids = list(range(1, 201))
            actual_ids = sorted(df["EmployeeID"].tolist())
            assert actual_ids == expected_ids

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_department_values(self):
        """Test that department values are from the expected list."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            expected_departments = ["HR", "Marketing", "Sales", "IT", "Finance"]
            actual_departments = df["Department"].unique().tolist()

            # All departments in the data should be from the expected list
            for dept in actual_departments:
                assert dept in expected_departments

            # We should have employees in each department (with high probability)
            # Given 200 employees and weighted distribution, this should be true
            assert (
                len(actual_departments) >= 4
            )  # Should have most departments represented

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_position_salary_consistency(self):
        """Test that position titles and salaries are consistent with department mapping."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            # Define expected salary ranges for each department/position combination
            expected_positions = {
                "HR": {"Manager": 4500, "HR Specialist": 4000},
                "Marketing": {"Manager": 4700, "Marketer": 4600},
                "Sales": {"Sales Rep": 5000, "Manager": 5200},
                "IT": {"Developer": 6000, "Manager": 6100},
                "Finance": {"Analyst": 5500, "Director": 5800},
            }

            # Check each employee's position and salary consistency
            for _, employee in df.iterrows():
                dept = employee["Department"]
                position = employee["Position"]
                salary = employee["MonthlySalary"]

                if dept in expected_positions:
                    if position in expected_positions[dept]:
                        expected_salary = expected_positions[dept][position]
                        assert (
                            salary == expected_salary
                        ), f"Salary mismatch for {dept} {position}: expected {expected_salary}, got {salary}"
                    else:
                        # Position might be "Staff" (default) with salary 3000
                        if position == "Staff":
                            assert salary == 3000
                        else:
                            # Unknown position, should still be a valid salary
                            assert isinstance(salary, (int, float))
                            assert salary > 0

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_salary_values(self):
        """Test that salary values are reasonable."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            # Check that all salaries are positive numbers
            assert (df["MonthlySalary"] > 0).all()

            # Check that salaries are within reasonable ranges (3000-7000 based on our mapping)
            assert (df["MonthlySalary"] >= 3000).all()
            assert (df["MonthlySalary"] <= 7000).all()

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_hours_worked_range(self):
        """Test that hours worked per week are within expected range."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            # Hours should be between 35 and 45 (inclusive)
            assert (df["HoursWorkedPerWeek"] >= 35).all()
            assert (df["HoursWorkedPerWeek"] <= 45).all()

            # All values should be integers
            assert df["HoursWorkedPerWeek"].dtype in ["int64", "int32"]

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_date_of_joining_format(self):
        """Test that DateOfJoining is in correct format and within expected range."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            current_date = datetime.now()
            five_years_ago = current_date - timedelta(days=5 * 365)

            for date_str in df["DateOfJoining"]:
                # Check date format (YYYY-MM-DD)
                assert len(date_str) == 10
                assert date_str[4] == "-" and date_str[7] == "-"

                # Parse the date
                join_date = datetime.strptime(date_str, "%Y-%m-%d")

                # Date should be between 5 years ago and today
                assert five_years_ago <= join_date <= current_date

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_email_address_format(self):
        """Test that email addresses have valid format."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            for email in df["EmailAddress"]:
                # Basic email format validation
                assert "@" in email
                assert "." in email.split("@")[1]  # Domain should have a dot
                assert len(email.split("@")) == 2  # Should have exactly one @

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_full_name_format(self):
        """Test that full names have reasonable format."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            for full_name in df["FullName"]:
                # Name should have at least first and last name
                name_parts = full_name.strip().split()
                assert (
                    len(name_parts) >= 2
                ), f"Name '{full_name}' should have at least 2 parts"

                # Each part should be non-empty and contain only letters
                for part in name_parts:
                    assert len(part) > 0
                    assert (
                        part.isalpha()
                    ), f"Name part '{part}' should contain only letters"

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_no_missing_values(self):
        """Test that there are no missing values in any column."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            # Check that no column has missing values
            for column in df.columns:
                missing_count = df[column].isnull().sum()
                assert (
                    missing_count == 0
                ), f"Column '{column}' has {missing_count} missing values"

                # Also check for empty strings
                if df[column].dtype == "object":  # String columns
                    empty_count = (df[column] == "").sum()
                    assert (
                        empty_count == 0
                    ), f"Column '{column}' has {empty_count} empty strings"

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_manager_distribution(self):
        """Test that manager distribution is approximately 10% as intended."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)
            df = pd.read_csv(temp_file_path)

            # Count managers and directors
            management_positions = ["Manager", "Director"]
            manager_count = df[df["Position"].isin(management_positions)].shape[0]

            # With 200 employees and 10% probability, we expect around 20 managers
            # Allow for some variance due to randomness (10-40 range should be reasonable)
            assert (
                5 <= manager_count <= 50
            ), f"Manager count {manager_count} seems outside reasonable range"

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)


class TestCSVIntegrity:
    """Test suite for CSV file integrity and format."""

    def test_csv_readable_by_pandas(self):
        """Test that generated CSV can be properly read by pandas."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)

            # This should not raise any exceptions
            df = pd.read_csv(temp_file_path)
            assert len(df) > 0

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_csv_readable_by_standard_csv_module(self):
        """Test that generated CSV can be read by Python's csv module."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            generate_fake_payroll(temp_file_path)

            # Read with standard csv module
            with open(temp_file_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)

                assert len(rows) == 200

                # Check that first row has all expected fields
                expected_fields = [
                    "EmployeeID",
                    "FullName",
                    "Department",
                    "Position",
                    "MonthlySalary",
                    "HoursWorkedPerWeek",
                    "DateOfJoining",
                    "EmailAddress",
                ]

                for field in expected_fields:
                    assert field in rows[0], f"Missing field: {field}"

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)


if __name__ == "__main__":
    pytest.main([__file__])
