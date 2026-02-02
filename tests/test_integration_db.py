import pytest
from app.models.document import Document
from sqlalchemy import select

@pytest.mark.asyncio
async def test_create_and_read_document(db_session):
    # 1. Create a sample document
    new_doc = Document(
        full_text="My name is Juan dela Cruz",
        pii_entities=[{"label": "NAME_STUDENT", "text": "Juan dela Cruz", "start": 11, "end": 25}],
        model_used="integration-test-model",
        processing_time=0.123
    )
    
    # 2. Add to DB
    db_session.add(new_doc)
    await db_session.commit()
    # Note: In our fixture, 'commit' only commits to the *transaction*, 
    # which we will rollback at the end. So it's safe!
    
    # 3. Query it back
    result = await db_session.execute(select(Document).where(Document.model_used == "integration-test-model"))
    fetched_doc = result.scalars().first()
    
    # 4. Assertions
    assert fetched_doc is not None
    assert fetched_doc.full_text == "My name is Juan dela Cruz"
    assert len(fetched_doc.pii_entities) == 1
    assert fetched_doc.pii_entities[0]["label"] == "NAME_STUDENT"
    assert fetched_doc.processing_time == 0.123
