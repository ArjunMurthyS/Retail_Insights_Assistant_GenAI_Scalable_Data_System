import pytest
import os
import pandas as pd
from sales_data_analysis.data.db_manager import DBManager

@pytest.fixture
def db():
    # Us in-memory DB for testing
    return DBManager(":memory:")

def test_ingest_and_query(db, tmp_path):
    # Create a dummy CSV
    csv_path = tmp_path / "test_sales.csv"
    df = pd.DataFrame({'id': [1, 2], 'amount': [100, 200]})
    df.to_csv(csv_path, index=False)
    
    success, msg = db.ingest_csv(str(csv_path), "test_table")
    assert success
    
    # Query
    result = db.execute_query("SELECT SUM(amount) as total FROM test_table")
    assert result.iloc[0]['total'] == 300

def test_schema_retrieval(db, tmp_path):
    csv_path = tmp_path / "test_sales.csv"
    df = pd.DataFrame({'id': [1], 'name': ['test']})
    df.to_csv(csv_path, index=False)
    db.ingest_csv(str(csv_path), "test_table")
    
    schema = db.get_schema("test_table")
    assert "id" in schema
    assert "name" in schema

def test_unsafe_query_detection(db):
    with pytest.raises(Exception):
        db.execute_query("DROP TABLE test_table")
