# 🎲 Fake My Data - Synthetic Data Generation

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-pytest-orange.svg)

*Professional synthetic data generation tools for server migration and payroll scenarios*

</div>

---

## 📖 Overview

This repository provides robust Python tools for generating realistic synthetic datasets, specifically designed for:

- **🖥️ Server Migration Planning**: Comprehensive infrastructure data for cloud migration scenarios
- **👥 Payroll Management**: Employee records with department assignments and compensation details

Perfect for testing, demonstrations, training, and development environments where realistic data is needed without privacy concerns.

## ✨ Features

### 🖥️ Server Migration Data Generator
- **15 comprehensive fields** including server specifications, migration status, and business criticality
- **Configurable row counts** with CLI support
- **Cloud provider mapping** (AWS, Azure, GCP, OCI)
- **Migration wave planning** with status tracking
- **Realistic server naming** conventions

### 👥 Payroll Data Generator
- **200 employee records** with full demographic details
- **5 department types** with weighted distribution
- **Role-based salary assignments** including management hierarchy
- **Realistic employment dates** spanning 1-5 years
- **Valid email generation** and working hours

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd fake-my-data

# Install dependencies
make install
```

### Generate Sample Data

```bash
# Generate example datasets
make examples

# Or generate specific data types
make run-server-data    # Server migration data (100 rows)
make run-payroll-data   # Payroll data (200 employees)
```

### Run Tests

```bash
# Run all tests
make test

# Run with coverage
make test-coverage
```

## 📁 Project Structure

```
fake-my-data/
├── 📄 create-testdata.py          # Server migration data generator
├── 👥 generate-payroll-data.py    # Payroll data generator  
├── 📋 requirements.txt            # Python dependencies
├── 🏗️ Makefile                   # Build and run commands
├── 📚 tests/                      # Comprehensive test suite
│   ├── test_create_testdata.py    # Server data tests
│   └── test_generate_payroll_data.py # Payroll data tests
├── 📊 output/                     # Generated data files (created on first run)
├── 📖 README.md                   # This file
└── 🔧 CLAUDE.md                   # AI assistant guidance
```

## 🛠️ Usage

### Server Migration Data

#### Command Line Interface

```bash
# Default generation (100 rows)
python create-testdata.py

# Custom row count and output file
python create-testdata.py --num-rows 500 --output-file custom_servers.csv

# Get help
python create-testdata.py --help
```

#### Makefile Shortcuts

```bash
make server-small     # 50 rows
make server-medium    # 200 rows  
make server-large     # 500 rows
make server-xlarge    # 1000 rows
```

#### Generated Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `server_id` | Unique UUID identifier | `550e8400-e29b-41d4-a716-446655440000` |
| `server_name` | Structured naming convention | `web-prod-api-01`, `db-staging-mysql-05` |
| `os_type` | Operating system | Ubuntu 22.04 LTS, RHEL 8, Windows Server 2019 |
| `cpu_cores` | CPU core count | 2, 4, 8, 16, 32, 64 |
| `ram_gb` | Memory in GB | 8, 16, 32, 64, 128, 256 |
| `storage_gb` | Storage capacity | 250, 500, 1000, 2000, 4000, 8000 |
| `datacenter_location` | Current location | us-east-1, eu-central-1, ap-southeast-1 |
| `migration_status` | Current migration phase | Pending Assessment, Planning, Completed |
| `target_cloud_provider` | Destination platform | AWS, Azure, GCP, OCI |
| `business_criticality` | Impact level | High, Medium, Low |

### Payroll Data

#### Command Line Usage

```bash
# Generate payroll data (200 employees)
python generate-payroll-data.py
```

#### Generated Fields

| Field | Description | Details |
|-------|-------------|---------|
| `EmployeeID` | Sequential identifier | 1-200 |
| `FullName` | Realistic names | Generated using Faker |
| `Department` | Business unit | HR, Marketing, Sales, IT, Finance |
| `Position` | Job title | Manager, Developer, Analyst, Specialist, etc. |
| `MonthlySalary` | Compensation | Department and role-based (3000-6100) |
| `HoursWorkedPerWeek` | Work schedule | 35-45 hours |
| `DateOfJoining` | Employment start | Random dates within last 5 years |
| `EmailAddress` | Contact information | Valid email format |

## 🧪 Testing

The project includes comprehensive test suites ensuring data quality and consistency.

### Run Tests

```bash
# All tests with pytest
python -m pytest tests/ -v

# Quick test via make
make test

# Specific test suites
python -m pytest tests/test_create_testdata.py -v     # Server data tests
python -m pytest tests/test_generate_payroll_data.py -v  # Payroll data tests

