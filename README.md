
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



<br />

<div align="center">
<h3> Connect with me<a href="https://gifyu.com/image/Zy2f"><img src="https://github.com/milaan9/milaan9/blob/main/Handshake.gif" width="50px"></a>
</h3> 
<p align="center">
    <a href="https://www.github.com/himanshu-03" target="_blank" rel="noreferrer"><img alt="Github" width="37px" src="https://github.com/himanshu-03/himanshu-03/raw/main/assets/socials/github.png"></a> &nbsp&nbsp&nbsp
    <a href="https://www.linkedin.com/in/agarwal-himanshu" target="_blank"><img alt="LinkedIn" width="35px" src="https://cdn.iconscout.com/icon/free/png-512/free-linkedin-189-721962.png?f=webp&w=256"></a> &nbsp&nbsp&nbsp
    <a href="https://twitter.com/hiimanshu_03" target="_blank"><img alt="Twitter" width="35px" src="https://freelogopng.com/images/all_img/1690643777twitter-x%20logo-png-white.png"></a> &nbsp&nbsp&nbsp
    <a href="https://www.instagram.com/_._hiimanshu_._" target="_blank"><img alt="Instagram" width="35px" src="https://github.com/himanshu-03/himanshu-03/raw/main/assets/socials/instagram.png"></a> &nbsp&nbsp&nbsp
    <a href="mailto:himanshuaaagarwal2002@gmail.com" target="_blank"><img alt="Gmail" width="35px" src="https://github.com/himanshu-03/himanshu-03/raw/main/assets/socials/gmail.png"></a>&nbsp&nbsp&nbsp
<p align="right">(<a href="#top">Back to top</a>)</p>
</p> 
