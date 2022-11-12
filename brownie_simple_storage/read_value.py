# this is for interacting with the already deployed contract
from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[
        -1
    ]  # this SimpleStorage will contain the address of the contract in the array form so if you want to access the last deployed contract use SimpleStorage[-1]->15 and SimpleStorage[0]->7
    # we need address of the contract and the Abi to interact with the contract we are getting the address from this array and we dont want to give the abi brownie will automatically take the abi itself
    print(simple_storage.retrieve())


def main():
    read_contract()
