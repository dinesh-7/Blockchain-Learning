from brownie import accounts, config, network


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


# this part was hardcoded for these kind of things we can go 1.forking into 2chains but not advisable 2.Moking it is  being used by many of the comapany also where you will create a whole functionality of the Agreegartor for using it locally
