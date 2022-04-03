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

    event OtpCreated(address indexed _owner, uint indexed _otpCode, uint _createdTime);
    event OtpSent(address indexed _owner, uint indexed _otpCode, uint _usedTime);
    event OtpExpired(address indexed _owner, uint indexed _otpCode, uint _expiredTime);
    event OtpValidated(address indexed _owner, uint indexed _otpCode, uint _revokedTime);

    function generateOTP(address user) public ownerOnly{
        uint otp = uint(keccak256(abi.encodePacked(block.timestamp,block.difficulty,  
        msg.sender))) % 1000000;
        saveOTP(otp,user);
    }

    function saveOTP(uint authenticationToken, address user) internal {
    require(authenticationToken > 0);
    otps[user].otpCode = authenticationToken;
    otps[user].createdTime = block.timestamp;
    emit OtpCreated(msg.sender, authenticationToken, block.timestamp);
  }

  function getAuthenticationToken(address user) public returns (uint) {
      emit OtpSent(msg.sender, otps[user].otpCode, block.timestamp);
    return otps[user].otpCode;
  }

  function getTime(address user) public view returns (uint) {
      return block.timestamp - otps[user].createdTime;
  }

    function validateOTP(uint code, address user) public returns(bool){
        if (block.timestamp - otps[user].createdTime < 1 minutes) {
            emit OtpValidated(msg.sender, otps[user].otpCode, block.timestamp);
            return otps[user].otpCode == code;
        }
        else{
            emit OtpExpired(msg.sender, otps[user].otpCode, block.timestamp);
            return false;
        }
    }
}