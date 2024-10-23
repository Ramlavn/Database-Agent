# app.py
import streamlit as st
import sqlite3
from similarity import get_top_n_sql_queries
import pandas as pd

def execute_query(sql_query):
    """
    Executes the given SQL query on the lab.db SQLite database.
    
    :param sql_query: The SQL query string to execute.
    :return: A tuple containing column names and fetched rows, or (None, error message) if an error occurs.
    """
    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        return columns, rows
    except Exception as e:
        return None, str(e)

def main():
    st.set_page_config(page_title="Lab Database AI Agent 🧠", layout="centered")

    # Sidebar description
    with st.sidebar:
        st.title("🔬 Lab Database AI Agent 🤖")
        st.write("""
            📝 **Project Description:**  
            The AI agent will suggest the most relevant SQL queries based on cosine similarity.  
            Select the query that best fits your needs, and get instant results!
        """)
        st.markdown("---")
        st.markdown("**Author: Ramlavan**")
        st.markdown("[GitHub: ramlavn](https://github.com/ramlavn)")

    # Main UI
    st.markdown("<div class='title'>🔍 Enter Your Query Below:</div>", unsafe_allow_html=True)
    st.write("Enter a natural language query, and the AI will suggest SQL queries.")

    # User input for natural language query
    user_query = st.text_input("Your Query:", placeholder="E.g., Show all available lab tests.")

    if user_query:
        with st.spinner('🔄 Generating suggestions...'):
            # Get the top 3 matching SQL queries
            suggestions = get_top_n_sql_queries(user_query, n=3, threshold=0.3)

        if suggestions:
            # Extract matched queries for display
            matched_queries = [f"{ql[1]} (Similarity: {ql[2]:.2f})" for ql in suggestions]
            sql_queries = [ql[0] for ql in suggestions]
            similarity_scores = [ql[2] for ql in suggestions]

            with st.expander("📋 Suggested SQL Queries", expanded=True):
                # Allow user to select the appropriate query with a custom message
                selected_query = st.radio(
                    "🤔 Select the most relevant SQL query based on your input:",
                    matched_queries,
                    help="Choose the query that matches your intent the best.",
                )
            
            # Find the index of the selected query
            selected_index = matched_queries.index(selected_query)
            selected_sql = sql_queries[selected_index]
            selected_similarity = similarity_scores[selected_index]
            selected_matched_query = suggestions[selected_index][1]

            # Display the selected SQL query with an option to run
            with st.expander("💡 Preview Your Selected SQL Query"):
                st.code(selected_sql, language='sql')
                st.write(f"**Similarity Score:** {selected_similarity:.2f} 🧠")
                st.write(f"**Matched Query:** {selected_matched_query} 🔍")

            # Button to execute the query
            if st.button("🚀 Run Query"):
                with st.spinner('🔎 Executing your SQL query...'):
                    columns, result = execute_query(selected_sql)

                    if columns and result:
                        st.success("✅ Query executed successfully!")
                        st.balloons()  # Fun visual when the query succeeds

                        st.subheader("🔬 Query Results:")
                        df = pd.DataFrame(result, columns=columns)
                        st.dataframe(df, use_container_width=True, height=400)
                    elif columns and not result:
                        st.info("ℹ️ The query returned no results.")
                    else:
                        st.error(f"❌ Error executing query: {result}")
        else:
            st.warning("⚠️ No suitable SQL queries found for your input. Please try rephrasing your query.")
    else:
        st.info("💡 Please enter a query above to receive suggestions.")

if __name__ == "__main__":
    main()
