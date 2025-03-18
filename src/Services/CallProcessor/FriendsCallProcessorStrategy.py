import os
from typing import List
from Dto.Models import CallResponse
from Dto.Enums import CallType
from Services.CallProcessor import CallProcessorStrategy


class FriendsCallProcessorStrategy(CallProcessorStrategy):
    """
    Strategy for processing calls to friends. This strategy keeps track of the number of calls made to friends
    and applies a specific calculation logic for such calls. It also delegates the calculation to foreign strategies
    if necessary.
    Attributes:
        _friends_calls_counter (int): Counter for the number of calls made to friends.
        _available_friends_calls (int): Maximum number of calls to friends allowed, fetched from environment variables.
        _foreigns_strategies (List[CallProcessorStrategy]): List of foreign strategies to delegate calculation if needed.
    """
    _friends_calls_counter = 0;
    _available_friends_calls = 0;
    _foreigns_strategies:List[CallProcessorStrategy]

    def __init__(self, foreigns_strategies=[]):
        """
        Initializes the strategy with a list of foreign strategies 
        and sets the available friends calls limit.
        """
        self._foreigns_strategies = foreigns_strategies
        self._available_friends_calls = int(os.environ.get("FRIENDS_CALLS"))
        self._identifier = CallType.FRIENDS.value
    
    def calculate(self, call: CallResponse) -> float:
        """
        Calculates the cost of a call to a friend. If the call is within the allowed limit, it updates the counter
        and accumulates the call cost.
        """
        amount = (self.delegateCalculate(call) * -1)
        if self._friends_calls_counter < self._available_friends_calls:
            self._friends_calls_counter += 1
            self._calls_cost_acumulated += amount
        return amount
    
    def delegateCalculate(self, call: CallResponse) -> float:
        """
        Delegates the calculation to the foreign strategies. Returns the price if a strategy processes the call,
        otherwise returns None.
        """
        for strategy in self._foreigns_strategies:
            price = strategy.process(call)
            if price is not None:
                return price
        return None

    def is_applicable(self, call: CallResponse) -> bool:
        """
        Checks if the call is applicable for this strategy by verifying if the destination number is in the user's
        friends list.
        """
        return call.numero_destino in self._user.friends