// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.4.22 <0.9.0;

contract auth2 {
    address owner;
    // uint expiry = 60;
    mapping (string=> Otp) otps;

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

    function generateOTP(string memory user, uint time) public ownerOnly{
        uint otp = uint(keccak256(abi.encodePacked(block.timestamp,block.difficulty,  
        msg.sender))) % 1000000;
        saveOTP(otp,user,time);
    }

    function saveOTP(uint authenticationToken, string memory user, uint time) internal {
    require(authenticationToken > 0);
    otps[user].otpCode = authenticationToken;
    otps[user].createdTime = time;
  }

  function getAuthenticationToken(string memory user) public view returns (uint) {
    return otps[user].otpCode;
  }

  function getTime(string memory user) public view returns (uint) {
      return block.timestamp - otps[user].createdTime;
  }

    function validateOTP(uint code, string memory user, uint time) public view returns(bool){
        if (time - otps[user].createdTime < 60000) {
            return otps[user].otpCode == code;
        }
        else{
            return false;
        }
    }
}