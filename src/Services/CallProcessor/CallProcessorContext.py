from typing import List
from src.Dto.Models import UserResponse
from Services.CallProcessor import CallProcessorStrategy


class CallProcessorContext:
    """
    A context class for managing and processing call strategies.
    This class allows adding multiple call processing strategies, setting user information,
    processing calls through the strategies, and retrieving summarized results.
    Attributes:
        _strategies (List[CallProcessorStrategy]): A list of call processing strategies.
    """
    _strategies:List[CallProcessorStrategy]

    def __init__(self):
        """
        Initializes the CallProcessorContext with an empty list of strategies.
        """
        self._strategies = []

    def add_strategy(self, strategy:CallProcessorStrategy):
        """
        Adds a call processing strategy to the context.
        """
        self._strategies.append(strategy)

    def set_user(self, user:UserResponse):
        """
        Sets the user information for all strategies in the context.
        """
        for strategy in self._strategies:
            strategy.set_user(user)

    def process(self, call):
        """
        Processes a call using the strategies in the context. Returns the price
        from the first strategy that provides a non-None result, or None if no
        strategy provides a result.
        """
        for strategy in self._strategies:
            price = strategy.process(call)
            if price is not None:
                return price
        return None
    
    def get_results(self):
        """
        Retrieves the accumulated results from all strategies, including a summary
        of total seconds and total cost.
        """
        results = {}
        total_amount = 0
        total_seconds = 0
        for strategy in self._strategies:
            total_amount += strategy._calls_cost_acumulated
            total_seconds += strategy._calls_seconds_acumulated
            results.update(strategy.get_totals())
        results.update({"summarize":{
            "seconds": total_seconds,
            "amount": total_amount
        } })
        return results