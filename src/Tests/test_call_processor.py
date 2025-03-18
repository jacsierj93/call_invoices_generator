from unittest.mock import MagicMock

from Dto.Enums import CallType
from .fixtures import user, call, international_call, friends_calls, mock_strategy
from Services.CallProcessor import CallProcessorContext, CallProcessorStrategy
from Services.CallProcessor import NationalCallProcessorStrategy
from Services.CallProcessor import InternationalCallProcessorStrategy
from Services.CallProcessor import FriendsCallProcessorStrategy

def test_add_strategies():
    """Test that strategies are added correctly to the context."""
    context = CallProcessorContext()
    strategy1 = MagicMock(CallProcessorStrategy)
    strategy2 = MagicMock(CallProcessorStrategy)
    context.add_strategy(strategy1)
    context.add_strategy(strategy2)
    assert len(context._strategies) == 2
    assert context._strategies[0] == strategy1
    assert context._strategies[1] == strategy2

def test_context_add_user(user):
    """Test that strategies are set user correctly to the context."""

    context = CallProcessorContext()
    strategy1 = MagicMock(CallProcessorStrategy)
    strategy2 = MagicMock(CallProcessorStrategy)
    context.add_strategy(strategy1)
    context.add_strategy(strategy2)
    context.set_user(user)

    strategy1.set_user.assert_called_once_with(user)
    strategy2.set_user.assert_called_once_with(user)

def test_process_strategies(call):
    """Test that strategies are proccess correctly to the context."""
    expected_price = 10

    context = CallProcessorContext()
    strategy1 = MagicMock(CallProcessorStrategy)
    strategy1.process.return_value = None
    strategy2 = MagicMock(CallProcessorStrategy)
    strategy2.process.return_value = expected_price
    strategy3 = MagicMock(CallProcessorStrategy)
    context.add_strategy(strategy1)
    context.add_strategy(strategy2)
    context.add_strategy(strategy3)

    assert context.process(call) == expected_price
    context._strategies[0].process.assert_called_once_with(call)
    context._strategies[1].process.assert_called_once_with(call)
    context._strategies[2].process.assert_not_called()

def test_national_strategy(user, call, international_call , monkeypatch):
    """test correct work NationalCallProcessorStrategy"""
    expected_price = 1
    monkeypatch.setenv("NATIONAL_PRICE_PER_CALL",str(expected_price))
    expected_totals = {CallType.NATIONAL.value:{'seconds':call.duracion, 'amount':expected_price}}
    
    strategy = NationalCallProcessorStrategy()
    strategy.set_user(user)

    assert strategy.is_applicable(call)
    assert not strategy.is_applicable(international_call)
    assert strategy.process(call) == expected_price
    assert strategy._user == user
    assert strategy.get_totals() == expected_totals

def test_international_strategy(user, call, international_call, monkeypatch):
    """test correct work InternationalCallProcessorStrategy"""

    fake_price = 2
    expected_price = fake_price * international_call.duracion
    monkeypatch.setenv("INTERNATIONAL_PRICE_PER_SECOND",str(fake_price))
    expected_totals = {CallType.INTERNATIONAL.value:{'seconds':international_call.duracion, 'amount':expected_price}}
    
    strategy = InternationalCallProcessorStrategy()
    strategy.set_user(user)

    assert not strategy.is_applicable(call)
    assert strategy.is_applicable(international_call)
    assert strategy.process(international_call) == expected_price 
    assert strategy._user == user
    assert strategy.get_totals() == expected_totals

def test_friends_strategy(user, friends_calls, international_call, mock_strategy, monkeypatch):
    """test correct work FriendsCallProcessorStrategy"""

    limit_free = 1
    monkeypatch.setenv("FRIENDS_CALLS",str(limit_free))
    expected_seconds = friends_calls[0].duracion + friends_calls[1].duracion
    fake_amount = 10
    expected_totals = {CallType.FRIENDS.value:{'seconds':expected_seconds, 'amount':-fake_amount}}
    
    mock_strategy.calculate.return_value = fake_amount
    mock_strategy.is_applicable.return_value = True
    strategy = FriendsCallProcessorStrategy([mock_strategy])
    strategy.set_user(user)
    
    assert not strategy.is_applicable(international_call)
    assert strategy.is_applicable(friends_calls[0])
    assert strategy.process(friends_calls[0]) == fake_amount 
    assert strategy.process(friends_calls[1]) == fake_amount
    assert strategy._user == user
    assert strategy.get_totals() == expected_totals
    assert mock_strategy._calls_seconds_acumulated == expected_seconds
    assert mock_strategy._calls_cost_acumulated == fake_amount*2

