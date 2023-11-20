# Import necessary modules
from algosdk import account, mnemonic
from algosdk import transaction
from typing import Dict, Any
import json
from base64 import b64decode
from algosdk.v2client import algod


# Connecting to the Algorand Testnet
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)


# # Function to generate Algorand account
# def generate_algorand_account():
#     private_key, address = account.generate_account()
#     return private_key, address

# for _ in range(2):
#     private_key, address = generate_algorand_account()
#     print(f"Generated account - Address: {address}, Private Key: {private_key}")


# In order to run this application with differe accounts you must:
# 1. Uncomment the codes from line 16 to 23 and comment all other lines below,
# This will generate two new accounts, save replace the addrA,addrB and pkA,pkB with relevant
# addresses and private keys.
# 2. Fund the accounts using https://bank.testnet.algorand.network/ or any other Algorand testnet dispenser
# 3. Uncomment all other codes that were previously not commented and run the python file

# Account details for user A and B below were saved after creation and have already been funded


addrA = "NK3KOECJ3WYJWCGA2TGMOIGGGJTR6JMBBHRZL5EJN2X73TM22NMOC2XF3A"
pkA = "i+wzKA+H7qjuKhVbi8ym3+1NivNPtVhqjhOgAOscrFZqtqcQSd2wmwjA1MzHIMYyZx8lgQnjlfSJbq/9zZrTWA=="

addrB = "DTQKRDVSCESTTSE5CYD3RBFZZBCINJR42URWNYTH2GUEXSRGRU3XMLWI3Y"
pkB = "Vgbu4qDHKjNG+goe+92vKtO+m2NG7NGZ1O4YIL2I9mkc4KiOshElOcidFge4hLnIRIamPNUjZuJn0ahLyiaNNw=="


mnA = mnemonic.from_private_key(pkA)
mnB = mnemonic.from_private_key(pkB)

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

# Sign with secret key of creator, user B
stxn_ASA = txn.sign(pkB)

# Send the transaction to the network and retrieve the txid.
ASA_txid = algod_client.send_transaction(stxn_ASA)
print(f"Sent asset create transaction with txid: {ASA_txid}")

# Wait for the transaction to be confirmed
ASA_results = transaction.wait_for_confirmation(algod_client, ASA_txid, 4)
print(f"Result confirmed in round: {ASA_results['confirmed-round']}")

# Grab the asset id for the UCTZAR we just created
UCTZAR_asset = ASA_results["asset-index"]
print(f"Asset ID created: {UCTZAR_asset}")

# Opt-in transaction for account A
A_optin = transaction.AssetOptInTxn(
    sender=addrA, sp=UCTZAR_params, index=UCTZAR_asset
)
signed_optin_txn = A_optin.sign(pkA)
A_optin_txid = algod_client.send_transaction(signed_optin_txn)
print(f"Sent opt in transaction with txid: {A_optin_txid}")

# Wait for the Opt-in transaction to be confirmed
optin_results = transaction.wait_for_confirmation(algod_client, A_optin_txid, 4)
print(f"Result confirmed in round: {optin_results['confirmed-round']}")

###################################################################################################

suggested_params = algod_client.suggested_params()

# Payment transaction from account A to account B
txn_A = transaction.PaymentTxn(addrA, suggested_params, addrB, 5000000)

# Asset transfer transaction from account B to account A
txn_B = transaction.AssetTransferTxn(
    sender=addrB,
    sp=suggested_params,
    receiver=addrA,
    amt=2,
    index=UCTZAR_asset,
)


# Assign group id to the transactions
transaction.assign_group_id([txn_A, txn_B])


# Signing transactions
stxn_A = txn_A.sign(pkA)
stxn_B = txn_B.sign(pkB)

# Combining the signed transactions into a single list
signed_group = [stxn_A, stxn_B]

# Only the first transaction id is returned
atomic_tx_id = algod_client.send_transactions(signed_group)

# wait for confirmation
atomic_result: Dict[str, Any] = transaction.wait_for_confirmation(
    algod_client, atomic_tx_id, 4
)
print(f"txID: {atomic_tx_id} confirmed in round: {atomic_result.get('confirmed-round', 0)}")