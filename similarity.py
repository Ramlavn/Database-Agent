# similarity.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download NLTK data if not already present
nltk.download('punkt')

# Initialize the stemmer
stemmer = PorterStemmer()

def preprocess(text):
    """
    Preprocesses the input text by lowercasing, removing punctuation, tokenizing, and stemming.
    
    :param text: The input text string.
    :return: The preprocessed text string.
    """
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    tokens = word_tokenize(text)
    # Stem
    tokens = [stemmer.stem(word) for word in tokens]
    # Join back to string
    return ' '.join(tokens)

# Predefined natural language queries and their corresponding SQL queries
PREDEFINED_QUERIES = {
    "Show all the data": "SELECT * from employees",
    "List all lab tests.": "SELECT name FROM LabTests;",
    "List all labs.": "SELECT name, price FROM LabTests;",  # Added synonym
    "List all lab tests in Hematology department.": "SELECT name, price FROM LabTests WHERE department_id = (SELECT id FROM Departments WHERE name = 'Hematology');",
    "Show the names and normal ranges of lab tests in Biochemistry.": "SELECT name, normal_range FROM LabTests WHERE department_id = (SELECT id FROM Departments WHERE name = 'Biochemistry');",
    "What lab tests are available in Chicago?": "SELECT LabTests.name FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id WHERE Departments.location = 'Chicago';",
    "Find the average price of lab tests in Immunology.": "SELECT AVG(price) FROM LabTests WHERE department_id = (SELECT id FROM Departments WHERE name = 'Immunology');",
    "List all lab tests with their department names.": "SELECT LabTests.name, Departments.name FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id;",
    "Show the total number of lab tests in each department.": "SELECT Departments.name, COUNT(LabTests.id) FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id GROUP BY Departments.name;",
    "Find lab tests with prices greater than the average price.": "SELECT name, price FROM LabTests WHERE price > (SELECT AVG(price) FROM LabTests);",
    "List departments and their locations.": "SELECT name, location FROM Departments;",
    "Show lab tests in the Pathology department.": "SELECT name FROM LabTests WHERE department_id = (SELECT id FROM Departments WHERE name = 'Pathology');",
    "Show all lab test details.": "SELECT * FROM LabTests;",
    "List all departments.": "SELECT * FROM Departments;",
    "Show the number of lab tests in Hematology.": "SELECT COUNT(*) FROM LabTests WHERE department_id = (SELECT id FROM Departments WHERE name = 'Hematology');",
    "Find lab tests in New York.": "SELECT name FROM LabTests WHERE department_id = (SELECT id FROM Departments WHERE location = 'New York');",
    "List lab tests with prices above 70.": "SELECT name, price FROM LabTests WHERE price > 70;",
    "Show average price per department.": "SELECT Departments.name, AVG(LabTests.price) FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id GROUP BY Departments.name;",
    "List lab tests with normal ranges for C-Reactive Protein (CRP).": "SELECT name, normal_range FROM LabTests WHERE name = 'C-Reactive Protein (CRP)';",
    "List all lab test names.": "SELECT name FROM LabTests;",
    "Find the most expensive lab test.": "SELECT name, price FROM LabTests ORDER BY price DESC LIMIT 1;",
    "Show lab tests costing less than 50.": "SELECT name, price FROM LabTests WHERE price < 50;",
    "List lab tests and their prices.": "SELECT name, price FROM LabTests;",
    "Show the departments with the highest number of lab tests.": "SELECT Departments.name, COUNT(LabTests.id) as test_count FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id GROUP BY Departments.name ORDER BY test_count DESC;",
    "Find lab tests in the second floor.": "SELECT LabTests.name FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id WHERE Departments.location = 'Second Floor';",
    "List employees working in Immunology department.": "SELECT Employees.name, Employees.role FROM Employees WHERE department_id = (SELECT id FROM Departments WHERE name = 'Immunology');",
    "Show all employees": "SELECT name FROM employees;",
    "Show all employee roles.": "SELECT DISTINCT role FROM Employees;",
    "Find employees with the role of Lab Manager.": "SELECT name FROM Employees WHERE role = 'Lab Manager';",
    "List employees and their departments.": "SELECT Employees.name, Departments.name FROM Employees JOIN Departments ON Employees.department_id = Departments.id;",
    "Show the total salary expenditure per department.": "SELECT Departments.name, SUM(Employees.salary) FROM Employees JOIN Departments ON Employees.department_id = Departments.id GROUP BY Departments.name;",
    "Find the youngest employee in each department.": "SELECT Departments.name, Employees.name, Employees.age FROM Employees JOIN Departments ON Employees.department_id = Departments.id WHERE Employees.age = (SELECT MIN(age) FROM Employees WHERE department_id = Departments.id);",
    "List all roles in the lab.": "SELECT DISTINCT role FROM Employees;",
    "Show employees in the Third Floor department.": "SELECT Employees.name, Employees.role FROM Employees JOIN Departments ON Employees.department_id = Departments.id WHERE Departments.location = 'Third Floor';",
    "Find employees with salaries above 70000.": "SELECT name, salary FROM Employees WHERE salary > 70000;",
    "List all lab tests along with their prices and normal ranges.": "SELECT name, price, normal_range FROM LabTests;",
    "Show the most common lab test location.": "SELECT Departments.location, COUNT(LabTests.id) as test_count FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id GROUP BY Departments.location ORDER BY test_count DESC LIMIT 1;",
    "Find lab tests that are priced between 30 and 60.": "SELECT name, price FROM LabTests WHERE price BETWEEN 30 AND 60;",
    "List all employees with their roles and departments.": "SELECT Employees.name, Employees.role, Departments.name FROM Employees JOIN Departments ON Employees.department_id = Departments.id;",
    "List lab tests costing exactly 50.": "SELECT name FROM LabTests WHERE price = 50;",
    "Show lab tests priced between 40 and 60.": "SELECT name, price FROM LabTests WHERE price BETWEEN 40 AND 60;",
    "Find the cheapest lab test in each department.": "SELECT Departments.name, LabTests.name, LabTests.price FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id WHERE LabTests.price = (SELECT MIN(price) FROM LabTests WHERE department_id = Departments.id);",
    "List lab tests with prices not equal to 30.": "SELECT name, price FROM LabTests WHERE price != 30;",
    "Show lab tests that cost more than the average price.": "SELECT name, price FROM LabTests WHERE price > (SELECT AVG(price) FROM LabTests);",
    "Find employees with salaries above the average salary.": "SELECT name, salary FROM Employees WHERE salary > (SELECT AVG(salary) FROM Employees);",
    "List lab tests with prices in the top 10% of all tests.": "SELECT name, price FROM LabTests WHERE price > (SELECT percentile_cont(0.9) WITHIN GROUP (ORDER BY price) FROM LabTests);",
    "Show employees earning less than 50000.": "SELECT name, salary FROM Employees WHERE salary < 50000;",
    "Find lab tests that are the most expensive in their department.": "SELECT Departments.name, LabTests.name, LabTests.price FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id WHERE LabTests.price = (SELECT MAX(price) FROM LabTests WHERE department_id = Departments.id);",
    "List departments where the total price of lab tests exceeds 300.": "SELECT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id GROUP BY Departments.name HAVING SUM(LabTests.price) > 300;",
    
    # Combining Multiple Filters
    "Find lab tests in Hematology priced above 50.": "SELECT name, price FROM LabTests WHERE department_id = (SELECT id FROM Departments WHERE name = 'Hematology') AND price > 50;",
    "List employees in Biochemistry earning over 70000.": "SELECT name, salary FROM Employees WHERE department_id = (SELECT id FROM Departments WHERE name = 'Biochemistry') AND salary > 70000;",
    "Show lab tests in Immunology priced below 40.": "SELECT name, price FROM LabTests WHERE department_id = (SELECT id FROM Departments WHERE name = 'Immunology') AND price < 40;",
    "Find employees in Pathology older than 35.": "SELECT name, age FROM Employees WHERE department_id = (SELECT id FROM Departments WHERE name = 'Pathology') AND age > 35;",
    "List lab tests in Microbiology with normal ranges containing 'ng/mL'.": "SELECT name, normal_range FROM LabTests WHERE department_id = (SELECT id FROM Departments WHERE name = 'Microbiology') AND normal_range LIKE '%ng/mL%';",
    "Show employees in departments located in Chicago earning above 60000.": "SELECT Employees.name, Employees.salary FROM Employees JOIN Departments ON Employees.department_id = Departments.id WHERE Departments.location = 'Chicago' AND Employees.salary > 60000;",
    "Find lab tests administered by employees younger than 30.": "SELECT LabTests.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id WHERE Employees.age < 30;",
    "List employees who are Lab Managers and earn more than 75000.": "SELECT name, salary FROM Employees WHERE role = 'Lab Manager' AND salary > 75000;",
    "Show lab tests in departments on the Second Floor costing less than 60.": "SELECT name, price FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id WHERE Departments.location = 'Second Floor' AND LabTests.price < 60;",
    "Find employees in Immunology earning between 50000 and 80000.": "SELECT name, salary FROM Employees WHERE department_id = (SELECT id FROM Departments WHERE name = 'Immunology') AND salary BETWEEN 50000 AND 80000;",
    
    # Advanced Aggregations
    "Calculate the median price of lab tests in each department.": "SELECT Departments.name, AVG(LabTests.price) as median_price FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id GROUP BY Departments.name;",
    "Show the standard deviation of employee salaries in each department.": "SELECT Departments.name, STDDEV(Employees.salary) FROM Employees JOIN Departments ON Employees.department_id = Departments.id GROUP BY Departments.name;",
    "Find the variance in lab test prices across all departments.": "SELECT VARIANCE(price) FROM LabTests;",
    "List departments with the highest average employee salary.": "SELECT Departments.name FROM Departments JOIN Employees ON Departments.id = Employees.department_id GROUP BY Departments.name ORDER BY AVG(Employees.salary) DESC LIMIT 1;",
    "Show the total and average price of lab tests in each department.": "SELECT Departments.name, SUM(LabTests.price) as total_price, AVG(LabTests.price) as average_price FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id GROUP BY Departments.name;",
    
    # Time-based Queries (Assuming 'join_date' is added)
    "Find employees who joined after 2015.": "SELECT name, join_date FROM Employees WHERE join_date > '2015-12-31';",
    "List employees who joined in the year 2020.": "SELECT name FROM Employees WHERE strftime('%Y', join_date) = '2020';",
    "Show the number of employees who joined each year.": "SELECT strftime('%Y', join_date) as year, COUNT(*) FROM Employees GROUP BY year;",
    "Find employees who joined between 2018 and 2020.": "SELECT name FROM Employees WHERE join_date BETWEEN '2018-01-01' AND '2020-12-31';",
    "List employees who joined in the last five years.": "SELECT name FROM Employees WHERE join_date >= date('now', '-5 years');",
    
    # Null and Not Null Queries
    "Find lab tests without a specified normal range.": "SELECT name FROM LabTests WHERE normal_range IS NULL OR normal_range = '';",
    "List employees who do not have a specified salary.": "SELECT name FROM Employees WHERE salary IS NULL;",
    "Show lab tests that do not belong to any department.": "SELECT name FROM LabTests WHERE department_id IS NULL;",
    "Find employees with no assigned department.": "SELECT name FROM Employees WHERE department_id IS NULL;",
    "List lab tests where the price is not set.": "SELECT name FROM LabTests WHERE price IS NULL;",
    
    # Pattern Matching
    "List lab tests with names containing 'Blood'.": "SELECT name FROM LabTests WHERE name LIKE '%Blood%';",
    "Show employees whose names start with 'J'.": "SELECT name FROM Employees WHERE name LIKE 'J%';",
    "Find lab tests that end with 'Panel'.": "SELECT name FROM LabTests WHERE name LIKE '%Panel';",
    "List departments with names containing 'ology'.": "SELECT name FROM Departments WHERE name LIKE '%ology%';",
    "Show employees whose names contain 'Smith'.": "SELECT name FROM Employees WHERE name LIKE '%Smith%';",
    
    # Combining Multiple Joins
    "List lab tests along with employee names and department locations.": "SELECT LabTests.name, Employees.name, Departments.location FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id JOIN Departments ON LabTests.department_id = Departments.id;",
    "Show employees, their roles, and the lab tests they administer.": "SELECT Employees.name, Employees.role, LabTests.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id;",
    "Find lab tests along with the names and salaries of employees in each department.": "SELECT LabTests.name, Employees.name, Employees.salary FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id;",
    "List departments, their employees, and lab tests offered.": "SELECT Departments.name, Employees.name, LabTests.name FROM Departments JOIN Employees ON Departments.id = Employees.department_id JOIN LabTests ON Departments.id = LabTests.department_id;",
    "Show employees working in departments that offer expensive lab tests.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE LabTests.price > 70;",
    
    # Miscellaneous Complex Queries
    "Find the total number of lab tests per employee.": "SELECT Employees.name, COUNT(LabTests.id) FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id GROUP BY Employees.name;",
    "List employees along with the average price of lab tests in their department.": "SELECT Employees.name, AVG(LabTests.price) FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id GROUP BY Employees.name;",
    "Show the highest and lowest priced lab tests in each department.": "SELECT Departments.name, MAX(LabTests.price) as max_price, MIN(LabTests.price) as min_price FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id GROUP BY Departments.name;",
    "Find employees who manage the most expensive lab tests.": "SELECT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id GROUP BY Employees.name ORDER BY MAX(LabTests.price) DESC LIMIT 1;",
    "List departments with an average employee salary above 60000.": "SELECT Departments.name FROM Departments JOIN Employees ON Departments.id = Employees.department_id GROUP BY Departments.name HAVING AVG(Employees.salary) > 60000;",
    
    # Specific Attribute Listings
    "List all lab test names and their prices.": "SELECT name, price FROM LabTests;",
    "Show all employee names and their salaries.": "SELECT name, salary FROM Employees;",
    "Find all departments and their locations.": "SELECT name, location FROM Departments;",
    "List all lab test names along with their normal ranges.": "SELECT name, normal_range FROM LabTests;",
    "Show employee names, roles, and ages.": "SELECT name, role, age FROM Employees;",
    
    # Combining Conditions and Aggregations
    "Find departments where the average lab test price is above 60 and have more than five tests.": "SELECT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id GROUP BY Departments.name HAVING AVG(LabTests.price) > 60 AND COUNT(LabTests.id) > 5;",
    "List employees in departments offering lab tests priced between 30 and 50.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE LabTests.price BETWEEN 30 AND 50;",
    "Show the average salary of employees in departments located in Chicago.": "SELECT Departments.name, AVG(Employees.salary) FROM Employees JOIN Departments ON Employees.department_id = Departments.id WHERE Departments.location = 'Chicago' GROUP BY Departments.name;",
    "Find lab tests administered by employees earning above 70000.": "SELECT LabTests.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id WHERE Employees.salary > 70000;",
    "List departments with employees older than 40 and lab tests priced above 80.": "SELECT DISTINCT Departments.name FROM Departments JOIN Employees ON Departments.id = Employees.department_id JOIN LabTests ON Departments.id = LabTests.department_id WHERE Employees.age > 40 AND LabTests.price > 80;",
    
    # Additional Creative Queries
    "Show the most common lab test price.": "SELECT price, COUNT(*) as frequency FROM LabTests GROUP BY price ORDER BY frequency DESC LIMIT 1;",
    "Find employees who have the same salary as the most expensive lab test.": "SELECT name FROM Employees WHERE salary = (SELECT MAX(price) FROM LabTests);",
    "List lab tests offered by departments with no employees.": "SELECT LabTests.name FROM LabTests LEFT JOIN Employees ON LabTests.department_id = Employees.department_id WHERE Employees.id IS NULL;",
    "Show departments with the least number of employees.": "SELECT Departments.name FROM Departments JOIN Employees ON Departments.id = Employees.department_id GROUP BY Departments.name ORDER BY COUNT(Employees.id) ASC LIMIT 1;",
    "Find lab tests that are more expensive than the average salary of employees in their department.": "SELECT LabTests.name FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id JOIN Employees ON LabTests.department_id = Employees.department_id WHERE LabTests.price > (SELECT AVG(salary) FROM Employees WHERE department_id = Departments.id);",
    "List employees who manage departments offering lab tests below 50.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE Employees.role = 'Lab Manager' AND LabTests.price < 50;",
    "Show the average age of employees per department.": "SELECT Departments.name, AVG(Employees.age) FROM Employees JOIN Departments ON Employees.department_id = Departments.id GROUP BY Departments.name;",
    "Find departments where employees earn above the overall average salary.": "SELECT Departments.name FROM Departments JOIN Employees ON Departments.id = Employees.department_id GROUP BY Departments.name HAVING AVG(Employees.salary) > (SELECT AVG(salary) FROM Employees);",
    "List lab tests along with the number of employees in their department.": "SELECT LabTests.name, COUNT(Employees.id) FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id JOIN Employees ON Departments.id = Employees.department_id GROUP BY LabTests.name;",
    "Show departments offering the same number of lab tests as their number of employees.": "SELECT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id JOIN Employees ON Departments.id = Employees.department_id GROUP BY Departments.name HAVING COUNT(LabTests.id) = COUNT(Employees.id);",
    
    # Additional 50 Queries for Diversity
    "List all lab tests with a price greater than 90.": "SELECT name, price FROM LabTests WHERE price > 90;",
    "Show employees who earn exactly 50000.": "SELECT name FROM Employees WHERE salary = 50000;",
    "Find lab tests in departments not located in Chicago.": "SELECT name FROM LabTests WHERE department_id NOT IN (SELECT id FROM Departments WHERE location = 'Chicago');",
    "List employees working in departments on the First Floor.": "SELECT Employees.name FROM Employees JOIN Departments ON Employees.department_id = Departments.id WHERE Departments.location = 'First Floor';",
    "Show the most common salary among employees.": "SELECT salary FROM Employees GROUP BY salary ORDER BY COUNT(*) DESC LIMIT 1;",
    "Find lab tests with prices less than the average lab test price.": "SELECT name, price FROM LabTests WHERE price < (SELECT AVG(price) FROM LabTests);",
    "List departments that offer at least one lab test costing above 80.": "SELECT DISTINCT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id WHERE LabTests.price > 80;",
    "Show employees who are older than the average employee age.": "SELECT name, age FROM Employees WHERE age > (SELECT AVG(age) FROM Employees);",
    "Find lab tests administered by employees older than 40.": "SELECT LabTests.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id WHERE Employees.age > 40;",
    "List departments with the highest average lab test price.": "SELECT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id GROUP BY Departments.name HAVING AVG(LabTests.price) = (SELECT MAX(avg_price) FROM (SELECT AVG(price) as avg_price FROM LabTests GROUP BY department_id));",
    
    "Show employees in Immunology earning above 60000.": "SELECT name, salary FROM Employees WHERE department_id = (SELECT id FROM Departments WHERE name = 'Immunology') AND salary > 60000;",
    "Find lab tests with prices not between 30 and 70.": "SELECT name, price FROM LabTests WHERE price NOT BETWEEN 30 AND 70;",
    "List employees who work in departments offering more than five lab tests.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id GROUP BY Employees.name HAVING COUNT(LabTests.id) > 5;",
    "Show the total number of lab tests in departments on the Fourth Floor.": "SELECT COUNT(LabTests.id) FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id WHERE Departments.location = 'Fourth Floor';",
    "Find employees whose names end with 'n'.": "SELECT name FROM Employees WHERE name LIKE '%n';",
    "List lab tests that have a normal range containing 'mg/L'.": "SELECT name FROM LabTests WHERE normal_range LIKE '%mg/L%';",
    "Show departments with an average lab test price below 50.": "SELECT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id GROUP BY Departments.name HAVING AVG(LabTests.price) < 50;",
    "Find employees with the highest salary in Immunology.": "SELECT name, salary FROM Employees WHERE department_id = (SELECT id FROM Departments WHERE name = 'Immunology') AND salary = (SELECT MAX(salary) FROM Employees WHERE department_id = (SELECT id FROM Departments WHERE name = 'Immunology'));",
    "List lab tests offered by departments with employees earning above 70000.": "SELECT DISTINCT LabTests.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id WHERE Employees.salary > 70000;",
    "Show employees in departments offering lab tests priced between 50 and 100.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE LabTests.price BETWEEN 50 AND 100;",
    
    "List departments that offer lab tests with prices exactly 25.": "SELECT DISTINCT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id WHERE LabTests.price = 25;",
    "Show lab tests in departments with no employees earning below 50000.": "SELECT LabTests.name FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id WHERE Departments.id NOT IN (SELECT department_id FROM Employees WHERE salary < 50000);",
    "Find employees who manage departments offering the most expensive lab tests.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE LabTests.price = (SELECT MAX(price) FROM LabTests);",
    "List lab tests in departments where the average employee age is above 30.": "SELECT LabTests.name FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id JOIN Employees ON Departments.id = Employees.department_id GROUP BY LabTests.name HAVING AVG(Employees.age) > 30;",
    "Show employees who work in departments offering lab tests with normal ranges starting with '0-'.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE LabTests.normal_range LIKE '0-%';",
    
    "Find the total salary paid to Lab Managers.": "SELECT SUM(salary) FROM Employees WHERE role = 'Lab Manager';",
    "List lab tests with prices not equal to 75.": "SELECT name, price FROM LabTests WHERE price != 75;",
    "Show employees in departments on the Second Floor earning between 60000 and 80000.": "SELECT name, salary FROM Employees JOIN Departments ON Employees.department_id = Departments.id WHERE Departments.location = 'Second Floor' AND Employees.salary BETWEEN 60000 AND 80000;",
    "Find lab tests offered by departments with more than two employees.": "SELECT LabTests.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id GROUP BY LabTests.name HAVING COUNT(Employees.id) > 2;",
    "List employees who are Senior Analysts and earn above 90000.": "SELECT name, salary FROM Employees WHERE role = 'Senior Analyst' AND salary > 90000;",
    
    "Show lab tests in departments located in San Francisco.": "SELECT LabTests.name FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id WHERE Departments.location = 'San Francisco';",
    "Find employees who have the same salary as the 'Lipid Panel' test.": "SELECT name FROM Employees WHERE salary = (SELECT price FROM LabTests WHERE name = 'Lipid Panel');",
    "List departments with lab tests priced above their department's average.": "SELECT DISTINCT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id WHERE LabTests.price > (SELECT AVG(price) FROM LabTests WHERE department_id = Departments.id);",
    "Show employees who are older than the oldest employee in Pathology.": "SELECT name, age FROM Employees WHERE age > (SELECT MAX(age) FROM Employees WHERE department_id = (SELECT id FROM Departments WHERE name = 'Pathology'));",
    "Find lab tests that are administered by employees earning exactly 50000.": "SELECT LabTests.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id WHERE Employees.salary = 50000;",
    
    "List all lab tests along with the names of employees who administer them.": "SELECT LabTests.name, Employees.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id;",
    "Show departments offering lab tests with normal ranges greater than '50 mg/dL'.": "SELECT DISTINCT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id WHERE LabTests.normal_range > '50 mg/dL';",
    "Find employees who work in departments offering both 'Complete Blood Count (CBC)' and 'Urinalysis'.": "SELECT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE LabTests.name IN ('Complete Blood Count (CBC)', 'Urinalysis') GROUP BY Employees.name HAVING COUNT(DISTINCT LabTests.name) = 2;",
    "List lab tests administered by employees younger than 35 and earning above 60000.": "SELECT LabTests.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id WHERE Employees.age < 35 AND Employees.salary > 60000;",
    "Show departments that offer lab tests with prices between 25 and 50 and have employees older than 30.": "SELECT DISTINCT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id JOIN Employees ON Departments.id = Employees.department_id WHERE LabTests.price BETWEEN 25 AND 50 AND Employees.age > 30;",
    
    "Find lab tests that are administered by both Lab Managers and Lab Technicians.": "SELECT DISTINCT LabTests.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id WHERE Employees.role IN ('Lab Manager', 'Lab Technician') GROUP BY LabTests.name HAVING COUNT(DISTINCT Employees.role) = 2;",
    "List employees who manage the most and least expensive lab tests.": "SELECT name FROM Employees WHERE salary IN ((SELECT MAX(price) FROM LabTests), (SELECT MIN(price) FROM LabTests));",
    "Show departments with the highest total salary expenditure.": "SELECT Departments.name FROM Departments JOIN Employees ON Departments.id = Employees.department_id GROUP BY Departments.name ORDER BY SUM(Employees.salary) DESC LIMIT 1;",
    "Find lab tests that have the same price as any employee's salary.": "SELECT name FROM LabTests WHERE price IN (SELECT salary FROM Employees);",
    "List employees in departments offering lab tests priced above 90.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE LabTests.price > 90;",
    
    # Advanced Pattern Matching
    "Show lab tests with names containing both 'Blood' and 'Count'.": "SELECT name FROM LabTests WHERE name LIKE '%Blood%' AND name LIKE '%Count%';",
    "Find employees whose names contain exactly two words.": "SELECT name FROM Employees WHERE LENGTH(name) - LENGTH(REPLACE(name, ' ', '')) = 1;",
    "List departments with names ending in 'ology'.": "SELECT name FROM Departments WHERE name LIKE '%ology';",
    "Show employees with roles that start with 'Senior'.": "SELECT name FROM Employees WHERE role LIKE 'Senior%';",
    "Find lab tests with names not containing 'Panel'.": "SELECT name FROM LabTests WHERE name NOT LIKE '%Panel%';",
    
    # Miscellaneous Complex Queries
    "List employees along with the number of lab tests they administer.": "SELECT Employees.name, COUNT(LabTests.id) as test_count FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id GROUP BY Employees.name;",
    "Show departments along with the average employee age.": "SELECT Departments.name, AVG(Employees.age) FROM Departments JOIN Employees ON Departments.id = Employees.department_id GROUP BY Departments.name;",
    "Find lab tests with the longest normal range descriptions.": "SELECT name FROM LabTests ORDER BY LENGTH(normal_range) DESC LIMIT 1;",
    "List employees who work in the same department as 'Alice Johnson'.": "SELECT name FROM Employees WHERE department_id = (SELECT department_id FROM Employees WHERE name = 'Alice Johnson') AND name != 'Alice Johnson';",
    "Show departments that offer both 'Complete Blood Count (CBC)' and 'Urinalysis'.": "SELECT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id WHERE LabTests.name IN ('Complete Blood Count (CBC)', 'Urinalysis') GROUP BY Departments.name HAVING COUNT(DISTINCT LabTests.name) = 2;",
    
    # Historical and Trend-Based Queries (Assuming 'join_date' exists)
    "Find employees who have been with the lab for more than 10 years.": "SELECT name FROM Employees WHERE join_date <= date('now', '-10 years');",
    "List lab tests introduced in the last five years.": "SELECT name FROM LabTests WHERE introduced_date >= date('now', '-5 years');",
    "Show the yearly increase in the number of lab tests.": "SELECT strftime('%Y', introduced_date) as year, COUNT(*) FROM LabTests GROUP BY year ORDER BY year ASC;",
    "Find employees who received a salary increase in 2021.": "SELECT name FROM Employees WHERE last_raise_year = 2021;",
    "List departments that have added new lab tests in the current year.": "SELECT DISTINCT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id WHERE LabTests.added_year = strftime('%Y','now');",
    
    # Null and Not Null Queries
    "Find employees who do not have a specified salary.": "SELECT name FROM Employees WHERE salary IS NULL;",
    "List lab tests without a specified normal range.": "SELECT name FROM LabTests WHERE normal_range IS NULL OR normal_range = '';",
    "Show departments that do not have any lab tests assigned.": "SELECT Departments.name FROM Departments LEFT JOIN LabTests ON Departments.id = LabTests.department_id WHERE LabTests.id IS NULL;",
    "Find employees without an assigned department.": "SELECT name FROM Employees WHERE department_id IS NULL;",
    "List lab tests where the price is not set.": "SELECT name FROM LabTests WHERE price IS NULL;",
    
    # Role-Based Queries
    "List all Lab Managers along with their departments.": "SELECT Employees.name, Departments.name FROM Employees JOIN Departments ON Employees.department_id = Departments.id WHERE Employees.role = 'Lab Manager';",
    "Show Lab Technicians earning above 50000.": "SELECT name, salary FROM Employees WHERE role = 'Lab Technician' AND salary > 50000;",
    "Find Quality Control staff in Biochemistry.": "SELECT Employees.name FROM Employees WHERE role = 'Quality Control' AND department_id = (SELECT id FROM Departments WHERE name = 'Biochemistry');",
    "List Senior Analysts with salaries above 90000.": "SELECT name, salary FROM Employees WHERE role = 'Senior Analyst' AND salary > 90000;",
    "Show employees in the 'Quality Control' role and located on the Second Floor.": "SELECT Employees.name FROM Employees JOIN Departments ON Employees.department_id = Departments.id WHERE Employees.role = 'Quality Control' AND Departments.location = 'Second Floor';",
    
    # Combining Aggregations and Conditions
    "Find departments where the average lab test price is above 60 and have more than three tests.": "SELECT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id GROUP BY Departments.name HAVING AVG(LabTests.price) > 60 AND COUNT(LabTests.id) > 3;",
    "List employees who are older than the average employee age and earn above the average salary.": "SELECT name FROM Employees WHERE age > (SELECT AVG(age) FROM Employees) AND salary > (SELECT AVG(salary) FROM Employees);",
    "Show departments with the highest total salary expenditure.": "SELECT Departments.name FROM Departments JOIN Employees ON Departments.id = Employees.department_id GROUP BY Departments.name ORDER BY SUM(Employees.salary) DESC LIMIT 1;",
    "Find lab tests that cost more than the average salary of employees in their department.": "SELECT LabTests.name FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id JOIN Employees ON LabTests.department_id = Employees.department_id WHERE LabTests.price > (SELECT AVG(salary) FROM Employees WHERE department_id = Departments.id);",
    "List employees who manage departments offering lab tests priced below 50.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE Employees.role = 'Lab Manager' AND LabTests.price < 50;",
    
    # Temporal Queries (Assuming 'join_date' and 'introduced_date' exist)
    "Find employees who joined after January 1, 2018.": "SELECT name FROM Employees WHERE join_date > '2018-01-01';",
    "List lab tests introduced before 2020.": "SELECT name FROM LabTests WHERE introduced_date < '2020-01-01';",
    "Show employees who joined in the year 2020.": "SELECT name FROM Employees WHERE strftime('%Y', join_date) = '2020';",
    "Find lab tests introduced in the last two years.": "SELECT name FROM LabTests WHERE introduced_date >= date('now', '-2 years');",
    "List employees who have been with the lab for over five years.": "SELECT name FROM Employees WHERE join_date <= date('now', '-5 years');",
    
    # Complex Conditional Queries
    "Find lab tests that are either priced above 80 or belong to Immunology.": "SELECT name, price FROM LabTests WHERE price > 80 OR department_id = (SELECT id FROM Departments WHERE name = 'Immunology');",
    "List employees who are Lab Technicians in departments offering tests priced below 50.": "SELECT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE Employees.role = 'Lab Technician' AND LabTests.price < 50;",
    "Show lab tests in departments located on the Fourth Floor and priced above 60.": "SELECT name, price FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id WHERE Departments.location = 'Fourth Floor' AND LabTests.price > 60;",
    "Find employees who are either Lab Managers or earn above 80000.": "SELECT name, role, salary FROM Employees WHERE role = 'Lab Manager' OR salary > 80000;",
    "List departments offering lab tests with normal ranges containing 'mg/L' and have at least two employees.": "SELECT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id JOIN Employees ON Departments.id = Employees.department_id WHERE LabTests.normal_range LIKE '%mg/L%' GROUP BY Departments.name HAVING COUNT(Employees.id) >= 2;",
    
    # Logical Operators and Advanced Conditions
    "Find lab tests that start with 'Blood' and are priced above 50.": "SELECT name, price FROM LabTests WHERE name LIKE 'Blood%' AND price > 50;",
    "List employees who are not Lab Managers and earn less than 60000.": "SELECT name FROM Employees WHERE role != 'Lab Manager' AND salary < 60000;",
    "Show lab tests that are either in Biochemistry or Immunology and priced below 80.": "SELECT name, price FROM LabTests WHERE (department_id = (SELECT id FROM Departments WHERE name = 'Biochemistry') OR department_id = (SELECT id FROM Departments WHERE name = 'Immunology')) AND price < 80;",
    "Find employees who are either older than 40 or earn above 90000.": "SELECT name FROM Employees WHERE age > 40 OR salary > 90000;",
    "List lab tests that are not administered by Lab Managers.": "SELECT LabTests.name FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id WHERE Employees.role != 'Lab Manager';",
    
    # Combining Multiple Joins and Conditions
    "Show lab tests along with the names and roles of employees who administer them and are located on the Third Floor.": "SELECT LabTests.name, Employees.name, Employees.role FROM LabTests JOIN Employees ON LabTests.department_id = Employees.department_id JOIN Departments ON LabTests.department_id = Departments.id WHERE Departments.location = 'Third Floor';",
    "Find employees who manage departments offering lab tests priced between 30 and 60.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE Employees.role = 'Lab Manager' AND LabTests.price BETWEEN 30 AND 60;",
    "List departments that offer lab tests containing 'Glucose' and have employees older than 30.": "SELECT DISTINCT Departments.name FROM Departments JOIN LabTests ON Departments.id = LabTests.department_id JOIN Employees ON Departments.id = Employees.department_id WHERE LabTests.name LIKE '%Glucose%' AND Employees.age > 30;",
    "Show lab tests in departments where the average employee salary is above 65000 and have more than three tests.": "SELECT LabTests.name FROM LabTests JOIN Departments ON LabTests.department_id = Departments.id JOIN Employees ON Departments.id = Employees.department_id GROUP BY LabTests.name HAVING AVG(Employees.salary) > 65000 AND COUNT(LabTests.id) > 3;",
    "Find employees who work in departments offering lab tests priced above the overall average and earn above 70000.": "SELECT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE LabTests.price > (SELECT AVG(price) FROM LabTests) AND Employees.salary > 70000;",
    
    # More Creative and User-Centric Queries
    "List lab tests that are essential for blood analysis.": "SELECT name, price FROM LabTests WHERE name LIKE '%Blood%';",
    "Show employees responsible for high-cost lab tests.": "SELECT DISTINCT Employees.name FROM Employees JOIN LabTests ON Employees.department_id = LabTests.department_id WHERE LabTests.price > 70;",
    "Find departments that do not offer any lab tests.": "SELECT name FROM Departments WHERE id NOT IN (SELECT department_id FROM LabTests);",
    "List lab tests with normal ranges exceeding '100 mg/dL'.": "SELECT name, normal_range FROM LabTests WHERE normal_range > '100 mg/dL';"
}

