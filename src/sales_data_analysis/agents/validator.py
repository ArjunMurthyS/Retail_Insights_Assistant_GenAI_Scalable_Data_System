from .base_agent import BaseAgent

class ValidatorAgent(BaseAgent):
    def __init__(self, db_manager):
        super().__init__("Validator", "QA & Compliance")
        self.db_manager = db_manager

    def validate_sql(self, sql):
        """
        Check for unsafe operations.
        """
        sql_lower = sql.lower()
        if "drop " in sql_lower or "delete " in sql_lower or "alter " in sql_lower:
            return False, "Dangerous SQL keyword detected (DROP/DELETE/ALTER)."
        return True, "Safe"

    def validate_response(self, sql, data_preview, text_response):
        """
        Check for hallucinations.
        """
        prompt = f"""
        You are a QA Auditor.
        
        Context:
        1. SQL Query Used: {sql}
        2. Data Data Retrieved:
        {data_preview}
        
        3. Generated Response:
        "{text_response}"
        
        Task: Verify if the Response is factually supported by the Data. 
        If the response mentions numbers not in the data, or contradicts the data, flag it.
        
        Output:
        - VALID: [Reason]
        or
        - INVALID: [Reason]
        """
        response = self.llm.generate_response(prompt)
        
        if "INVALID" in response.upper():
            return False, response
        return True, "Passed hallucination check."
