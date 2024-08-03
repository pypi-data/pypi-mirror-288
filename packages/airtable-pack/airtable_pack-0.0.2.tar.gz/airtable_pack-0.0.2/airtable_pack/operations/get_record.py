from pyairtable import Table
from pyairtable.formulas import match

def get_record(table: Table, filter: dict) -> dict:
    """ Get a single record by filter.
    - TODO: Ver si retorna 1 o muchos.
    """
    formula = match(filter)
    result = table.all(formula=formula)
    return result
