from brownie import accounts, config, SimpleStorage, network

# for testnet and the developement network differentiation
def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_simplestorage():
    account = (
        get_account()
    )  # this is the local ganache-cli first account will be comming
    # for testnet accounts like goreli accounts we need to add accounts to the brownie through command line "brownie accounts new '{NAME}' freecodecamp-accounts"
    # account = accounts.load("freecodecamp-accounts")
    # next method is from env through brownie-config.yaml
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

    # no need to complie it's in build complie and no signing it auto detect Transact(state change of the blockchain) and call also
    # so direct deploying
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)
    # we will do the same what we did in web3_simplestorage same retrive, store(7)->only we need to add address,retrieve
    stored_val = simple_storage.retrieve()
    print(stored_val)
    transaction = simple_storage.store(15, {"from": account})
    # here also we will wait there we used wait_for_transaction reciept
    transaction.wait(
        1
    )  # pattrick told we are waiting for one block or one second dont know
    stored_val = simple_storage.retrieve()
    print(stored_val)


def main():
    # print("hello")
    deploy_simplestorage()
