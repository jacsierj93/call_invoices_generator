from fastapi import Depends
from Connectors import CallsRegistryBaseConnector, CallsRegistryCSVConnector
from Services import PhoneInvoiceService, UsersConnectorService
from Services.CallProcessor import NationalCallProcessorStrategy, FriendsCallProcessorStrategy, InternationalCallProcessorStrategy, CallProcessorContext

def get_call_registry()->CallsRegistryBaseConnector:
    """
    Returns the Call registry connector service
    This Class can be change for any other connector who implements the CallsRegistryBaseConnector interface
    """
    return CallsRegistryCSVConnector()

def get_user_connector():
    """
    Returns the UsersConnectorService instance.
    This service is responsible for managing user-related operations.
    """
    return UsersConnectorService()

def get_price_calculator_strategies():
    """
    Returns a CallProcessorContext instance with configured call processing strategies.
    - Adds the FriendsCallProcessorStrategy, which combines national and international strategies.
    - Adds the NationalCallProcessorStrategy for handling national calls.
    - Adds the InternationalCallProcessorStrategy for handling international calls.
    """
    national_strategy_instance = NationalCallProcessorStrategy()
    international_strategy_instance = InternationalCallProcessorStrategy()
    strategy_context = CallProcessorContext()
    strategy_context.add_strategy(FriendsCallProcessorStrategy([national_strategy_instance, international_strategy_instance]))
    strategy_context.add_strategy(national_strategy_instance)
    strategy_context.add_strategy(international_strategy_instance)
    return strategy_context

def get_service(
        call_registry: CallsRegistryBaseConnector = Depends(get_call_registry),
        user_connector: UsersConnectorService = Depends(get_user_connector),
        price_calculator: CallProcessorContext = Depends(get_price_calculator_strategies)
    ):
    """
    Returns an instance of PhoneInvoiceService.
    - call_registry: Dependency injection for the call registry connector.
    - user_connector: Dependency injection for the user connector service.
    - price_calculator: Dependency injection for the call processing strategies.
    This service handles the generation of phone invoices.
    """
    return PhoneInvoiceService(call_registry, user_connector, price_calculator)