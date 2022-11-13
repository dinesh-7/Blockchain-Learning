from brownie import Fundme, MockV3Aggregator, network, config
from scripts.helper import get_account


def deploy_fund_me():
    account = get_account()

    # if we are on a Ethereum any networks like goreli use the associated address of the respective chain
    # otherwise we need to mock the chain.. we need to use mocks
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks ...")
        mock_aggregator = MockV3Aggregator.deploy(
            18, 200000000000000000, {"from": account}
        )
        price_feed_address = mock_aggregator.address

    fund_me = Fundme.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # .get will eliminate the index list out of range error
    )  # actually we are going to send this
    # AggreatorV3Interface pricefeed address for getting the dollar to inr value from the chain.links or oracles
    # throught this address 0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e now we are going to give this throught this function
    # for the constructor of the smart contract
    print(f"Contract deployed at {fund_me.address}")


def main():
    deploy_fund_me()
