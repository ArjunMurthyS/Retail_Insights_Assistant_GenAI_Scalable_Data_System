import duckdb
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

class DBManager:
    def __init__(self, db_path=":memory:"):
        """
        Initialize the DuckDB connection.
        If db_path represents a persistent file, it will be used.
        Otherwise, an in-memory database is used.
        """
        self.con = duckdb.connect(database=db_path)
        logger.info(f"DuckDB initialized with path: {db_path}")

    def close(self):
        """
        Close the DuckDB connection explicitly.
        """
        if self.con:
            self.con.close()
            logger.info("DuckDB connection closed.")

    def ingest_csv(self, file_path, table_name="sales"):
        """
        Ingest a CSV file into a DuckDB table.
        """
        logger.info(f"Ingesting {file_path} into table {table_name}")
        try:
            # Drop table if exists to allow reloading
            self.con.execute(f"DROP TABLE IF EXISTS {table_name}")
            
            # Create a table directly from the CSV
            # DuckDB's read_csv_auto is very powerful
            self.con.execute(f"""
                CREATE TABLE {table_name} AS 
                SELECT * FROM read_csv_auto('{file_path}', normalize_names=True)
            """)
            
            # Verify ingestion
            count = self.con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            logger.info(f"Successfully ingested {count} rows into {table_name}")
            return True, f"Ingested {count} rows."
        except duckdb.Error as e:
            logger.error(f"DuckDB Ingestion Error: {e}")
            return False, f"Database Error: {str(e)}"
        except Exception as e:
            logger.error(f"Error ingesting CSV: {e}")
            return False, f"File Error: {str(e)}"

    def execute_query(self, sql_query):
        """
        Execute a SQL query and return a Pandas DataFrame.
        """
        logger.info(f"Executing query: {sql_query}")
        try:
            # Safety check (basic) - sophisticated checks should be in Validator agent
            if "drop" in sql_query.lower() or "delete" in sql_query.lower():
                raise ValueError("Unsafe query detected: DROP/DELETE not allowed.")

            df = self.con.execute(sql_query).df()
            return df
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise e

    def get_schema(self, table_name="sales"):
        """
        Get the schema of the table to help agents understand the structure.
        """
        try:
            df = self.con.execute(f"DESCRIBE {table_name}").df()
            # Convert to a string representation for the LLM
            schema_str = df.to_markdown(index=False)
            return schema_str
        except Exception as e:
            return str(e)

if __name__ == "__main__":
    # Test locally
    logging.basicConfig(level=logging.INFO)
    db = DBManager()
    # Assuming the path relative to where this might run
    # Update this path to match your actual local path for testing
    # Use relative path for portability
    # Assuming script is run from project root or src
    path = os.path.join(os.getcwd(), "Sales_Dataset", "Amazon Sale Report.csv")
    if os.path.exists(path):
        db.ingest_csv(path)
        print(db.get_schema())
        print(db.execute_query("SELECT * FROM sales LIMIT 5"))
    else:
        print(f"File not found for testing: {path}")
