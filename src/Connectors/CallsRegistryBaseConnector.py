from abc import ABC, abstractmethod
import datetime
from typing import List

from src.Dto.Models import CallResponse

class CallsRegistryBaseConnector(ABC):
    @abstractmethod
    def get_list_calls(self, phone_number: int, from_date: datetime, to_date: datetime) -> List[CallResponse]:
        pass