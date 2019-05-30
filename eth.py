#!/usr/bin/python
import ethereum, binascii, requests, time

keys = set()
with open('example.csv') as f:
	for line in f.read().split('\n'):
		if line:
			repo, file, pkey = line.split(",")
			keys.add(pkey)

for priv in keys:
	try:
		eth_addr = ethereum.utils.privtoaddr(priv)
		eth_addr_hex = binascii.hexlify(eth_addr).decode("utf-8")
		eth_balance = requests.get("https://api.etherscan.io/api?module=account&action=balance&address=0x" + eth_addr_hex + "&tag=latest&apikey=YOURAPIKEYHERE").json()["result"]
		print("ETH balance: {} address: 0x{} privkey: {}".format(float(eth_balance)/100000000, eth_addr_hex, priv))
		time.sleep(1)
	except (AssertionError, IndexError):
	    pass
	except ValueError:
		print (ethbalance)
