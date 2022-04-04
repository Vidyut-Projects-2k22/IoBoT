import web3
import time
import json
import math
import constants

with open("../IoBoT-OTP/build/contracts/auth2.json") as f:
    data = json.load(f)

w3 = web3.Web3(web3.HTTPProvider(constants.HTTP_PROVIDER))
address = constants.CONTRACT_ADDRESS
w3.eth.default_account = w3.eth.accounts[0]
counter = w3.eth.contract(address=address, abi=data["abi"])

def generateOTP(user):
    try:
        tx_hash = counter.functions.generateOTP(user, math.ceil(time.time())).transact()
        print(tx_hash)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt
    except Exception as e:
        print(e)

def getAuthenticationToken(user):
    try:
        tx_hash = counter.functions.getAuthenticationToken(user).transact()
        print(tx_hash)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt
    except Exception as e:
        print(e)

def validateOTP(code, user):
    try:
        tx_hash = counter.functions.validateOTP(code, user, math.ceil(time.time())).transact()
        print(tx_hash)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt
    except Exception as e:
        print(e)

generateOTP("user1")
time.sleep(1)
otp = getAuthenticationToken("user1")
print(otp)
time.sleep(1)
res = validateOTP(otp, "user1")
print(res)
time.sleep(62)
res2 = validateOTP(otp, "user1")
print(res2)