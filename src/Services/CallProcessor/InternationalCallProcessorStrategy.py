import os
from Dto.Enums import CallType
from Dto.Models import CallResponse
from Services.CallProcessor import CallProcessorStrategy

class InternationalCallProcessorStrategy(CallProcessorStrategy):
    _price_per_second = 0.0
    def __init__(self):
        self._price_per_second = float(os.environ.get("INTERNATIONAL_PRICE_PER_SECOND"))
        self._identifier = CallType.INTERNATIONAL.value

    def calculate(self, call: CallResponse):
        return call.duracion * self._price_per_second

    def is_applicable(self, call: CallResponse) -> bool:
        return self._user.phone_number[:3] != call.numero_destino[:3]