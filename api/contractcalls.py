from django.conf import settings
from . import contract_config
import json
import os

from web3 import Web3
from web3.middleware import geth_poa_middleware


# Contract data
contract_address = contract_config.config["contract_address"]
public_key = contract_config.config["public_key"]
private_key = contract_config.config["private_key"]
contract_filepath = os.path.join(
    settings.BASE_DIR, "api/Admin.json")
with open(contract_filepath, "r") as file:
    contract_json = json.load(file)
abi = contract_json["abi"]
bytecode = contract_json["bytecode"]


# w3 = Web3(Web3.HTTPProvider("https://matic-mumbai.chainstacklabs.com"))
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
w3.eth.defaultAccount = public_key
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
myContract = w3.eth.contract(address=contract_address, abi=abi)


# def deploy_contract(name):
#     new_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
#     nonce = w3.eth.get_transaction_count(public_key)
#     new_tx = new_contract.constructor(name, name).build_transaction(
#         {"from": public_key, "nonce": nonce})
#     signed_tx = w3.eth.account.sign_transaction(new_tx, private_key)
#     tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
#     tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#     address = tx_receipt.contractAddress
#     return address


def add_user(_userAddress, _userName, _userDescription, _profilepic):
    print("Calling contract---------------------")
    nonce = w3.eth.get_transaction_count(public_key)
    add_user_tx = myContract.functions.addUser(
        _userAddress, _userName, _userDescription, _profilepic).build_transaction({"from": public_key, "nonce": nonce, "gasPrice": 100000})
    signed_tx = w3.eth.account.sign_transaction(
        add_user_tx, private_key=private_key)
    add_user_tx_data = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(add_user_tx_data)
    return True


def add_club(
    _clubName,
    _clubDescription,
    _clubProfilePic,
    _clubcategory,
    _admin
):
    print("Calling contract---------------------")
    nonce = w3.eth.get_transaction_count(public_key)
    add_club_tx = myContract.functions.addClub(
        _clubName,
        _clubDescription,
        _clubProfilePic,
        _clubcategory,
        _admin).build_transaction({"from": public_key, "nonce": nonce, "gasPrice": 100000})
    signed_tx = w3.eth.account.sign_transaction(
        add_club_tx, private_key=private_key)
    add_club_tx_data = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(add_club_tx_data)
    return True


def add_post(
    _postContent,
    _clubId,
    _postedBy
):
    print("Calling contract---------------------")
    nonce = w3.eth.get_transaction_count(public_key)
    add_post_tx = myContract.functions.addPost(
        _postContent,
        _clubId,
        _postedBy).build_transaction({"from": public_key, "nonce": nonce, "gasPrice": 100000})
    signed_tx = w3.eth.account.sign_transaction(
        add_post_tx, private_key=private_key)
    add_post_tx_data = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(add_post_tx_data)
    return True


# def create_souvenir(account, metadata, contract_address):
#     souvenirContract = w3.eth.contract(address=contract_address, abi=abi)
#     print("minting NFT...")
#     print(w3.isConnected())
#     nonce = w3.eth.get_transaction_count(public_key)
#     print(f"nonce = {nonce}")
#     try:
#         print("trying....")
#         createCertificate_tx = souvenirContract.functions.createCertificate(
#             metadata, account
#         ).build_transaction({"from": public_key, "nonce": nonce})
#         print("Built transaction...")
#         signed_transaction = w3.eth.account.sign_transaction(
#             createCertificate_tx, private_key=private_key
#         )
#         print("Signed transaction transaction...")
#         tx_data = w3.eth.send_raw_transaction(
#             signed_transaction.rawTransaction)
#     except:
#         print("excepting...")
#         createCertificate_tx = myContract.functions.createCertificate(
#             metadata, account
#         ).build_transaction({"from": public_key, "nonce": nonce + 1})
#         print("Built transaction...")
#         signed_transaction = w3.eth.account.sign_transaction(
#             createCertificate_tx, private_key=private_key
#         )
#         print("Signed transaction transaction...")
#         tx_data = w3.eth.send_raw_transaction(
#             signed_transaction.rawTransaction)
#     # receipt = w3.eth.wait_for_transaction_receipt(tx_data)
#     print("transaction sent...")
#     token_id = myContract.functions.tokenCounter().call()
#     print(token_id)
#     return (token_id, tx_data.hex())


# def create_certificate(account, metadata):
    # print("minting NFT...")
    # print(w3.isConnected())
    # nonce = w3.eth.get_transaction_count(public_key)
    # print(f"nonce = {nonce}")
    # try:
    #     print("trying....")
    #     createCertificate_tx = myContract.functions.createCertificate(
    #         metadata, account
    #     ).build_transaction({"from": public_key, "nonce": nonce})
    #     print("Built transaction...")
    #     signed_transaction = w3.eth.account.sign_transaction(
    #         createCertificate_tx, private_key=private_key
    #     )
    #     print("Signed transaction transaction...")
    #     tx_data = w3.eth.send_raw_transaction(
    #         signed_transaction.rawTransaction)
    # except:
    #     print("excepting...")
    #     createCertificate_tx = myContract.functions.createCertificate(
    #         metadata, account
    #     ).build_transaction({"from": public_key, "nonce": nonce + 1})
    #     print("Built transaction...")
    #     signed_transaction = w3.eth.account.sign_transaction(
    #         createCertificate_tx, private_key=private_key
    #     )
    #     print("Signed transaction transaction...")
    #     tx_data = w3.eth.send_raw_transaction(
    #         signed_transaction.rawTransaction)
    # # receipt = w3.eth.wait_for_transaction_receipt(tx_data)
    # print("transaction sent...")
    # token_id = myContract.functions.tokenCounter().call()
    # print(token_id)
    # return (token_id, tx_data.hex())
