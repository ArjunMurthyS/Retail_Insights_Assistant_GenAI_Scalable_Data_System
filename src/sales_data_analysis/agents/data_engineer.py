from .base_agent import BaseAgent
import re

class DataEngineerAgent(BaseAgent):
    def __init__(self, db_manager):
        super().__init__("DataEngineer", "SQL Specialist")
        self.db_manager = db_manager

    def process(self, user_query, schema):
        """
        Generate DuckDB SQL query from user query and schema.
        """
        prompt = f"""
        You are an expert Data Engineer specializing in DuckDB SQL.
        
        The table name is "sales".
        Schema:
        {schema}
        
        User Query: "{user_query}"
        
        Goal: Write a single valid DuckDB SQL query to answer the user's question.
        
        Rules:
        1. Use only the provided columns.
        2. Do NOT use markdown code blocks (\`\`\`). Just output the SQL.
        3. DATE columns might be strings, use appropriate casting if needed, e.g. strptime(Date, '%m-%d-%y').
        4. If asking for 'highest' or 'top', use ORDER BY and LIMIT.
        5. Return ONLY the SQL.
        """
        response = self.llm.generate_response(prompt)
        
        if response.startswith("Error"):
            return None, response
        
        # Clean up cleanup response
        sql = response.strip()
        sql = re.sub(r"```sql", "", sql)
        sql = re.sub(r"```", "", sql)
        
        return sql.strip(), "Generated SQL based on schema."
