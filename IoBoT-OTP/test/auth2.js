const Auth = artifacts.require("auth2");

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
    await instance.generateOTP("user1", 0);
    return assert.isTrue(true);
  })
  it("Validated OTP", async function () {
    const instance = await Auth.deployed();
    const otp = await instance.getAuthenticationToken("user1");
    const result = await instance.validateOTP(otp, "user1", 30);
    const result2 = await instance.validateOTP(0, "user1", 30);
    assert.equal(result, true, "OTP is valid");
    assert.equal(result2, false, "OTP is invalid");
  })
  it("Expired OTP", async function () {
    const instance = await Auth.deployed();
    const otp = await instance.getAuthenticationToken("user1");

    function timeout(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
    const result = await instance.validateOTP(otp, "user1", 60);
    assert.equal(result, false, "OTP has expired");

  })
});
