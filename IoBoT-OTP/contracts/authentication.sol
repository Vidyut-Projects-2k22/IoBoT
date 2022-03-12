// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.4.22 <0.9.0;

contract auth {
    address owner;
    // uint expiry = 60;
    mapping (address=> Otp) otps;

    struct Otp {
        uint otpCode;
        uint createdTime;
    }

    constructor(){
        owner = msg.sender;
    }

    modifier ownerOnly {
        require(msg.sender==owner);
        _;
    }

    function generateOTP(address user) public ownerOnly{
        uint otp = uint(keccak256(abi.encodePacked(block.timestamp,block.difficulty,  
        msg.sender))) % 1000000;
        saveOTP(otp,user);
    }

    function saveOTP(uint authenticationToken, address user) internal {
    require(authenticationToken > 0);
    otps[user].otpCode = authenticationToken;
    otps[user].createdTime = block.timestamp;
  }

  function getAuthenticationToken(address user) public view returns (uint) {
    return otps[user].otpCode;
  }

  function getTime(address user) public view returns (uint) {
      return block.timestamp - otps[user].createdTime;
  }

    function validateOTP(uint code, address user) public view returns(bool){
        if (block.timestamp - otps[user].createdTime < 1 minutes) {
            return otps[user].otpCode == code;
        }
        else{
            return false;
        }
    }
}