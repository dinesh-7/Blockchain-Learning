from brownie import accounts, SimpleStorage


def test_deploy():
    # Arrange
    account = accounts[0]
    # ACT
    simple_storage = SimpleStorage.deploy({"from": account})
    start_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert start_value == expected


def test_update():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # ACT
    expected = 15
    simple_storage.store(expected, {"from": account})
    # Assert
    assert expected == simple_storage.retrieve()
