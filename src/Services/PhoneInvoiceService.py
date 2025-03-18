from typing import List
from Connectors import CallsRegistryBaseConnector
from Dto.Enums import CallType
from Dto.Models import CallDetail, CallResponse, PhoneInvoiceRequest, PhoneInvoiceResponse, UserDetail, UserResponse
from Services.CallProcessor import CallProcessorContext
from . import UsersConnectorService

class PhoneInvoiceService:
    _call_registry_service: CallsRegistryBaseConnector
    _user_service: UsersConnectorService
    _call_processor: CallProcessorContext

    def __init__(self, call_registry_service: CallsRegistryBaseConnector, user_service: UsersConnectorService, call_processor: CallProcessorContext):
        self._call_registry_service = call_registry_service
        self._user_service = user_service
        self._call_processor = call_processor

    def get_phone_invoice(self, phone_invoice_request: PhoneInvoiceRequest):
        user = self._user_service.get_user(phone_invoice_request.phone_number)
        calls = self._call_registry_service.get_list_calls(
            phone_invoice_request.phone_number,
            phone_invoice_request.date_from,
            phone_invoice_request.date_to
        )
        
        return self.process_calls(calls, user)
    
    def process_calls(self, calls:List[CallResponse], user:UserResponse):
        self._call_processor.set_user(user)
        response = self.init_response(user)
        for call in calls:
            amount = self._call_processor.process(call)
            response.calls.append(CallDetail(
                phone_number = call.numero_destino,
                duration = call.duracion,
                timestamp = call.fecha,
                amount = amount
            ))
        
        totals = self._call_processor.get_results()
        response.total_international_seconds = totals[CallType.INTERNATIONAL.value]["seconds"]
        response.total_national_seconds = totals[CallType.NATIONAL.value]["seconds"]
        response.total_friends_seconds = totals[CallType.FRIENDS.value]["seconds"]
        response.total = totals["summarize"]["amount"]
        response.gross_total = totals["summarize"]["amount"] + (totals[CallType.FRIENDS.value]["amount"] * -1)
        response.friends_discount = totals[CallType.FRIENDS.value]["amount"]
        return response
    
    def init_response(self, user:UserResponse):
        return PhoneInvoiceResponse(
            user = UserDetail(
                address = user.address,
                name = user.name,
                phone_number = user.phone_number,
            ),
            calls = [],
            total_international_seconds = 0,
            total_national_seconds = 0,
            total_friends_seconds = 0,
            gross_total = 0,
            friends_discount = 0,
            total = 0
        )