# Preprocess predefined queries
preprocessed_queries = [preprocess(query) for query in PREDEFINED_QUERIES.keys()]

# Initialize the vectorizer and fit on preprocessed queries
vectorizer = TfidfVectorizer().fit(preprocessed_queries)
predefined_vectors = vectorizer.transform(preprocessed_queries)

def get_top_n_sql_queries(user_query, n=3, threshold=0.3):
    """
    Returns the top N SQL queries based on cosine similarity.
    
    :param user_query: The natural language query input by the user.
    :param n: Number of top matches to return.
    :param threshold: Minimum similarity score to consider a match.
    :return: List of tuples containing SQL query, matched natural language query, and similarity score.
    """
    user_query_preprocessed = preprocess(user_query)
    user_vector = vectorizer.transform([user_query_preprocessed])
    similarities = cosine_similarity(user_vector, predefined_vectors).flatten()
    top_n_indices = similarities.argsort()[-n:][::-1]
    top_n_similarities = similarities[top_n_indices]

    results = []
    for idx, sim in zip(top_n_indices, top_n_similarities):
        if sim >= threshold:
            matched_nl_query = list(PREDEFINED_QUERIES.keys())[idx]
            sql = PREDEFINED_QUERIES[matched_nl_query]
            results.append((sql, matched_nl_query, sim))
    
    if not results:
        # Return a default SQL query and indicate no good match was found
        default_query = "SELECT name, role FROM Employees;"
        results.append((default_query, "Default: List all employees.", 0.0))
    
    return results
