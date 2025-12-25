from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Planner", "Architect")

    def process(self, user_query):
        """
        Decompose the user query into logical steps.
        """
        prompt = f"""
        You are a Senior Data Architect.
        User Query: "{user_query}"
        
        Break this down into logical data retrieval steps.
        If it's a simple query, just state "Single Step: Retrieve appropriate data".
        If complex (e.g., comparison), list the steps.
        
        Output format: Bullet points.
        """
        response = self.llm.generate_response(prompt)
        return response
