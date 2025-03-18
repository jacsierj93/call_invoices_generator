from unittest.mock import MagicMock
import pytest
from Dto.Models import CallResponse, UserResponse
from Services.CallProcessor import CallProcessorStrategy

@pytest.fixture
def user():
    """Fixture for a mock UserResponse."""
    return UserResponse(
        address="123 Main St",
        name="John Doe",
        phone_number="+54911111111",
        friends=["+54922222222", "+55933333333"]
    )


@pytest.fixture
def call():
    """Fixture for a mock CallResponse."""
    return CallResponse(
        numero_origen="+54911111111",
        numero_destino="+54922222222",
        duracion=120,
        fecha="2025-03-15"
    )


@pytest.fixture
def international_call():
    """Fixture for a mock CallResponse."""
    return CallResponse(
        numero_origen="+54911111111",
        numero_destino="+55922222222",
        duracion=200,
        fecha="2025-03-15"
    )

@pytest.fixture
def friends_calls():
    """Fixture for a mock CallResponse."""
    return [
        CallResponse(
            numero_origen="+54911111111",
            numero_destino="+54922222222",
            duracion=200,
            fecha="2025-03-15"
        ),
        
        CallResponse(
            numero_origen="+54911111111",
            numero_destino="+54922222222",
            duracion=200,
            fecha="2025-03-15"
        ),
    ]

@pytest.fixture
def mock_strategy():
    return type(
            "AnonymousCallProcessorStrategy",  
            (CallProcessorStrategy,),
            {
                "calculate": MagicMock(),
                "is_applicable": MagicMock()
            }
        )()