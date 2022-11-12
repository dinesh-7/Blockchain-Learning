// SPDX-License-Identifier: MIT

//this is just to import the library function demo but in this python course again i am going to merge it in the fundme itself
// because it is creating a new json file and i dont know how to merge it
// ***UndeployedLibrary: Contract requires 'Converter' library, but it has not been deployed yet***

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol"; //remix can read this but brownie cannot so add dependies and remapping from brownie-config.yaml

library Converter {
    function convert_eth_to_usd(uint256 value_wei)
        public
        view
        returns (uint256)
    {
        uint256 one_eth_usd = eth_to_usd() * 1e10;
        uint256 total_usd = (value_wei * one_eth_usd) / 1e18; //because we are multiplying with two 10e18 so we need to divide with one 10e18
        return total_usd;
    }

    function eth_to_usd() public view returns (uint256) {
        //for this function we need to connect with chainlink to get data so use priceConsumerV3.sol in https://docs.chain.link/docs/data-feeds/price-feeds/
        //-> in that we imported that set of code from github using npm
        //we need address of goerli in which this priceconverted is deployed - Address: 0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        //then we need the ABI - so we are importing the code from the github and we are using
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        );
        (
            ,
            /*uint80 roundID*/
            int256 price, /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/
            ,
            ,

        ) = priceFeed.latestRoundData();
        return uint256(price); //typecasting because msg.value is in the form of uint so we want to maintain uint and this returns with 8 decimal place appended with it
    }
}
