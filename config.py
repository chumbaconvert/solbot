from solana.rpc.api import Client
from solders.keypair import Keypair #type: ignore

PRIV_KEY = "private key"
RPC = "rpc url"
UNIT_BUDGET =  85_000
JITO_FEE =  10_000_000
client = Client(RPC)
payer_keypair = Keypair.from_base58_string(PRIV_KEY)

API_ID=telegramapiid
API_HASH="telegramapihash"
PHONE_NUMBER=+10000000000
CHANNEL_CHAT_ID=channelchatid