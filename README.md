
# Database Agent using Cosine Similarity

A Python-based project that converts user-provided natural language queries into SQL queries using cosine similarity. It uses a mock database for testing purposes and an SQLite database for deployment, enabling users to retrieve information about departments, employees, lab tests, and more without needing to write SQL themselves.

## Features

- **Natural Language to SQL Conversion**: Converts user queries into SQL using a predefined set of natural language queries.
- **Cosine Similarity Calculation**: Uses cosine similarity to find the best match for the user's input from predefined queries.
- **Mock Database for Testing**: Simulates database interactions with a mock setup during development and testing.
- **SQLite for Deployment**: Uses SQLite (`lab.db`) for storing data in production, allowing easy deployment and interaction with real data.

## Requirements

- Python 3.8+
- Install the required packages using:

    ```bash
    pip install -r requirements.txt
    ```

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Ramlavn/Database-Agent.git
    cd Database-Agent
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Database Setup**:
   - **For Testing**: The project uses a mock database setup during development.
   - **For Deployment**: Ensure that `lab.db` is in the project root for a real SQLite database. You can modify `db.py` to initialize the database if required.

## Usage

- **Run the Application**:

    To start the application, run:

    ```bash
    streamlit run app.py
    ```

- **Provide a Query**: Enter a natural language query, such as:
    - "List all lab tests with a price above 100."
    - "Show employees in the Immunology department."
    
    The application will convert the input into an SQL query using cosine similarity and return the results.

### Project Structure

- **app.py**: The main entry point for running the application, handling user input and output.
- **db.py**: Contains functions for mock database setup during testing and connection to SQLite for deployment.
- **lab.db**: SQLite database file used during deployment for storing data related to departments, employees, and lab tests.
- **similarity.py**: Implements the cosine similarity logic for matching user input with predefined queries and generating corresponding SQL statements.
- **requirements.txt**: Lists all necessary Python packages to run the project.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any new features or bug fixes.

## Contact

For any questions or suggestions, please reach out to:

- **Name** - Ramlavan A
- **GitHub**: [Ramlavn](https://github.com/Ramlavn)
