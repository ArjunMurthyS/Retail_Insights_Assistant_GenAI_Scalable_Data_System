import pytest
from unittest.mock import MagicMock, patch
from sales_data_analysis.agents.validator import ValidatorAgent
from sales_data_analysis.agents.data_engineer import DataEngineerAgent

@pytest.fixture
def mock_llm_client():
    with patch("sales_data_analysis.agents.base_agent.LLMClient") as mock:
        yield mock

def test_validator_sql_safety(mock_llm_client):
    db_mock = MagicMock()
    # mock_llm_client is automatically active here
    validator = ValidatorAgent(db_mock)
    
    is_safe, msg = validator.validate_sql("SELECT * FROM sales")
    assert is_safe
    
    is_safe, msg = validator.validate_sql("DROP TABLE sales")
    assert not is_safe

def test_data_engineer_sql_generation(mock_llm_client):
    # Setup mock instance
    mock_inst = MagicMock()
    mock_inst.generate_response.return_value = "SELECT sum(amount) FROM sales"
    mock_llm_client.return_value = mock_inst
    
    db_mock = MagicMock()
    engineer = DataEngineerAgent(db_mock)
    
    sql, msg = engineer.process("What is total sales?", schema="dummy_schema")
    
    assert sql == "SELECT sum(amount) FROM sales"
