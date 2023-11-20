# Importing necessary modules
from algosdk import account, mnemonic
from algosdk import transaction
from typing import Dict, Any
import json
from base64 import b64decode
import math
from algosdk.v2client import algod


# Connecting to the Algorand Testnet
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)

# # Function to generate Algorand account
# def generate_algorand_account():
#     private_key, address = account.generate_account()
#     return private_key, address

# for _ in range(3):
#     private_key, address = generate_algorand_account()
#     print(f"Generated account - Address: {address}, Private Key: {private_key}")

# In order to run this application with differe accounts you must:
# 1. Uncomment the codes from line 16 to 23 and comment all other lines below,
# This will generate two new accounts, save replace the addr1,addr2,addr3 and pk1,pk2,pk3 with relevant
# addresses and private keys.
# 2. Fund the accounts using https://bank.testnet.algorand.network/ or any other Algorand testnet dispenser
# 3. Uncomment all other codes that were previously not commented and run the python file

# Account details for user 1,2 and 3 below were saved after creation and have already been funded

addr1 = "N73LTWPZRQ4QN4JQ2ED2IIIUGKSR23BMTNNUCIVFUHIMGOJ57BA2TUTPYU"
pk1 = "WzlIWEnmpGAkcREIjAufYsIO8Db0mEzWeMDq4QpBHnJv9rnZ+Yw5BvEw0QekIRQypR1sLJtbQSKlodDDOT34QQ=="

addr2 = "NCQ3ZZ5XW7NME72TFQFMEQU6ENNPMYPHZ5BZVMKCLBTMHKXGGE3LRLF3HA"
pk2 = "7UHdXnTVWb/7hCpbBp+L24JY22QBfeE5zP3nAQYyYstoobznt7fawn9TLArCQp4jWvZh589DmrFCWGbDquYxNg=="

addr3 = "RBZESUKPW4CVAQ5CY4IGOQJFSDO5NFKZXWUOFXRECZEBDNODKMYW7VGGJM"
pk3 = "uCylsc7qnbkFoj5fr4sHa1mGxjCL3z4MGKcZ/Bhe6waIcklRT7cFUEOixxBnQSWQ3daVWb2o4t4kFkgRtcNTMQ=="



mn1 = mnemonic.from_private_key(pk1)
mn2 = mnemonic.from_private_key(pk2)
mn3 = mnemonic.from_private_key(pk3)

################################################################################################

# Account 1 creates a fractional NFT FRANFT with a total supply of 10 units

suggested_params = algod_client.suggested_params()

# To create a fractional NFT the total should be a a number that is a power of 10 but greater that 1
# The decimals should be a log of base 10 of the total number of units
# This ensures that the total units always equal to 1

fractional_nft_creation = transaction.AssetConfigTxn(
    sender=addr1,
    sp=suggested_params,
    default_frozen=False,
    unit_name="FRANFT",
    asset_name="FRANFT",
    manager=addr1,
    reserve=addr1,
    freeze=addr1,
    clawback=addr1,
    url="",
    total=10,
    decimals= math.log10(10),
)

# Sign account creation with private key of creator, account 1
stxn_fractional_nft = fractional_nft_creation.sign(pk1)


# Sending the transaction to the network and retrieving the transaction ID.
fractional_ASA_txid = algod_client.send_transaction(stxn_fractional_nft)
print(f"Sent asset create transaction with txid: {fractional_ASA_txid}")


# Waiting for the transaction to be confirmed
fractional_ASA_results = transaction.wait_for_confirmation(algod_client, fractional_ASA_txid, 4)
print(f"Result confirmed in round: {fractional_ASA_results['confirmed-round']}")

# Grab the asset id for the Fractional NFT we just created
fractional_nft_asset = fractional_ASA_results["asset-index"]
print(f"Asset ID created: {fractional_nft_asset}")

##################################################################################################

# Opt-in transactions for addr2 and addr3
# Account 2 opting in
optin_2 = transaction.AssetOptInTxn(
    sender=addr2, sp=suggested_params, index=fractional_nft_asset
)

# Account 2 signing the opting in transaction
signed_optin_2_txn = optin_2.sign(pk2)

# Opt in transaction sent to the network to retrieve the Transaction ID
optin_2_txid = algod_client.send_transaction(signed_optin_2_txn)
print(f"Sent opt in transaction with txid: {optin_2_txid}")

# Waiting for the transaction to be confirmed
optin_2_results = transaction.wait_for_confirmation(algod_client, optin_2_txid, 4)
print(f"Result confirmed in round: {optin_2_results['confirmed-round']}")


# Account 3 opting in
optin_3 = transaction.AssetOptInTxn(
    sender=addr3, sp=suggested_params, index=fractional_nft_asset
)

# Account 3 signing the opting in transaction
signed_optin_3_txn = optin_3.sign(pk3)

# Opt in transaction sent to the network to retrieve the Transaction ID
optin_3_txid = algod_client.send_transaction(signed_optin_3_txn)
print(f"Sent opt in transaction with txid: {optin_3_txid}")

# Waiting for the transaction to be confirmed
optin_3_results = transaction.wait_for_confirmation(algod_client, optin_3_txid, 4)
print(f"Result confirmed in round: {optin_3_results['confirmed-round']}")

###########################################################################################

# Asset transfer transactions from account 1 to account(s) 2 & 3
txn_2 = transaction.AssetTransferTxn(
    sender=addr1,
    sp=suggested_params,
    receiver=addr2,
    amt=3,
    index=fractional_nft_asset,
)


txn_3 = transaction.AssetTransferTxn(
    sender=addr1,
    sp=suggested_params,
    receiver=addr3,
    amt=3,
    index=fractional_nft_asset,
)


# Signing and sending asset transfer transactions
stxn_2 = txn_2.sign(pk1)
stxn_3 = txn_3.sign(pk1)

stxn_2_txid = algod_client.send_transaction(stxn_2)
print(f"Sent asset transfer to Address 2 transaction with txid: {stxn_2_txid}")

# Wait for the transaction to be confirmed
stxn_2_results = transaction.wait_for_confirmation(algod_client, stxn_2_txid, 4)
print(f"Result confirmed in round: {stxn_2_results['confirmed-round']}")


stxn_3_txid = algod_client.send_transaction(stxn_3)
print(f"Sent asset transfer to Address 3 transaction with txid: {stxn_3_txid}")

# Wait for the transaction to be confirmed
stxn_3_results = transaction.wait_for_confirmation(algod_client, stxn_3_txid, 4)
print(f"Result confirmed in round: {stxn_3_results['confirmed-round']}")

##############################################################################################

# List of holders with their private keys and addresses
holders = [(pk1, addr1),
              (pk2, addr2),
              (pk3, addr3),
              ]

# Function to check ownership of the fractional NFT for each holder
def check_nft_ownership(asset_id, holders):
    for private_key, address in holders:
        account_asset_info = algod_client.account_asset_info(address,asset_id)
        balance = account_asset_info.get('asset-holding', {}).get('amount', None)
        if balance > 0:
            print(f"Address {address} owns {balance} units of the fractional NFT.")
        else:
            print(f"Address {address} does not own any units of the fractional NFT.")


# Check ownership for each holder
check_nft_ownership(fractional_nft_asset, holders)