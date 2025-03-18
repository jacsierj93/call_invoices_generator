import os
from Dto.Enums import CallType
from Dto.Models import CallResponse
from Services.CallProcessor import CallProcessorStrategy

class NationalCallProcessorStrategy(CallProcessorStrategy):
    """
    A strategy class for processing national calls. This class implements the 
    CallProcessorStrategy interface and provides specific behavior for handling 
    national calls.

    Attributes:
        _price_per_call (float): The price per call for national calls, retrieved 
                                 from the environment variable 'NATIONAL_PRICE_PER_CALL'.
        _identifier (str): The identifier for the call type, set to the value of 
                           CallType.NATIONAL.
    """

    _price_per_call = 0.0

    def __init__(self):
        """
        Initializes the NationalCallProcessorStrategy instance by setting the 
        price per call from the environment variable and the call type identifier.
        """
        self._price_per_call = float(os.environ.get("NATIONAL_PRICE_PER_CALL"))
        self._identifier = CallType.NATIONAL.value

    def calculate(self, call: CallResponse) -> float:
        """
        Calculates the cost of a national call.

        Args:
            call (CallResponse): The call response object containing call details.

        Returns:
            float: The cost of the call, which is a fixed price per call.
        """
        return self._price_per_call

    def is_applicable(self, call: CallResponse) -> bool:
        """
        Determines if the given call is a national call by comparing the first 
        three digits of the user's phone number with the destination number.

        Args:
            call (CallResponse): The call response object containing call details.

        Returns:
            bool: True if the call is a national call, False otherwise.
        """
        return self._user.phone_number[:3] == call.numero_destino[:3]