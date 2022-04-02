var Auth = artifacts.require("auth2");

module.exports = function(deployer) {
  deployer.deploy(Auth);
};