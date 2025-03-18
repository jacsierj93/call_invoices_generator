from .CallsRegistryBaseConnector import CallsRegistryBaseConnector
from datetime import datetime
from fastapi import HTTPException
from typing import List
import pandas as pd
import os

from src.Dto.Models import CallResponse

class CallsRegistryCSVConnector(CallsRegistryBaseConnector):
    client = None
    # Define the expected column types
    column_types = {
        "numero_origen": str,  # Phone numbers as strings
        "numero_destino": str,  # Phone numbers as strings
        "duracion": int,  # Duration as integers
        "fecha": str,  # Dates as strings
    }

    def __init__(self):
        file_path = os.environ.get("CSV_FILE_PATH")
        try:
            self.client = pd.read_csv(f"./{file_path}", dtype=self.column_types)
            # Convert Dates to datetime
            self.client["fecha"] = pd.to_datetime(self.client["fecha"], utc=True)
        except FileNotFoundError:
             raise HTTPException(status_code=500, detail="CSV file not found")
        except ValueError as e:
            print({"error": str(e)})

    def get_list_calls(self, phone_number: int, from_date: datetime, to_date: datetime) -> List[CallResponse]:
        # Filter the DataFrame for the given phone number

        # Convert from_date and to_date to UTC timezone
        from_date = from_date.astimezone(pd.Timestamp.utcnow().tz)
        to_date = to_date.astimezone(pd.Timestamp.utcnow().tz)

        records = self.client[
            (self.client["numero_origen"] == phone_number) &
            (self.client["fecha"] >= from_date) &
            (self.client["fecha"] <= to_date)
        ]
        # Check if a record was found
        if not records.empty:

            # Convert the filtered records to a list of CallResponse objects
            return [CallResponse(**record) for record in records.sort_values(by="fecha", ascending=True).to_dict(orient="records")]
        else:
            raise HTTPException(status_code=404, detail="No calls found for the given phone number")
        