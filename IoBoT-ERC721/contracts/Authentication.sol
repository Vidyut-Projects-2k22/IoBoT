// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract Authentcation is ERC721 {
    uint expiry = 600;
    constructor() ERC721 ("Authentcation", "AUTH") {
    }
    struct token {
        uint256 id;
        uint createdTime;
    }
    mapping (address=> token) tokens;
    function generateToken(address user) public {
        uint256 tokenId = uint256(keccak256(abi.encodePacked(block.timestamp,block.difficulty,  
        msg.sender)));
        _mint(user, tokenId);
        saveOTP(tokenId,user);
    }
    function saveOTP(uint256 authenticationToken, address user) internal {
    require(authenticationToken > 0);
    tokens[user].id = authenticationToken;
    tokens[user].createdTime = block.timestamp;
  }
  function getAuthenticationToken(address user) public view returns (uint) {
    return tokens[user].id;
  }
  function validateOTP(uint256 code, address user) public returns(uint256){
        if (block.timestamp - tokens[user].createdTime < expiry){
            if (tokens[user].id == code){
                generateToken(user);
                _burn(code);
                return tokens[user].id;
            } else {
                return 0;
            }
        }
        else{
            return 0;
        }
    }
}