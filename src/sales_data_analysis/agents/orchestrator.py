from .base_agent import BaseAgent
from .planner import PlannerAgent
from .data_engineer import DataEngineerAgent
from .analyst import AnalystAgent
from .validator import ValidatorAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self, db_manager):
        super().__init__("Orchestrator", "Manager")
        self.db_manager = db_manager
        self.planner = PlannerAgent()
        self.data_engineer = DataEngineerAgent(db_manager)
        self.analyst = AnalystAgent()
        self.validator = ValidatorAgent(db_manager)

    def process(self, user_query):
        """
        Orstrate the flow:
        1. Identify if it's a simple lookup or complex analysis.
        2. Delegate to Planner or directly to Data Engineer.
        3. Validate results.
        4. Return final response.
        """
        print(f"[{self.name}] Received query: {user_query}")
        
        # Simple routing logic (could be LLM driven for more complexity)
        # For this assignment, we'll assume most queries go through the full pipeline
        # for robustness.
        
        # 1. Planner decomposes the query
        plan = self.planner.process(user_query)
        print(f"[{self.name}] Plan: {plan}")
        
        results = {}
        # 2. Execute plan steps (simplified for MVP: treating plan as a single complex query intent mostly)
        # In a full system, we'd iterate over plan steps. Here we'll pass the context to Data Engineer.
        
        sql_query, explanation = self.data_engineer.process(user_query, schema=self.db_manager.get_schema())
        print(f"[{self.name}] Generated SQL: {sql_query}")
        
        if sql_query is None:
             return f"Could not generate SQL. Reason: {explanation}"

        # 3. Validate SQL Safety
        is_safe, failure_reason = self.validator.validate_sql(sql_query)
        if not is_safe:
            return f"Required action blocked by safety policy: {failure_reason}"
        
        # 4. Execute Data Retrieval
        try:
            data_df = self.db_manager.execute_query(sql_query)
            # Limit rows for context window if too large (naive approach for MVP)
            data_preview = data_df.head(50).to_markdown(index=False)
        except Exception as e:
            return f"Error executing query: {str(e)}"
            
        # 5. Analyst generates insights
        final_response = self.analyst.process(user_query, data_preview)
        
        # 6. Final Hallucination Check
        is_valid, validation_msg = self.validator.validate_response(sql_query, data_preview, final_response)
        if not is_valid:
             print(f"[{self.name}] Validation Warning: {validation_msg}")
             # We might choose to regenerate or append a warning.
             final_response += f"\n\n(Note: Automated validation flagged potential inconsistency: {validation_msg})"
             
        return final_response
