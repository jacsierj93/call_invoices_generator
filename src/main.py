from fastapi import FastAPI, Depends

from Config.dependencies import get_service
from Dto.Models import PhoneInvoiceRequest
from Services import PhoneInvoiceService
app = FastAPI()

@app.post("/get-invoice/")
def get_invoice(request: PhoneInvoiceRequest, service: PhoneInvoiceService = Depends(get_service)):
    return service.get_phone_invoice(request)