# With coverage reporting
make test-coverage
```

### Test Coverage

**24 comprehensive tests** with 100% pass rate covering:

- ✅ **Data Structure**: Correct fields and formats (8 tests)
- ✅ **Value Ranges**: Realistic and expected data ranges (6 tests)
- ✅ **Business Logic**: Department/salary consistency (4 tests)
- ✅ **File Integrity**: Valid CSV output (3 tests)
- ✅ **CLI Interface**: Command-line argument handling (2 tests)
- ✅ **Edge Cases**: Error handling and validation (1 test)

All tests validate both server migration and payroll data generation with comprehensive business rule checking.

## 📊 Sample Data Output

### Server Migration Data Sample
```csv
server_id,server_name,os_type,cpu_cores,ram_gb,storage_gb,migration_status
550e8400-e29b-41d4-a716-446655440000,web-prod-api-01,Ubuntu 22.04 LTS,8,32,500,Planning
6ba7b810-9dad-11d1-80b4-00c04fd430c8,db-staging-mysql-05,RHEL 8,16,64,2000,Ready for Migration
```

### Payroll Data Sample
```csv
EmployeeID,FullName,Department,Position,MonthlySalary,HoursWorkedPerWeek,DateOfJoining,EmailAddress
1,Amanda Mueller,HR,HR Specialist,4000,45,2021-04-09,amanda.mueller@example.com
2,Mary Evans,Finance,Analyst,5500,42,2024-05-19,mary.evans@example.net
```

## 🔧 Development

### Available Make Commands

```bash
make help           # Show all available commands
make install        # Install dependencies
make examples       # Generate example datasets
make test           # Run test suite
make test-coverage  # Run tests with coverage
make lint           # Code linting (requires flake8)
make format         # Code formatting (requires black)
make validate       # Run tests + linting
make clean          # Clean generated files
make info           # Show project information
make quickstart     # Install + examples + test
```

### Adding New Features

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-data-type`
3. **Add your generator function** to existing files or create new ones
4. **Write comprehensive tests** in the `tests/` directory
5. **Update documentation** and Makefile targets
6. **Submit a pull request**

## 🏗️ Architecture

### Data Generation Pattern

Both generators follow a consistent architecture:

1. **Constants Definition**: Predefined value lists for realistic data
2. **Generation Functions**: Core logic with configurable parameters
3. **Faker Integration**: Realistic names, emails, dates, and addresses
4. **DataFrame Output**: Structured data using pandas
5. **CLI Interface**: User-friendly command-line tools

### Key Design Principles

- **🎯 Realistic Data**: Values mirror real-world scenarios
- **🔧 Configurable**: Flexible parameters for different use cases  
- **📊 Consistent**: Repeatable structure across generations
- **✅ Tested**: Comprehensive validation and quality assurance
- **🚀 Fast**: Efficient generation for large datasets

## 🛡️ Data Privacy & GDPR Compliance

All generated data is **completely synthetic** and fully GDPR compliant:

### 🔒 Privacy Protection
- ❌ **No real personal information** - All names, emails, and IDs are faker-generated
- ❌ **No actual server details** - Infrastructure data is entirely synthetic
- ❌ **No sensitive business data** - Safe for sharing and testing
- ✅ **Safe for all environments** - Development, staging, and production testing
- ✅ **No data subject rights apply** - Not derived from real individuals
- ✅ **No anonymization needed** - Never contained personal data

### 🌍 Cloud Provider Compliance
The server migration data includes cloud provider mappings to support GDPR-compliant infrastructure planning:

- **AWS, Azure, GCP, OCI** targeting with data residency considerations
- **EU region mapping** (eu-central-1, eu-west-1) for European data sovereignty
- **Migration wave planning** to ensure compliance during cloud transitions
- **Business criticality flags** to identify systems handling personal data

### ✅ Legal Benefits
- **Article 4(1) GDPR doesn't apply** - No processing of personal data
- **Safe for international transfer** - No cross-border data restrictions
- **No consent required** - Synthetic data, not personal information
- **No breach notification** - No real data at risk

## 📦 Dependencies

- **Python 3.8+**
- **faker**: Realistic fake data generation
- **pandas**: Data manipulation and CSV output
- **click**: Command-line interface framework
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting

## 📈 Roadmap

Future enhancements planned:

- 🔄 **Additional data types** (customer records, financial transactions)
- 🌐 **JSON/XML output formats**
- 📊 **Data relationship modeling**
- 🎛️ **Advanced configuration options**
- 📱 **Web interface** for data generation
- 🔌 **API endpoints** for programmatic access

## 🤝 Contributing

Contributions are welcome! Please see our contribution guidelines:

1. **Fork** the repository
2. **Create** a feature branch
3. **Add tests** for new functionality
4. **Ensure** all tests pass (`make test`)
5. **Submit** a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions, issues, or feature requests:

- 🐛 **Bug Reports**: Create an issue with detailed description
- 💡 **Feature Requests**: Propose new functionality
- 📚 **Documentation**: Help improve guides and examples
- 💬 **Discussion**: Join community conversations

---

<div align="center">

**[⭐ Star this repository](https://github.com/michaelcolletti/fake-my-data) if you find it helpful!**

*Built with ❤️ for the data generation community*

</div>