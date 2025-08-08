from langchain.tools import tool
from plugins.price_from_mandi import AgmarknetAPIClient

@tool("get_mandi_price", return_direct=True)
def get_mandi_price(format_='json', commodity=None, state=None, district=None, market=None, variety=None, grade=None, limit=1, offset=0):
    """
    Tool: get_mandi_price

    Description:
    Fetches the modal price (or minimum price) for a specified commodity in a particular market using the Agmarknet API.
    Only format_ is required. All other parameters are optional.
    Returns the price as a float, or 0 if not found.

    Usage:
    Use this tool to retrieve up-to-date mandi prices for agricultural commodities from Indian markets.
    """
    # Clean and validate inputs
    def clean(val):
        return val.strip() if isinstance(val, str) and val else None
    commodity = clean(commodity)
    state = clean(state)
    district = clean(district)
    market = clean(market)
    variety = clean(variety)
    grade = clean(grade)

    client = AgmarknetAPIClient()
    records = client(
        state=state,
        district=district,
        market=market,
        commodity=commodity,
        variety=variety,
        grade=grade,
        limit=limit,
        offset=offset,
        format=format_
    )
    if not records:
        return "No mandi data found."
    record = records[0]
    price = record.get("modal_price") or record.get("min_price") or 0
    try:
        return float(price)
    except Exception:
        return 0
