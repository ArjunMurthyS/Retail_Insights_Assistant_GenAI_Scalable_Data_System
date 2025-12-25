from .base_agent import BaseAgent

class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__("Analyst", "Business Insights")

    def process(self, user_query, data_preview):
        """
        Generate a natural language answer based on the query and data.
        """
        prompt = f"""
        You are a Senior Business Analyst.
        
        User Query: "{user_query}"
        
        Data Retrieved (First 50 rows / Summary):
        {data_preview}
        
        Task: Provide a concise, professional answer to the user's query based strictly on the data provided.
        If the data doesn't answer the question, say so.
        Do not cite specific row numbers unless relevant. Use data context.
        """
        response = self.llm.generate_response(prompt)
        return response
