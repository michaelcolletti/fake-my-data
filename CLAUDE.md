# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The fake-my-data repository contains Python scripts for generating synthetic test data, specifically focused on:
- **Server migration data**: Complete server infrastructure records for cloud migration scenarios
- **Payroll data**: Employee records with department, salary, and employment details

## Common Commands

### Environment Setup
```bash
pip install -r requirements.txt
```

### Data Generation
```bash
# Generate server migration data (default: 100 rows)
python create-testdata.py

# Generate custom number of rows and specify output file
python create-testdata.py --num-rows 500 --output-file custom_servers.csv

# Generate payroll data
python generate-payroll-data.py
```

## Code Architecture

### Data Generation Pattern
Both scripts follow a similar pattern:
1. Define constants/configuration data at module level
2. Create generation functions that take parameters and faker instance
3. Use pandas DataFrame for structured data output
4. CLI interface with click for server migration script

### Key Components
- **create-testdata.py**: Well-structured server migration data generator with comprehensive CLI interface using click
- **generate-payroll-data.py**: Payroll data generator (contains syntax errors that need fixing)

### Data Models
- **Server Migration**: 15 fields including server specs, migration status, cloud targets, and business criticality
- **Payroll**: 8 fields covering employee demographics, department assignment, and compensation

## Important Notes

The `generate-payroll-data.py` script contains syntax errors and incomplete logic that prevent it from running successfully. When working on this file, focus on:
- Fixing the misplaced dictionary append logic around lines 40-51
- Completing the incomplete employee record generation
- Ensuring proper indentation and structure consistency
