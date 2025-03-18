from abc import ABC, abstractmethod
from Dto.Models import CallResponse, UserResponse

class CallProcessorStrategy(ABC):
    """
    Abstract base class for processing call data with a specific strategy.

    Attributes:
        _user (UserResponse): The user associated with the call processing.
        _identifier (str): A unique identifier for the strategy.
        _calls_seconds_acumulated (float): Accumulated duration of calls processed by this strategy in seconds.
        _calls_cost_acumulated (float): Accumulated cost of calls processed by this strategy.
    """
    _user: UserResponse = None
    _identifier: str = None

    _calls_seconds_acumulated = 0.0
    _calls_cost_acumulated = 0.0

    def set_user(self, user: UserResponse):
        """
        Sets the user for the strategy.

        Args:
            user (UserResponse): The user to associate with the strategy.
        """
        self._user = user

    def process(self, call: CallResponse) -> float | None:
        """
        Processes a call if the strategy is applicable. Updates the accumulated
        seconds and cost.

        Args:
            call (CallResponse): The call to process.

        Returns:
            float | None: The absolute value of the calculated cost if applicable,
                          otherwise None.
        """
        if self.is_applicable(call):
            self._calls_seconds_acumulated += call.duracion
            amount = self.calculate(call)
            self._calls_cost_acumulated += amount if amount > 0 else 0
            return abs(amount)
        return None

    def get_totals(self) -> dict:
        """
        Retrieves the accumulated totals for the strategy.

        Returns:
            dict: A dictionary containing the accumulated seconds and cost.
        """
        return {
            self._identifier: {
                "seconds": self._calls_seconds_acumulated,
                "amount": self._calls_cost_acumulated
            }
        }

    @abstractmethod
    def calculate(self, call: CallResponse) -> float:
        """
        Abstract method to calculate the cost of a call.

        Args:
            call (CallResponse): The call to calculate the cost for.

        Returns:
            float: The calculated cost of the call.
        """
        pass

    @abstractmethod
    def is_applicable(self, call: CallResponse) -> bool:
        """
        Abstract method to determine if the strategy is applicable to a call.

        Args:
            call (CallResponse): The call to check applicability for.

        Returns:
            bool: True if the strategy is applicable, False otherwise.
        """
        pass