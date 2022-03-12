const Auth = artifacts.require("Authentcation");

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
    await instance.generateToken(accounts[0]);
    return assert.isTrue(true);
  })
  it("Validated OTP", async function () {
    const instance = await Auth.deployed();
    const otp = await instance.getAuthenticationToken(accounts[0]);
    const result = await instance.validateOTP(otp, accounts[0]);
    const result2 = await instance.validateOTP(0, accounts[0]);
    const result3 = await instance.validateOTP(otp, accounts[0]);
    const result4 = await instance.validateOTP(result, accounts[0]);
    assert.notEqual(result, 0, "OTP is valid");
    assert.equal(result2, 0, "OTP is invalid");
    assert.equal(result3, 0, "OTP refreshed");
    assert.notEqual(result4, 0, "new OTP validated");
  })
});
