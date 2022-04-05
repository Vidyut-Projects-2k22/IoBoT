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

    // event OtpCreated(string indexed _owner, uint indexed _otpCode, uint _createdTime);
    // event OtpSent(string indexed _owner, uint indexed _otpCode);
    // event OtpExpired(string indexed _owner, uint indexed _otpCode, uint _expiredTime);
    // event OtpValidated(string indexed _owner, uint indexed _otpCode, uint _revokedTime);

    function generateOTP(string memory user, uint time) public ownerOnly{
        uint otp = uint(keccak256(abi.encodePacked(time,block.difficulty,  
        msg.sender))) % 1000000;
        saveOTP(otp,user,time);
    }

    function saveOTP(uint authenticationToken, string memory user, uint time) internal {
    require(authenticationToken > 0);
    otps[user].otpCode = authenticationToken;
    otps[user].createdTime = time;
    // emit OtpCreated(user, authenticationToken, time);
  }

  function getAuthenticationToken(string memory user) public view returns (uint) {
    //   emit OtpSent(user, otps[user].otpCode);
    return otps[user].otpCode;
  }

  function getTime(string memory user) public view returns (uint) {
      return block.timestamp - otps[user].createdTime;
  }

    function validateOTP(uint code, string memory user, uint time) public view returns(bool){
        if (time - otps[user].createdTime < 60) {
            // emit OtpValidated(user, otps[user].otpCode, time);
            return otps[user].otpCode == code;
        }
        else{
            // emit OtpExpired(user, otps[user].otpCode, time);
            return false;
        }
    }
}