import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from backend.src.models.environment_config import DevelopmentEnvironmentCreate
from backend.src.services.environment_setup import EnvironmentSetupService


@pytest.fixture
def mock_db_session():
    """Mock database session for testing."""
    session = Mock(spec=Session)
    return session


@pytest.fixture
def environment_service():
    """Create an instance of EnvironmentSetupService for testing."""
    return EnvironmentSetupService()


def test_create_environment(mock_db_session, environment_service):
    """Test creating a development environment."""
    # Arrange
    new_env_data = DevelopmentEnvironmentCreate(
        name="Test Environment",
        description="A test environment",
        runtime_version="Python 3.11",
        dependencies={"fastapi": "0.104.1"},
        ide_config={"theme": "dark"}
    )
    
    # Act
    result = environment_service.create(mock_db_session, new_env_data)
    
    # Assert
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    
    # Check that the returned object has the expected attributes
    assert result.name == new_env_data.name
    assert result.description == new_env_data.description
    assert result.runtime_version == new_env_data.runtime_version


def test_get_environment(mock_db_session, environment_service):
    """Test retrieving a development environment by ID."""
    # Arrange
    env_id = "some-uuid-string"
    expected_env = MagicMock()
    mock_db_session.query().filter().first.return_value = expected_env
    
    # Act
    result = environment_service.get(mock_db_session, env_id)
    
    # Assert
    assert result == expected_env
    mock_db_session.query.assert_called_once()
    # Verify the filter was called with the correct condition
    mock_db_session.query().filter.assert_called_once()


def test_get_nonexistent_environment(mock_db_session, environment_service):
    """Test retrieving a non-existent development environment."""
    # Arrange
    env_id = "nonexistent-uuid"
    mock_db_session.query().filter().first.return_value = None
    
    # Act
    result = environment_service.get(mock_db_session, env_id)
    
    # Assert
    assert result is None


def test_delete_environment(mock_db_session, environment_service):
    """Test deleting a development environment."""
    # Arrange
    env_id = "some-uuid-string"
    env_to_delete = MagicMock()
    mock_db_session.query().filter().first.return_value = env_to_delete
    
    # Act
    result = environment_service.delete(mock_db_session, env_id)
    
    # Assert
    assert result is True
    mock_db_session.delete.assert_called_once_with(env_to_delete)
    mock_db_session.commit.assert_called_once()


def test_delete_nonexistent_environment(mock_db_session, environment_service):
    """Test deleting a non-existent development environment."""
    # Arrange
    env_id = "nonexistent-uuid"
    mock_db_session.query().filter().first.return_value = None
    
    # Act
    result = environment_service.delete(mock_db_session, env_id)
    
    # Assert
    assert result is False
    mock_db_session.delete.assert_not_called()
    mock_db_session.commit.assert_not_called()