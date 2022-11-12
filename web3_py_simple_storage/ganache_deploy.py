from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)
print("Installing...")
install_solc("0.6.0")  # here we are installing the solidity complier with we want
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
# print(compiled_sol)

with open("Compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# now we need byte code and the abi to intract with the contract so we will take that part alone from the json or that compiled_sol variable
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
][
    "object"
]  # this is the same what we will get in the remix
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# print(bytecode,abi)

# now we are going to connect to ganache our local blockchain network like Javascript VM or RemixVM london
ganachelink = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
myadress = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# myprivatekey = 0xae1284e2d786daa2188125ed57ef7e58079eda7d29520bff6d189b4e28d9f4f9 # but you should not ues your private key like this in code anyone can see that
private_key = os.getenv(
    "Private_key"
)  # this is by adding the privatekey in the environment varible we did with .env file
print(private_key)

# ********************************************Contract Creation*************************************************************************

# till now we compiled the contract so now create the contract with abi and bytecode
Simple_storage = ganachelink.eth.contract(abi=abi, bytecode=bytecode)
# we need nonce for mining each and every transactions so we need to create that value actually we need it for authentication
nonce = ganachelink.eth.getTransactionCount(myadress)
# print(nonce)
# To deploy the contract or to send any transaction you need to do this , if you are going to change any state in the blockchain network
# 1.first you need to create a transaction
# 2.Sign the transaction with your private key
# 3.send the transaction to the network
# 1.create
deploy_transaction = Simple_storage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": ganachelink.eth.gas_price,
        "from": myadress,
        "nonce": nonce,
    }
)
# 2.sign
signed_txn = ganachelink.eth.account.sign_transaction(
    deploy_transaction, private_key=private_key
)
# 3.send it to the Blockchain network
contract_hash = ganachelink.eth.send_raw_transaction(signed_txn.rawTransaction)
contract_recipt = ganachelink.eth.wait_for_transaction_receipt(contract_hash)
print("done! Contract deployed at ,", contract_recipt.contractAddress)
# print(contract_recipt)

# *****************************************************************Woring with Contract **********************************************************************
# now we will work with the deployed contract i.e we will call store retrieve functions

# if we need to interact with the contract we need contract address and abi
# in creation we used bytecode and abi to have contract here we are going to use the contract address instead of byte code and we are going to use ABI
Simple_storage = ganachelink.eth.contract(
    address=contract_recipt.contractAddress, abi=abi
)  # using the same variable just becasue we are going to perform the same operations
# retrive function just calling so no state change occurs
print(
    Simple_storage.functions.retrieve().call()
)  # for retrieve and we are just calling the function with .call() at the end
# store-> for this we need to do the same all steps whatever we did for the contract creation
store_transaction = Simple_storage.functions.store(7).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": ganachelink.eth.gas_price,
        "from": myadress,
        "nonce": nonce + 1,
    }
)  # the nonce value is the nonce+1 next nonce
# 2.sign
signed_txn = ganachelink.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# 3.send it to the Blockchain network
store_hash = ganachelink.eth.send_raw_transaction(signed_txn.rawTransaction)
store_recipt = ganachelink.eth.wait_for_transaction_receipt(store_hash)
# print("done! store  transaction hash  ,",store_recipt)
# again calling the retrive function just calling so no state change occurs
print(
    Simple_storage.functions.retrieve().call()
)  # for retrieve and we are just calling the function with .call() at the end
