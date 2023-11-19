# from utils import get_accounts, get_algod_client
from algosdk import account, mnemonic
from algosdk import transaction
from typing import Dict, Any
import json
from base64 import b64decode

from algosdk import transaction
from algosdk.v2client import algod


# Connecting to the Algorand Testnet
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)


def generate_algorand_account():
    private_key, address = account.generate_account()
    return private_key, address

for _ in range(2):
    private_key, address = generate_algorand_account()
    print(f"Generated account - Address: {address}, Private Key: {private_key}")

addrA = "NK3KOECJ3WYJWCGA2TGMOIGGGJTR6JMBBHRZL5EJN2X73TM22NMOC2XF3A"
pkA = "i+wzKA+H7qjuKhVbi8ym3+1NivNPtVhqjhOgAOscrFZqtqcQSd2wmwjA1MzHIMYyZx8lgQnjlfSJbq/9zZrTWA=="

addrB = "DTQKRDVSCESTTSE5CYD3RBFZZBCINJR42URWNYTH2GUEXSRGRU3XMLWI3Y"
pkB = "Vgbu4qDHKjNG+goe+92vKtO+m2NG7NGZ1O4YIL2I9mkc4KiOshElOcidFge4hLnIRIamPNUjZuJn0ahLyiaNNw=="


mnA = mnemonic.from_private_key(pkA)
mnB = mnemonic.from_private_key(pkB)

skA = addrA, pkA
skB = addrB, pkB

print(mnA)
print(mnB)

###################################################################################################

# User B creates an asset UCTZAR with a total supply
# 10 units and set itself to the freeze/clawback/manager/reserve roles
UCTZAR_params = algod_client.suggested_params()
txn = transaction.AssetConfigTxn(
    sender=addrB,
    sp=UCTZAR_params,
    default_frozen=False,
    unit_name="UCTZAR",
    asset_name="UCTZAR",
    manager=addrB,
    reserve=addrB,
    freeze=addrB,
    clawback=addrB,
    url="",
    total=10,
    decimals=0,
)

# Sign with secret key of creator
stxn_ASA = txn.sign(pkB)
# Send the transaction to the network and retrieve the txid.
ASA_txid = algod_client.send_transaction(stxn_ASA)
print(f"Sent asset create transaction with txid: {ASA_txid}")
# Wait for the transaction to be confirmed
ASA_results = transaction.wait_for_confirmation(algod_client, ASA_txid, 4)
print(f"Result confirmed in round: {ASA_results['confirmed-round']}")

# grab the asset id for the asset we just created
UCTZAR_asset = ASA_results["asset-index"]
print(f"Asset ID created: {UCTZAR_asset}")


A_optin = transaction.AssetOptInTxn(
    sender=addrA, sp=UCTZAR_params, index=UCTZAR_asset
)
signed_optin_txn = A_optin.sign(pkA)
A_optin_txid = algod_client.send_transaction(signed_optin_txn)
print(f"Sent opt in transaction with txid: {A_optin_txid}")

# Wait for the transaction to be confirmed
optin_results = transaction.wait_for_confirmation(algod_client, A_optin_txid, 4)
print(f"Result confirmed in round: {optin_results['confirmed-round']}")

###################################################################################################

suggested_params = algod_client.suggested_params()

# payment from account 1 to account 2
txn_A = transaction.PaymentTxn(addrA, suggested_params, addrB, 5000000)
# payment from account 2 to account 1
txn_B = transaction.AssetTransferTxn(
    sender=addrB,
    sp=suggested_params,
    receiver=addrA,
    amt=2,
    index=UCTZAR_asset,
)


# Assign group id to the transactions (order matters!)
transaction.assign_group_id([txn_A, txn_B])


# sign transactions
stxn_A = txn_A.sign(pkA)
stxn_B = txn_B.sign(pkB)

# combine the signed transactions into a single list
signed_group = [stxn_A, stxn_B]

# Only the first transaction id is returned
atomic_tx_id = algod_client.send_transactions(signed_group)

# wait for confirmation
atomic_result: Dict[str, Any] = transaction.wait_for_confirmation(
    algod_client, atomic_tx_id, 4
)
print(f"txID: {atomic_tx_id} confirmed in round: {atomic_result.get('confirmed-round', 0)}")