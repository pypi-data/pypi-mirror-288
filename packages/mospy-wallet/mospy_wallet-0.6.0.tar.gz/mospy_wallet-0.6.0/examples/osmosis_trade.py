
from mospy import Account, Transaction
from osmosis_protobuf.osmosis.gamm.v1beta1.tx_pb2 import MsgSwapExactAmountIn
import osmosis_protobuf.osmosis.poolmanager.v1beta1.tx_pb2 as tx_osmosis
from mospy.clients import HTTPClient

seed_phrase = ""

account = Account(
    seed_phrase=seed_phrase,
    account_number=630264,
    next_sequence=0,
    hrp="osmo",
    protobuf="osmosis"
)
client = HTTPClient(api="https://api.osmosis.interbloc.org")

tx = Transaction( account=account, chain_id="osmosis-1", gas=10000000, protobuf="osmosis")

msg = MsgSwapExactAmountIn()
msg.sender = account.address

routes = [
    {'pool_id': "678", 'token_out_denom': "uosmo"},
    {'pool_id': '1', 'token_out_denom': 'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2'}
]
for route in routes:
    _route = tx_osmosis.SwapAmountInRoute()
    _route.pool_id = int(route["pool_id"])
    _route.token_out_denom = route["token_out_denom"]
    msg.routes.append(_route)


msg.token_in.denom = "uatom"
msg.token_in.amount = str(1)
msg.token_out_min_amount = str(1)

tx.add_raw_msg(msg, type_url="/osmosis.gamm.v1beta1.MsgSwapExactAmountIn")
tx.set_fee( amount=25000, denom="uosmo")


print(client.broadcast_transaction(transaction=tx))
