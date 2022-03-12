var Auth = artifacts.require("auth");

module.exports = function(deployer) {
  deployer.deploy(Auth);
};