from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result
import dataclasses

@dataclasses.dataclass
class CancelOrderBatchResult:
    count: int

def cancel_order_batch_request(ids: list[str]):
    """
    Cancel an order
    :return:
    """
    if len(ids) == 1:
        return prepare_private(url="/0/private/CancelOrder", data={"txid": ids[0]})
    return prepare_private(url="/0/private/CancelOrderBatch", json={"orders": ids})


def cancel_order_batch_result():
    return send_and_map_to_result(CancelOrderBatchResult)
