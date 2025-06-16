#!/usr/bin/env python3

import csv
from faker import Faker
from datetime import datetime, timedelta
import random


def generate_fake_payroll(filename):
    fake = Faker()

    employees = []
    for e_id in range(1, 201):  # Generates EmployeeIDs from 1 to 200
        dept = random.choices(
            ["HR", "Marketing", "Sales", "IT", "Finance"],
            weights=[0.15, 0.2, 0.15, 0.3, 0.25],
            k=1,
        )[0]
        is_manager = random.random() < 0.1  # 10% chance for Manager

        dept_salary_map = {
            "HR": {"Manager": 4500, "HR Specialist": 4000},
            "Marketing": {"Manager": 4700, "Marketer": 4600},
            "Sales": {"Sales Rep": 5000, "Manager": 5200},
            "IT": {"Developer": 6000, "Manager": 6100},
            "Finance": {"Analyst": 5500, "Director": 5800},
        }

        # Determine position title and actual_base_salary
        dept_roles_salaries = dept_salary_map[dept]
        
        if is_manager:
            if dept == "Finance" and "Director" in dept_roles_salaries:
                position_name = "Director"
                actual_base_salary = dept_roles_salaries["Director"]
            elif "Manager" in dept_roles_salaries:
                position_name = "Manager"
                actual_base_salary = dept_roles_salaries["Manager"]
            else:
                # Fallback for manager role
                position_name = "Manager"
                actual_base_salary = 5000
        else:
            # Get non-manager options
            non_manager_options = {
                k: v
                for k, v in dept_roles_salaries.items()
                if k not in ["Manager", "Director"]
            }
            if non_manager_options:
                position_name = random.choice(list(non_manager_options.keys()))
                actual_base_salary = non_manager_options[position_name]
            else:
                # Fallback for non-manager role
                position_name = "Staff"
                actual_base_salary = 3500

        # Generate hours worked per week (35-45 hours)
        hours_per_week = random.randint(35, 45)

        # Generate DateOfJoining between one to five years ago
        end_date = datetime.now()
        total_days_in_5_years = 5 * 365
        random_days_offset = random.randint(1, total_days_in_5_years)
        date_of_joining = end_date - timedelta(days=random_days_offset)

        email_address = fake.email()

        employees.append(
            {
                "EmployeeID": e_id,
                "FullName": f"{fake.first_name()} {fake.last_name()}",
                "Department": dept,
                "Position": position_name,
                "MonthlySalary": actual_base_salary,
                "HoursWorkedPerWeek": hours_per_week,
                "DateOfJoining": date_of_joining.strftime("%Y-%m-%d"),
                "EmailAddress": email_address,
            }
        )

    # Write to CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "EmployeeID",
            "FullName",
            "Department",
            "Position",
            "MonthlySalary",
            "HoursWorkedPerWeek",
            "DateOfJoining",
            "EmailAddress",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees:
            writer.writerow(emp)


if __name__ == "__main__":
    generate_fake_payroll("fake_payroll.csv")
    print("Generated 200 rows of payroll data into fake_payroll.csv")
