var Auth = artifacts.require("Authentcation");

module.exports = function(deployer) {
  deployer.deploy(Auth);
};