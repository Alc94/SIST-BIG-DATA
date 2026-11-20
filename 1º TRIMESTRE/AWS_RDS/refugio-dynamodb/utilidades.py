from decimal import Decimal


def convertir(obj):
    """Para json.dumps: Decimal de DynamoDB -> int/float, y fechas -> texto."""
    if isinstance(obj, Decimal):
        return int(obj) if obj == obj.to_integral_value() else float(obj)
    return str(obj)