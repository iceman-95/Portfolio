# Employee Management System

A comprehensive command-line based Employee Management System built with Python and MySQL. This system provides a complete solution for managing employee information, including adding, updating, searching, and analyzing employee data.

## Features

### 1. Employee Management
- ➕ Add new employees with auto-generated IDs, emails, and phone numbers
- 📋 View complete employee list organized by departments
- 🔍 Search employees by ID, name, email, or department
- 📝 Update employee information
- 🗑️ Remove employees from the system
- 🚀 Promote employees with position and salary updates

### 2. Salary Analysis
- 📊 Comprehensive salary analysis across departments
- 💰 Position-wise salary distribution
- 📈 Salary range analysis
- 📉 Department-wise salary statistics
- 💵 Overall salary metrics

### 3. Database Management
- 💾 Export database state to SQL file
- 🔄 Automatic database initialization
- 📑 Stored procedures for common operations
- 🔐 User privilege management

## Prerequisites

- Python 3.6 or higher
- MySQL Server
- Required Python packages:
  - mysql-connector-python
  - tabulate

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd employee-management-system
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Set up the MySQL database:
   - Create a MySQL database named `employee_management`
   - Update the database configuration in `db_config.py`

## Configuration

Create a `db_config.py` file with the following content:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'employee_management'
}
```

## Usage

1. Run the program:
```bash
python employee_management.py
```

2. Use the main menu to navigate through different features:
   - 1: Add New Employee
   - 2: View Employee List
   - 3: Search Employee
   - 4: Update Employee Details
   - 5: Remove Employee
   - 6: Promote Employee
   - 7: Export Database State
   - 8: Analyze Salaries
   - 9: Exit

## Employee ID System

The system uses a department-based ID system:
- Finance: 1xx
- IT: 2xx
- Marketing: 3xx
- Sales: 4xx
- HR: 5xx

## Database Structure

### Employees Table
```sql
CREATE TABLE employees (
    id VARCHAR(3) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    department VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    hire_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Features in Detail

### Adding Employees
- Automatic ID generation based on department
- Email generation using first initial and last name
- Phone number generation based on employee ID
- Input validation for all fields

### Viewing Employees
- Department-wise organization
- Formatted tables using tabulate
- Summary statistics for each department
- Total employee count

### Salary Analysis
- Overall salary statistics
- Department-wise analysis
- Position-wise analysis
- Salary range distribution
- Minimum, maximum, and average salaries

### Database Export
- Complete database state export
- Includes table structure
- Includes all employee data
- Includes stored procedures
- Includes user privileges

## Error Handling

The system includes comprehensive error handling for:
- Database connection issues
- Invalid input data
- Duplicate entries
- SQL query errors
- File operations

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the maintainers. 