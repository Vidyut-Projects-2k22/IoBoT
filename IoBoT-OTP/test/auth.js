const Auth = artifacts.require("auth");

/*
 * uncomment accounts to access the test accounts made available by the
 * Ethereum client
 * See docs: https://www.trufflesuite.com/docs/truffle/testing/writing-tests-in-javascript
 */
contract("Auth", function (accounts) {
  it("Deployed", async function () {
    instance = await Auth.deployed();
    return assert.isTrue(true);
  });
  it("Generated OTP", async function () {
    const instance = await Auth.deployed();
    await instance.generateOTP(accounts[0]);
    return assert.isTrue(true);
  })
  it("Validated OTP", async function () {
    const instance = await Auth.deployed();
    const otp = await instance.getAuthenticationToken(accounts[0]);
    const result = await instance.validateOTP(otp, accounts[0]);
    const result2 = await instance.validateOTP(0, accounts[0]);
    assert.equal(result, true, "OTP is valid");
    assert.equal(result2, false, "OTP is invalid");
  })

});
