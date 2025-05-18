"""
Real implementation tests for AMM Engine without mocks.

These tests focus on testing actual functionality with real dependencies
and proper test isolation using temporary directories and databases.
"""

import os
import pytest
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from amm_project.models.amm_models import (
    AMMDesign,
    GeminiConfig,
    GeminiModelType,
    AdaptiveMemoryConfig,
    KnowledgeSourceConfig,
    KnowledgeSourceType
)
from amm_project.models.memory_models import InteractionRecordPydantic
from amm_project.engine.amm_engine import AMMEngine

# Test data
SAMPLE_KNOWLEDGE = """
This is a test knowledge base.
It contains information about testing.
Use this for testing purposes only.
"""

@pytest.fixture(scope="module")
def temp_dir():
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
def minimal_design():
    """Create a minimal AMMDesign for testing."""
    return AMMDesign(
        name="TestDesign",
        gemini_config=GeminiConfig(
            model_name=GeminiModelType.GEMINI_FLASH_LATEST
        ),
        adaptive_memory=AdaptiveMemoryConfig(
            enabled=True,
            db_name_prefix="test_adaptive_memory"
        )
    )

@pytest.fixture
def engine_with_knowledge(minimal_design, tmp_path):
    """Create an AMMEngine instance with test knowledge."""
    # Create a temporary knowledge file
    knowledge_file = tmp_path / "knowledge.txt"
    knowledge_file.write_text(
        "This is a test knowledge base.\n"
        "It contains information about testing.\n"
        "Use this for testing purposes..."
    )
    
    # Create a knowledge source
    knowledge_source = KnowledgeSourceConfig(
        name="Test Knowledge",
        type=KnowledgeSourceType.FILE,
        path=str(knowledge_file),
        content_type="text/plain"
    )
    
    # Create a design with the knowledge source
    minimal_design.knowledge_sources = [knowledge_source]
    
    # Create the engine
    engine = AMMEngine(design=minimal_design, base_data_path=str(tmp_path))
    
    # Clear any existing records before returning the engine
    if hasattr(engine, 'adaptive_memory') and hasattr(engine.adaptive_memory, 'session'):
        # Clear interaction records
        engine.adaptive_memory.session.query(engine.adaptive_memory.InteractionRecord).delete()
        engine.adaptive_memory.session.commit()
    
    return engine

def test_engine_initialization(minimal_design, temp_dir):
    """Test basic engine initialization."""
    # Temporarily remove the API key from the environment
    api_key = os.environ.pop('GEMINI_API_KEY', None)
    
    try:
        engine = AMMEngine(design=minimal_design, base_data_path=str(temp_dir))
        
        assert engine.design == minimal_design
        # Check that the SQLite database file exists
        sqlite_path = Path(temp_dir) / f"{minimal_design.adaptive_memory.db_name_prefix}_{minimal_design.design_id}.sqlite"
        assert sqlite_path.exists()
    finally:
        # Restore the API key
        if api_key is not None:
            os.environ['GEMINI_API_KEY'] = api_key

def test_interaction_record_lifecycle(engine_with_knowledge):
    """Test the full lifecycle of interaction records (CRUD operations)."""
    # Create a test record with a unique query to avoid conflicts
    test_query = f"test query {uuid4()}"
    test_record = {
        "query": test_query,
        "response": "test response",
        "timestamp": datetime.now(timezone.utc),
        "additional_metadata": {"test": "data", "source": "test_interaction"}
    }
    
    # Test adding a record
    record_id = engine_with_knowledge.add_interaction_record(
        InteractionRecordPydantic(**test_record)
    )
    assert record_id is not None, "Failed to add record"
    
    # Test retrieving records
    records = engine_with_knowledge.get_recent_interaction_records(limit=10)
    assert len(records) > 0, "No records found after adding"
    
    # Find our test record using the unique query
    test_record = next((r for r in records if r.query == test_query), None)
    assert test_record is not None, f"Test record with query '{test_query}' not found in records: {records}"
    assert test_record.response == "test response"
    assert test_record.additional_metadata.get("source") == "test_interaction"
    
    # Test updating the record
    if hasattr(test_record, 'id'):
        # Create an update using the correct Pydantic model
        from amm_project.models.memory_models import InteractionRecordUpdatePydantic
        update_data = InteractionRecordUpdatePydantic(
            response="updated response",
            additional_metadata={"test": "updated", "source": "test_interaction_updated"}
        )
        
        # Apply update
        engine_with_knowledge.update_interaction_record(str(test_record.id), update_data)
        
        # Verify update
        updated_records = engine_with_knowledge.get_recent_interaction_records(limit=10)
        updated_record = next(
            (r for r in updated_records 
             if hasattr(r, 'id') and str(r.id) == str(test_record.id)),
            None
        )
        assert updated_record is not None
        assert updated_record.response == "updated response"
        assert updated_record.additional_metadata.get("test") == "updated"
        
        # Test deleting the record
        engine_with_knowledge.delete_interaction_record(str(test_record.id))
        
        # Verify deletion
        remaining_records = engine_with_knowledge.get_recent_interaction_records(limit=10)
        deleted_record = next(
            (r for r in remaining_records 
             if hasattr(r, 'id') and str(r.id) == str(test_record.id)),
            None
        )
        assert deleted_record is None, "Record was not deleted"

