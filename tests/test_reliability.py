import pytest
import os
import duckdb
from sales_data_analysis.data.db_manager import DBManager
from sales_data_analysis.agents.validator import ValidatorAgent

def test_db_connection_lifecycle():
    # Test connection open/close
    try:
        db = DBManager(":memory:")
        assert db.con is not None
        db.close()
    except Exception as e:
        pytest.fail(f"Lifecycle failed: {e}")

def test_ingest_empty_csv(tmp_path):
    # Create empty CSV using tmp_path fixture
    f = tmp_path / "empty.csv"
    f.write_text("")
    
    db = DBManager(":memory:")
    success, msg = db.ingest_csv(str(f))
    db.close()
    
    # Should not crash, success can be True/False depending on how DuckDB handles 0 rows
    # Recent versions might just create empty table
    assert isinstance(success, bool)

def test_ingest_malformed_csv(tmp_path):
    # Create malformed CSV
    f = tmp_path / "malformed.csv"
    f.write_text("col1,col2\n1,2,3\n") # 2 cols header, 3 cols data
    
    db = DBManager(":memory:")
    success, msg = db.ingest_csv(str(f))
    db.close()
    
    print(f"Malformed Result: {msg}")
    # DuckDB read_csv_auto is robust. If it "succeeds" by ignoring the bad row, that's fine too.
    # We just don't want an exception.
    assert isinstance(success, bool) 

def test_unsafe_sql_injection():
    db = DBManager(":memory:")
    validator = ValidatorAgent(db)
    
    unsafe_queries = [
        "DROP TABLE sales;",
        "DELETE FROM sales WHERE 1=1;",
        "ALTER TABLE sales DROP COLUMN amount;"
    ]
    
    for query in unsafe_queries:
        is_safe, reason = validator.validate_sql(query)
        print(f"Query: {query} | Safe: {is_safe} | Reason: {reason}")
        assert is_safe is False, f"Query '{query}' should be unsafe. Reason: {reason}"
        assert "unsafe" in reason.lower() or "blocked" in reason.lower() or "dangerous" in reason.lower()
    db.close()
    db.close()
