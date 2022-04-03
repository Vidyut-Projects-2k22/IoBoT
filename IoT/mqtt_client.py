# enable TLS client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
import paho.mqtt.client as paho
from paho import mqtt
import web3

abi = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "_owner",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "_otpCode",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "_createdTime",
          "type": "uint256"
        }
      ],
      "name": "OtpCreated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "_owner",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "_otpCode",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "_expiredTime",
          "type": "uint256"
        }
      ],
      "name": "OtpExpired",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "_owner",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "_otpCode",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "_usedTime",
          "type": "uint256"
        }
      ],
      "name": "OtpSent",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "_owner",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "_otpCode",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "_revokedTime",
          "type": "uint256"
        }
      ],
      "name": "OtpValidated",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "user",
          "type": "address"
        }
      ],
      "name": "generateOTP",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "user",
          "type": "address"
        }
      ],
      "name": "getAuthenticationToken",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "user",
          "type": "address"
        }
      ],
      "name": "getTime",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "code",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "user",
          "type": "address"
        }
      ],
      "name": "validateOTP",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]

w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:7545'))
address = "0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
counter = w3.eth.contract(address=address, abi=abi)

def generateOTP(user):
    try:
        tx_hash = counter.functions.generateOTP(user).transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt
    except Exception as e:
        print(e)

def getAuthenticationToken(user):
    try:
        tx_hash = counter.functions.getAuthenticationToken(user).transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt
    except Exception as e:
        print(e)

def validateOTP(code, user):
    try:
        tx_hash = counter.functions.validateOTP(code, user).transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt
    except Exception as e:
        print(e)

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("Prasanna8446", "Prasu8446")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("64a80fb731404d588892b35b24a09263.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("encyclopedia/#", qos=1)

# a single publish, this can also be done in loops, etc.

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()