def test_process_query(engine_with_knowledge):
    """Test the process_query method with a simple query."""
    # Save the original API key
    original_api_key = os.environ.get('GEMINI_API_KEY')
    
    try:
        # Test without API key
        if original_api_key:
            del os.environ['GEMINI_API_KEY']
        
        # The engine should still work for non-LLM operations
        response = engine_with_knowledge.process_query("test query")
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Test with API key if available
        if original_api_key:
            os.environ['GEMINI_API_KEY'] = original_api_key
            engine_with_key = AMMEngine(
                design=engine_with_knowledge.design,
                base_data_path=str(Path(engine_with_knowledge.instance_data_path).parent / "with_key")
            )
            response = engine_with_key.process_query("test query with key")
            assert isinstance(response, str)
            assert len(response) > 0
    finally:
        # Restore the API key
        if original_api_key is not None:
            os.environ['GEMINI_API_KEY'] = original_api_key

def test_knowledge_retrieval(engine_with_knowledge):
    """Test that knowledge retrieval works with the real database."""
    # Create unique test records with timestamps
    test_records = [
        {"query": f"testing knowledge base {uuid4()}", "response": "Test response 1"},
        {"query": f"search for something {uuid4()}", "response": "Test response 3"},
        {"query": f"another test query {uuid4()}", "response": "Test response 2"}
    ]
    
    # Store the queries for later verification
    test_queries = {r["query"] for r in test_records}
    
    # Add records with timestamps spaced out
    for i, record_data in enumerate(test_records):
        record = InteractionRecordPydantic(
            query=record_data["query"],
            response=record_data["response"],
            timestamp=datetime.now(timezone.utc) - timedelta(minutes=len(test_records)-i),
            additional_metadata={"test": "knowledge_retrieval", "index": i}
        )
        engine_with_knowledge.add_interaction_record(record)
    
    # Test retrieving recent interactions
    recent = engine_with_knowledge.get_recent_interaction_records(limit=2)
    assert len(recent) == 2, f"Should return exactly 2 most recent records, got {len(recent)}: {recent}"
    
    # Check that we have the expected records (order independent)
    recent_queries = {r.query for r in recent}
    assert len(recent_queries.intersection(test_queries)) > 0, \
        f"Expected some of {recent_queries} to be in {test_queries}"
    
    # Test getting all records
    all_records = engine_with_knowledge.get_recent_interaction_records(limit=10)
    assert len(all_records) >= len(test_records), \
        f"Expected at least {len(test_records)} records, got {len(all_records)}"

def test_error_handling(engine_with_knowledge):
    """Test error handling for invalid operations."""
    # Test adding invalid record (should not raise but return None)
    result = engine_with_knowledge.add_interaction_record("not a valid record")
    assert result is None, "Expected None when adding invalid record"
    
    # Test updating non-existent record (should not raise)
    try:
        engine_with_knowledge.update_interaction_record(
            "non-existent-id",
            {"response": "should not fail"}
        )
    except Exception as e:
        pytest.fail(f"Updating non-existent record raised an exception: {e}")
    
    # Test deleting non-existent record (should not raise)
    try:
        engine_with_knowledge.delete_interaction_record("non-existent-id")
    except Exception as e:
        pytest.fail(f"Deleting non-existent record raised an exception: {e}")

# Note: Tests requiring actual API calls to Gemini are intentionally omitted
# as per the requirement to not use mocks and to avoid real API calls in tests.
