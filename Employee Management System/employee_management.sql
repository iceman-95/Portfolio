-- Employee Management System Database
-- Last updated: 2025-06-13 22:36:31

-- Drop database if exists and create new one
DROP DATABASE IF EXISTS employee_management;
CREATE DATABASE employee_management;
USE employee_management;

-- Create employees table
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

-- Insert employee data
INSERT INTO employees (id, first_name, last_name, email, phone, department, position, salary, hire_date) VALUES
('101', 'Levan', 'Dvalishvili', 'l.dvalishvili@company.com', '555-555-101', 'Finance', 'Finance Manager', 90000.00, '2019-06-15'),
('102', 'Nino', 'Abashidze', 'n.abashidze@company.com', '555-555-102', 'Finance', 'Accountant', 45000.00, '2020-01-15'),
('103', 'Giorgi', 'Beridze', 'g.beridze@company.com', '555-555-103', 'Finance', 'Financial Analyst', 52000.00, '2020-02-20'),
('104', 'Mariam', 'Chkheidze', 'm.chkheidze@company.com', '555-555-104', 'Finance', 'Financial Analyst', 51000.00, '2020-03-10'),
('501', 'Zura', 'Razmadze', 'z.razmadze@company.com', '555-555-501', 'HR', 'HR Manager', 80000.00, '2019-11-15'),
('502', 'Ana', 'Qipshidze', 'a.qipshidze@company.com', '555-555-502', 'HR', 'HR Specialist', 46000.00, '2021-01-10'),
('503', 'Nana', 'Svanidze', 'n.svanidze@company.com', '555-555-503', 'HR', 'Recruiter', 44000.00, '2021-02-20'),
('504', 'Beka', 'Tsereteli', 'b.tsereteli@company.com', '555-555-504', 'HR', 'HR Specialist', 45000.00, '2021-03-15'),
('201', 'Beka', 'Hakobidze', 'b.hakobidze@company.com', '555-555-201', 'IT', 'IT Manager', 95000.00, '2019-08-10'),
('202', 'Ana', 'Ebralidze', 'a.ebralidze@company.com', '555-555-202', 'IT', 'Software Developer', 65000.00, '2020-04-05'),
('203', 'Zura', 'Furmanidze', 'z.furmanidze@company.com', '555-555-203', 'IT', 'System Administrator', 62000.00, '2020-05-12'),
('204', 'Nana', 'Gogoladze', 'n.gogoladze@company.com', '555-555-204', 'IT', 'Software Developer', 63000.00, '2020-06-20'),
('205', 'Lika', 'Ivanishvili', 'l.ivanishvili@company.com', '555-555-205', 'IT', 'QA Engineer', 58000.00, '2020-07-15'),
('206', 'Solomoni', 'Tutberidze', 's.tutberidze@company.com', '555-555-206', 'IT', 'Software Developer', 55000.00, '2023-05-20'),
('301', 'Salome', 'Kalandadze', 's.kalandadze@company.com', '555-555-301', 'Marketing', 'Marketing Manager', 82000.00, '2019-09-15'),
('302', 'Giorgi', 'Japaridze', 'g.japaridze@company.com', '555-555-302', 'Marketing', 'Marketing Specialist', 48000.00, '2020-08-01'),
('303', 'Luka', 'Lomidze', 'l.lomidze@company.com', '555-555-303', 'Marketing', 'Content Writer', 45000.00, '2020-09-20'),
('304', 'Mari', 'Sulikashvili', 'm.sulikashvili@company.com', '555-555-304', 'Marketing', 'Content Writer', 45000.00, '2024-08-24'),
('402', 'Nino', 'Mamulashvili', 'n.mamulashvili@company.com', '555-555-402', 'Marketing', 'Marketing Specialist', 50000.00, '2020-10-05'),
('401', 'Mariam', 'Ochiauri', 'm.ochiauri@company.com', '555-555-401', 'Sales', 'Sales Manager', 88000.00, '2019-10-20'),
('403', 'Giorgi', 'Nakashidze', 'g.nakashidze@company.com', '555-555-403', 'Sales', 'Senior Sales Representative', 55000.00, '2020-11-10'),
('404', 'Levan', 'Pirtskhalava', 'l.pirtskhalava@company.com', '555-555-404', 'Sales', 'Sales Representative', 41000.00, '2020-12-15'),
('405', 'Tsotne', 'Meskhi', 't.meskhi@company.com', '555-555-405', 'Sales', 'Sales Representative', 42000.00, '2021-03-17');

-- Create indexes for better performance
CREATE INDEX idx_department ON employees(department);
CREATE INDEX idx_position ON employees(position);
CREATE INDEX idx_hire_date ON employees(hire_date);

-- Create a view for employee summary
CREATE VIEW employee_summary AS
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary
FROM employees
GROUP BY department;

-- Create stored procedures
DELIMITER //
CREATE PROCEDURE promote_employee(
    IN emp_id VARCHAR(3),
    IN new_position VARCHAR(50),
    IN new_salary DECIMAL(10, 2)
)
BEGIN
    UPDATE employees 
    SET position = new_position,
        salary = new_salary
    WHERE id = emp_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE search_employees(
    IN search_term VARCHAR(100)
)
BEGIN
    SELECT *
    FROM employees
    WHERE first_name LIKE CONCAT('%', search_term, '%')
    OR last_name LIKE CONCAT('%', search_term, '%')
    OR email LIKE CONCAT('%', search_term, '%')
    OR department LIKE CONCAT('%', search_term, '%')
    OR position LIKE CONCAT('%', search_term, '%');
END //
DELIMITER ;

-- Set up user privileges
CREATE USER IF NOT EXISTS 'employee_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON employee_management.* TO 'employee_user'@'localhost';
FLUSH PRIVILEGES;
