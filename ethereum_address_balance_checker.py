#!/usr/bin/env python3
from web3 import Web3
from eth_utils import to_checksum_address  # Add this import
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import sys
import json
import os
import warnings
from urllib3.exceptions import InsecureRequestWarning
from dotenv import load_dotenv

# Suppress SSL warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

# Load environment variables
load_dotenv()

class ConfigurationError(Exception):
    """Raised when there's a configuration issue with the script"""
    pass

# Get Infura Project ID from environment
INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID', '')

def validate_configuration():
    if not INFURA_PROJECT_ID or INFURA_PROJECT_ID in ['', 'your_infura_id_here', 'YOUR_INFURA_PROJECT_ID_HERE']:
        raise ConfigurationError(
            "\n⚠️  ERROR: No valid Infura Project ID configured!\n"
            "Please add your Infura Project ID to the .env file:\n"
            "1. Create a .env file in the project root\n"
            "2. Add your Infura Project ID as: INFURA_PROJECT_ID=your_id_here\n"
            "3. Make sure the .env file is in the same directory as this script\n"
            "\nCurrent value is invalid or empty."
        )

class EthereumChecker:
    def __init__(self):
        self.w3 = None
        
    def initialize_web3(self):
        """Initialize Web3 connection after configuration is validated"""
        infura_url = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'
        self.w3 = Web3(Web3.HTTPProvider(
            infura_url,
            request_kwargs={
                'verify': False,
                'timeout': 30,
            }
        ))
        
        # Test connection
        try:
            self.w3.eth.block_number
        except Exception as e:
            raise ConfigurationError(
                "\n⚠️  ERROR: Could not connect to Infura endpoint.\n"
                f"Error details: {str(e)}\n"
                "Please check your Project ID and internet connection."
            )

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
    try:
        multicall = w3.eth.contract(address=MULTICALL_ADDRESS, abi=MULTICALL_ABI)
        
        # Fetch ETH balance
        eth_balance = w3.eth.get_balance(address)

        calls = []
        tokens = list(TOKENS_TO_CHECK.items())
        
        for token_name, token_address in tokens:
            token_contract = w3.eth.contract(
                address=to_checksum_address(token_address),
                abi=ERC20_ABI
            )
            call_data = token_contract.functions.balanceOf(address)._encode_transaction_data()
            calls.append((
                to_checksum_address(token_address),
                call_data
            ))

        # Execute the multicall to fetch token balances
        _, return_data = multicall.functions.aggregate(calls).call()

        # Process balances
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
        # Use the imported to_checksum_address function
        checksum_address = to_checksum_address(address)
        balances = get_all_balances(checksum_address)
        
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

def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    os.makedirs('data', exist_ok=True)

def validate_input_file():
    """Validate and create input file if it doesn't exist"""
    input_file = 'data/ethereum_addresses.txt'
    ensure_data_directory()
    
    if not os.path.exists(input_file):
        with open(input_file, 'w') as f:
            f.write("# Add your Ethereum addresses here (one per line)\n")
            f.write("# Example:\n")
            f.write("# 0x742d35Cc6634C0532925a3b844Bc454e4438f44e\n")
        print(f"\n⚠️  Created {input_file}")
        print("Please add your Ethereum addresses to this file and run the script again.")
        sys.exit(1)
    
    with open(input_file, 'r') as f:
        addresses = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not addresses:
        print(f"\n⚠️  No addresses found in {input_file}")
        print("Please add your Ethereum addresses to this file and run the script again.")
        sys.exit(1)
    
    return addresses

def main():
    try:
        # First validate configuration
        validate_configuration()
        
        # Then initialize Web3
        checker = EthereumChecker()
        checker.initialize_web3()
        
        # Continue with address checking
        addresses = validate_input_file()
        print(f"Checking {len(addresses)} addresses...")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_address, addr) for addr in addresses]
            
            results = []
            with tqdm(total=len(addresses), desc="Checking addresses", unit="address") as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
                    pbar.update(1)
        
        if results:
            save_results_to_txt(results)
        else:
            print("\nNo addresses with balance found.")

    except ConfigurationError as e:
        print(str(e))
        sys.exit(1)

if __name__ == '__main__':
    main()