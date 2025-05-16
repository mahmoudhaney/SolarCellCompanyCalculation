# Solar Cell Company Calculation App

This Frappe app provides tools for solar energy companies to evaluate and track the return on investment (ROI) for clients switching to solar. The core feature is the **Solar Calculation** DocType which calculates energy consumption patterns and estimates monthly low/high tariff costs.

## 🚀 Features

- Calculates average **KW** and **KWH** from customer data.
- Determines **low** and **high tariff** consumption based on time-of-day.
- Populates a detailed **Monthly Tariffs** child table.
- Automatically assigns a unique serial number per customer.
- Built-in validation for consumption data and dates.
- Role-based access restrictions (Sales vs. Accounts).


## 🔧 Setup Instructions

## Installing App

1. Install the App on the bench from the Repository:

```
bench get-app --branch main test_mahmoud git@github.com:mahmoudhaney/SolarCellCompanyCalculation.git
```

2. Install the App to the site:

```
bench --site [site-name] install-app test_mahmoud
```

3. Migrate the changes:

```
bench --site [site-name] migrate
```

4. Build the App:

```
bench --site [site-name] build
```

## 📦 Usage Guide
1. Create a Solar Calculation Record
- Go to Solar Calculation from the Desk.
- Fill in:
  - Customer
  - Start Date
  - End Date
  - Add multiple rows to the Consumption Data table:
    - timestamp (DateTime)
    - kw (non-negative float)
    - kwh (non-negative float)

2. Run Calculation
- Click the Calculate button to:
  - Compute average `kw` and `kwh`
  - Analyze time-of-day usage
  - Estimate low and high tariff values per month

## ⚙️ Logic Overview
- Low Tariff Period: 11 PM to 6 AM
- High Tariff Period: 6 AM to 11 PM
- Tariff Rates (Example):
  - Low tariff: 0.1 * `kwh`
  - High tariff: 0.3 * `kwh`
- The Monthly Tariffs Table is generated dynamically.

## 🧪 Data Validation
- Start Date must precede End Date
- Each Consumption Data row must have:
- Valid timestamp
- Non-negative kw and kwh
- Validation enforced client-side and server-side

## 🔐 Access Control
| Role | Access Level |
| -------- | ------- |
| Sales User | Full access |
| Accounts User | Read-only |


If a user has both roles, Sales permissions override.

## 📁 File Structure
```text
test_mahmoud/
├── solar_cell_company_calculation/
│   └── doctype/
│       ├── solar_calculation/
│       │   ├── solar_calculation.py       # Main DocType backend logic
│       │   ├── solar_calculation.js       # Frontend form script
│       │   ├── solar_calculation.json     # DocType schema definition
│       ├── consumption_record/
│       │   ├── consumption_record.py      # Child table for KW/KWH data
│       │   ├── consumption_record.json    # DocType definition
│       ├── monthly_tariff/
│       │   ├── monthly_tariff.py          # Child table for monthly tariff results
│       │   ├── monthly_tariff.json        # DocType definition
├── README.md  
