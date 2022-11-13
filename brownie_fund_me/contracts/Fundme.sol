// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

//in this contract i am going to create a funding function in which you can give money to me but i want money more
//than only 50 dollars -> so i want to convert that $50 to equivalent amount of ether or wei or wei that we are going to
//give in the value section-> so how will i get todays ethereum price->so i want to connect to oracles or chainlink
//which gives me the data what i want -> with that i am going to do basic math and uint and int type casting

// https://github.com/smartcontractkit/chainlink-brownie-contracts we took the below chainlink from this github repo
//now we are going to verify this contract in etherscan for that etherscan it cannot unzip or read @chainlink so we need to paste the whole code here but brownie has a cool feature
// for that we need to create the API key from etherscan and we are adding that in the environment variable **export ETHERSCAN_TOKEN = SD8V3N8YAGHBW7AUX33IQMSU8H2M4D7UAB** and browine will verfiy the contract
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol"; //remix can read this but brownie cannot so add dependies and remapping from brownie-config.yaml

// import "./Converterlib.sol";

error Notowner(); // gas efficiency

contract Fundme {
    // using Converter for uint256;
    uint256 public constant min_USD = 2 * 1e18; //gas efficiency
    address[] public funders; // an array to store who all funded to our System
    mapping(address => uint256) public funder_amount; // map to store how much who funded
    address public immutable owner; //gas efficiency
    AggregatorV3Interface public priceFeed;

    constructor(address _pricefeed) {
        priceFeed = AggregatorV3Interface(_pricefeed);
        owner = msg.sender;
    }

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

        // AggregatorV3Interface priceFeed = AggregatorV3Interface(
        //     0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        // ); //this part was hardcoded for these kind of things we can go 1.forking into 2chains but not advisable 2.Moking it is  being used by many of the comapany also where you will create a whole functionality of the Agreegartor for using it locally
        (
            ,
            /*uint80 roundID*/
            int256 price, /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/
            ,
            ,

        ) = priceFeed.latestRoundData();
        return uint256(price); //typecasting because msg.value is in the form of uint so we want to maintain uint and this returns with 8 decimal place appended with it
    }

    function fund() public payable {
        //we are adding funds to the contract
        uint256 value_wei = msg.value;
        // require(value_wei>=min_USD,"Didn't sent enough money");
        require(
            convert_eth_to_usd(value_wei) >= min_USD,
            "Didn't sent enough money"
        );
        // require(
        //     value_wei.convert_eth_to_usd() >= min_USD,
        //     "Didn't sent enough money"
        // ); //because of this error UndeployedLibrary: Contract requires 'Converter' library, but it has not been deployed yet
        funders.push(msg.sender);
        funder_amount[msg.sender] += value_wei;
    }

    function withdraw() public onlyOwner {
        for (uint256 i = 0; i < funders.length; i++) {
            funder_amount[funders[i]] = 0;
        }
        funders = new address[](0); //this tell the array has zero objects
        //now we will reduce that money from the contract also
        // there are three method to do that 1.transfer 2.send 3.call
        //transfer (2300 gas, throws error)
        // send (2300 gas, returns bool)
        // call (forward all gas or set gas, returns bool) return bool and calldata ->we are going to use this only
        // // transfer
        // payable(msg.sender).transfer(address(this).balance);
        // // send
        // bool sendSuccess = payable(msg.sender).send(address(this).balance);
        // require(sendSuccess, "Send failed");
        // call
        (bool callSuccess, ) = payable(msg.sender).call{
            value: address(this).balance
        }("");
        require(callSuccess, "call failed");
    }

    modifier onlyOwner() {
        //require(msg.sender== owner,"only owner can access this part of contract");
        if (msg.sender != owner) revert Notowner();
        _;
    }

    //this recieve and fallback used to use from metamask itself it fund itself is not called
    receive() external payable {
        fund();
    }

    fallback() external payable {
        fund();
    }
}
