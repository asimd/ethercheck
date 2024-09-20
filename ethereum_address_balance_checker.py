#!/usr/bin/env python3
from web3 import Web3
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import sys
import json

# Infura Project ID
INFURA_PROJECT_ID = 'YOUR_INFURA_PROJECT_ID_HERE'
INFURA_URL = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'

# Initialize Web3 with Infura endpoint
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Multicall contract address (Ethereum mainnet)
MULTICALL_ADDRESS = '0xeefBa1e63905eF1D7ACbA5a8513c70307C1cE441'

# Multicall ABI
MULTICALL_ABI = json.loads('[{"constant":false,"inputs":[{"components":[{"name":"target","type":"address"},{"name":"callData","type":"bytes"}],"name":"calls","type":"tuple[]"}],"name":"aggregate","outputs":[{"name":"blockNumber","type":"uint256"},{"name":"returnData","type":"bytes[]"}],"type":"function"}]')

# ERC-20 ABI for balanceOf function
ERC20_ABI = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]')

TOKEN_DECIMALS = {
    'USDT': 6,
    'USDC': 6,
    'BNB': 18,
    'BUSD': 18,
    'SHIB': 18,
    'BAT': 18,
    'HOT': 18,
    'SNX': 18,
    '1INCH': 18,
    'BNT': 18,
}

# List of top 100 tokens to check
TOKENS_TO_CHECK = {
    'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'BNB': '0xB8c77482e45F1F44dE1745F52C74426C631bDD52',
    'BUSD': '0x4Fabb145d64652a948d72533023f6E7A623C7C53',
    'LINK': '0x514910771AF9Ca656af840dff83E8264EcF986CA',
    'MATIC': '0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0',
    'UNI': '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984',
    'WBTC': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
    'DAI': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
    'SHIB': '0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE',
}

def format_balance(balance, decimals):
    if balance == 0:
        return None
    adjusted_balance = balance / (10 ** decimals)
    if adjusted_balance < 0.00001:
        return f"{adjusted_balance:.8f}"
    elif adjusted_balance < 1:
        return f"{adjusted_balance:.6f}"
    else:
        return f"{adjusted_balance:.4f}"

def get_all_balances(address):
    multicall = w3.eth.contract(address=MULTICALL_ADDRESS, abi=MULTICALL_ABI)
    erc20_contract = w3.eth.contract(abi=ERC20_ABI)

    calls = []
    tokens = list(TOKENS_TO_CHECK.items())
    
    for _, token_address in tokens:
        calls.append((
            Web3.to_checksum_address(token_address),
            erc20_contract.encodeABI("balanceOf", [address])
        ))

    try:
        # Get ETH balance separately
        eth_balance = w3.eth.get_balance(address)
        
        # Get token balances
        _, return_data = multicall.functions.aggregate(calls).call()

        balances = {}
        
        # Add ETH balance
        eth_formatted = format_balance(eth_balance, 18)
        if eth_formatted:
            balances['ETH'] = eth_formatted

        # Process token balances
        for (token_name, _), data in zip(tokens, return_data):
            try:
                balance = int(data.hex(), 16)
                if balance > 0:
                    decimals = TOKEN_DECIMALS.get(token_name, 18)
                    formatted_balance = format_balance(balance, decimals)
                    if formatted_balance:
                        balances[token_name] = formatted_balance
            except ValueError as ve:
                print(f"Error parsing balance for {token_name}: {ve}")
            except Exception as e:
                print(f"Unexpected error for {token_name}: {e}")

        return balances
    except Exception as e:
        print(f"Error getting balances for {address}: {e}")
        return None

def process_address(address):
    try:
        # Ensure the address is in checksum format
        checksum_address = Web3.to_checksum_address(address)
        balances = get_all_balances(checksum_address)
        
        # Only return addresses with any balances
        if balances and any(balances.values()):
            return (checksum_address, balances)
    except Exception as e:
        print(f"Error processing address: {e}")
    return None

def save_results_to_txt(results, filename='data/ethereum_address_balance.txt'):
    with open(filename, 'w') as txtfile:
        for addr, balances in results:
            txtfile.write(f"Address: {addr}\n")
            for token, balance in balances.items():
                txtfile.write(f"{token} Balance: {balance}\n")
            txtfile.write("\n")
    print(f"\nResults saved to {filename}")

def main():
    # Read Ethereum addresses from file
    with open('data/ethereum_addresses.txt', 'r') as file:
        addresses = [line.strip() for line in file if line.strip()]

    results = []
    total_addresses = len(addresses)

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_address, addr) for addr in addresses]
        
        with tqdm(total=total_addresses, desc="Checking addresses", unit="address") as pbar:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    addr, balances = result
                    results.append(result)
                    print(f"\nFound balances for address: {addr}")
                    for token, balance in balances.items():
                        print(f"{token} Balance: {balance}")
                pbar.update(1)
                sys.stdout.flush()  # Ensure output is immediately displayed

    # Save results to TXT
    if results:
        save_results_to_txt(results)
    else:
        print("\nNo addresses with balance found.")

if __name__ == "__main__":
    main()