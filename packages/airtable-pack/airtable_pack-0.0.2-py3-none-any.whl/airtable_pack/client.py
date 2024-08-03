from typing import List

from pyairtable import Api, Base, Table

from airtable_pack.operations.get_record import get_record

class Airtable:
    def __init__(self, api_key: str, base_id: str):
        self.api = Api(api_key=api_key)
        self.base_id: str = base_id
        self.base: Base = self.api.base(self.base_id)
    
    def get_table(self, table_name: str) -> Table:
        return self.base.table(table_name)

    def get_record(self, table: Table, filter_: dict) -> List[dict]:
        return get_record(table=table, filter_=filter_)

    def delete_record(self):
        raise NotImplementedError("No está implementada el borrado.")
