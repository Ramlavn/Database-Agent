# create_db.py
import sqlite3

def create_database():
    conn = sqlite3.connect('lab.db')  # Database name is 'lab.db'
    cursor = conn.cursor()

    # Create Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        );
    ''')

    # Create LabTests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LabTests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department_id INTEGER,
            price REAL,
            normal_range TEXT,
            FOREIGN KEY (department_id) REFERENCES Departments(id)
        );
    ''')

    # Create Employees table with 'age' and 'salary'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            department_id INTEGER,
            age INTEGER,
            salary REAL,
            FOREIGN KEY (department_id) REFERENCES Departments(id)
        );
    ''')

    # Insert sample data into Departments
    departments = [
        ('Hematology', 'First Floor'),
        ('Biochemistry', 'Second Floor'),
        ('Microbiology', 'Third Floor'),
        ('Immunology', 'Fourth Floor'),
        ('Pathology', 'Fifth Floor')
    ]
    cursor.executemany('INSERT INTO Departments (name, location) VALUES (?, ?);', departments)

    # Insert sample data into LabTests
    lab_tests = [
        ('Complete Blood Count (CBC)', 1, 50.0, '4.5-11.0 x10^9/L'),
        ('Lipid Panel', 2, 75.0, 'Total Cholesterol: <200 mg/dL'),
        ('Urinalysis', 1, 30.0, 'Various parameters depending on the test'),
        ('Blood Glucose', 2, 25.0, '70-99 mg/dL'),
        ('Thyroid Stimulating Hormone (TSH)', 4, 40.0, '0.4-4.0 mIU/L'),
        ('Hepatitis Panel', 3, 100.0, 'Depends on specific markers'),
        ('Prostate-Specific Antigen (PSA)', 5, 60.0, '0-4 ng/mL'),
        ('C-Reactive Protein (CRP)', 4, 35.0, '<10 mg/L'),
        ('Vitamin D Level', 2, 80.0, '20-50 ng/mL'),
        ('Sputum Culture', 3, 90.0, 'No growth or specific pathogen identification')
    ]
    cursor.executemany('INSERT INTO LabTests (name, department_id, price, normal_range) VALUES (?, ?, ?, ?);', lab_tests)

    # Insert sample data into Employees with 'age' and 'salary'
    employees = [
        ('Alice Johnson', 'Lab Technician', 1, 28, 50000),
        ('Bob Smith', 'Lab Manager', 2, 35, 75000),
        ('Charlie Lee', 'Lab Technician', 3, 32, 52000),
        ('Diana Prince', 'Senior Analyst', 4, 45, 90000),
        ('Ethan Hunt', 'Lab Technician', 1, 29, 51000),
        ('Fiona Gallagher', 'Quality Control', 2, 31, 68000),
        ('George Costanza', 'Lab Manager', 5, 38, 76000),
        ('Hannah Baker', 'Lab Technician', 4, 27, 50000),
        ('Ian Malcolm', 'Senior Analyst', 3, 50, 95000),
        ('Jenny Lind', 'Lab Technician', 1, 26, 49000)
    ]
    cursor.executemany('INSERT INTO Employees (name, role, department_id, age, salary) VALUES (?, ?, ?, ?, ?);', employees)

    conn.commit()
    conn.close()
    print("Database 'lab.db' created and populated with mock data successfully.")

if __name__ == "__main__":
    create_database()
