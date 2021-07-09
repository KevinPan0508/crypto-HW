pragma solidity ^0.4.21;

interface IFlashLoanReceiver {
    // Note: approve lender to tranfer your token in order to return the fund.
    function execute(address tokenAddr, address lender, uint256 amount) external returns (bool);
}