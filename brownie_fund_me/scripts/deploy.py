from brownie import Fundme, Converter
from scripts.helper import get_account


def deploy_fund_me():
    account = get_account()
    fund_me = Fundme.deploy({"from": account}, publish_source=True)
    print(f"Contract deployed at {fund_me.address}")


def main():
    deploy_fund_me()
