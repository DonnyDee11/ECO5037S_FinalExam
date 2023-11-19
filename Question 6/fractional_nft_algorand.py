# from utils import get_accounts, get_algod_client
from algosdk import account, mnemonic
from algosdk import transaction
from typing import Dict, Any
import json
from base64 import b64decode
import math

from algosdk import transaction
from algosdk.v2client import algod


# Connecting to the Algorand Testnet
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)


def generate_algorand_account():
    private_key, address = account.generate_account()
    return private_key, address

for _ in range(3):
    private_key, address = generate_algorand_account()
    print(f"Generated account - Address: {address}, Private Key: {private_key}")

addr1 = "NK3KOECJ3WYJWCGA2TGMOIGGGJTR6JMBBHRZL5EJN2X73TM22NMOC2XF3A"
pk1 = "i+wzKA+H7qjuKhVbi8ym3+1NivNPtVhqjhOgAOscrFZqtqcQSd2wmwjA1MzHIMYyZx8lgQnjlfSJbq/9zZrTWA=="

addr2 = "DTQKRDVSCESTTSE5CYD3RBFZZBCINJR42URWNYTH2GUEXSRGRU3XMLWI3Y"
pk2 = "Vgbu4qDHKjNG+goe+92vKtO+m2NG7NGZ1O4YIL2I9mkc4KiOshElOcidFge4hLnIRIamPNUjZuJn0ahLyiaNNw=="

addr3 = "NK3KOECJ3WYJWCGA2TGMOIGGGJTR6JMBBHRZL5EJN2X73TM22NMOC2XF3A"
pk3 = "i+wzKA+H7qjuKhVbi8ym3+1NivNPtVhqjhOgAOscrFZqtqcQSd2wmwjA1MzHIMYyZx8lgQnjlfSJbq/9zZrTWA=="



mn1 = mnemonic.from_private_key(pk1)
mn2 = mnemonic.from_private_key(pk2)
mn3 = mnemonic.from_private_key(pk3)

# User B creates an asset UCTZAR with a total supply
# 10 units and set itself to the freeze/clawback/manager/reserve roles
suggested_params = algod_client.suggested_params()
fractional_nft_creation = transaction.AssetConfigTxn(
    sender=addr1,
    sp=suggested_params,
    default_frozen=False,
    unit_name="Donel_NFT",
    asset_name="Donel_NFT",
    manager=addr1,
    reserve=addr1,
    freeze=addr1,
    clawback=addr1,
    url="",
    total=10,
    decimals= math.log10(10),
)

# Sign with secret key of creator
stxn_fractional_nft = fractional_nft_creation.sign(pk1)
# Send the transaction to the network and retrieve the txid.
fractional_ASA_txid = algod_client.send_transaction(stxn_fractional_nft)
print(f"Sent asset create transaction with txid: {fractional_ASA_txid}")
# Wait for the transaction to be confirmed
fractional_ASA_results = transaction.wait_for_confirmation(algod_client, fractional_ASA_txid, 4)
print(f"Result confirmed in round: {fractional_ASA_results['confirmed-round']}")

# grab the asset id for the asset we just created
fractional_nft_asset = fractional_ASA_results["asset-index"]
print(f"Asset ID created: {fractional_nft_asset}")

optin_2 = transaction.AssetOptInTxn(
    sender=addr2, sp=suggested_params, index=fractional_nft_asset
)
signed_optin_2_txn = optin_2.sign(pk2)
optin_2_txid = algod_client.send_transaction(signed_optin_2_txn)
print(f"Sent opt in transaction with txid: {optin_2_txid}")

optin_2_results = transaction.wait_for_confirmation(algod_client, optin_2_txid, 4)
print(f"Result confirmed in round: {optin_2_results['confirmed-round']}")

optin_3 = transaction.AssetOptInTxn(
    sender=addr3, sp=suggested_params, index=fractional_nft_asset
)
signed_optin_3_txn = optin_2.sign(pk3)
optin_3_txid = algod_client.send_transaction(signed_optin_3_txn)
print(f"Sent opt in transaction with txid: {optin_3_txid}")


optin_3_results = transaction.wait_for_confirmation(algod_client, optin_3_txid, 4)
print(f"Result confirmed in round: {optin_3_results['confirmed-round']}")

txn_2 = transaction.AssetTransferTxn(
    sender=addr1,
    sp=suggested_params,
    receiver=addr2,
    amt=3,
    index=fractional_nft_asset,
)


txn_3 = transaction.AssetTransferTxn(
    sender=addr3,
    sp=suggested_params,
    receiver=addr1,
    amt=3,
    index=fractional_nft_asset,
)


def check_nft_ownership(client, asset_id, recipients):
    for private_key, address in recipients:
        balance = AlgorandUtils.get_asset_balance(client, address, asset_id)
        if balance > 0:
            print(f"Address {address} owns {balance} units of the fractional NFT.")
        else:
            print(f"Address {address} does not own any units of the fractional NFT.")
