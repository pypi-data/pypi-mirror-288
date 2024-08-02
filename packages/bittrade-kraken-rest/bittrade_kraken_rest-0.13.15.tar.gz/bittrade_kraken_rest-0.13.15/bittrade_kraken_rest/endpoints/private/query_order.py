import dataclasses
from typing import Any, List
from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result

GetAccountBalanceResult = dict[str, str]

@dataclasses.dataclass
class QueryOrderResult:
    refid: str
    userref: int
    cl_ord_id: str
    status: str
    opentm: int
    starttm: int
    expiretm: int
    vol: str
    vol_exec: str
    cost: str
    fee: str
    price: str
    stopprice: str
    limitprice: str
    trigger: str
    margin: bool
    sender_sub_id: str
    oflags: str
    descr: Any
    trades: List[str]


def query_order(*, txid: str | int, trades = False, userref = None, consolidate_taker = False):
    """
    Executes a private query for an order using the given transaction ID.

    Args:
        txid (str | int): The transaction ID of the order to query.

    Returns:
        Observable: An observable that represents the result of the query. The observable emits a tuple containing the prepared request, the URL, and the data to be sent with the request.

    Raises:
        None
    """
    data = {"txid": txid, "trades": trades, "userref": userref, "consolidate_taker": consolidate_taker}
    return prepare_private(url="/0/private/QueryOrders", data=data)


def query_order_result():
    return send_and_map_to_result(QueryOrderResult)