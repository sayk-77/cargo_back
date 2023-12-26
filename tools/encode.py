import json
from decimal import Decimal


class DecimalEncode(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncode, self).default(o)
