#!/usr/bin/env python3
import re
from web3 import Web3
from eth_account import Account
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import sys
import os
import warnings
from urllib3.exceptions import InsecureRequestWarning
from dotenv import load_dotenv
from eth_utils import to_checksum_address

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.web3_manager import Web3Manager
from src.core.balance_checker import BalanceChecker
from src.core.output_formatter import OutputFormatter
from src.utils.helpers import ensure_data_directory, validate_private_keys_file
from src.utils.exceptions import ConfigurationError
from src.utils.config import (
    MULTICALL_ADDRESS, MULTICALL_ABI, ERC20_ABI,
    TOKENS_TO_CHECK, TOKEN_DECIMALS, MIN_BALANCE
)

# Suppress SSL warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

# Load environment variables
load_dotenv()

# Global variables for Web3 instances
w3_instances = []
current_w3_index = 0
rate_limited_endpoints = set()
terminate_script = False

# Global set to keep track of processed keys
processed_keys = set()

def remove_processed_keys_from_file(filename):
    global processed_keys
    processed_count = len(processed_keys)
    processed_keys.clear()
    print(f"Found {processed_count} addresses with balances")

def is_valid_private_key(key):
    return bool(re.fullmatch(r'[a-fA-F0-9]{64}', key))

def process_key(key, w3_manager, balance_checker):
    try:
        if not is_valid_private_key(key):
            return None
            
        account = Account.from_key(key)
        address = account.address
        
        balances = balance_checker.get_all_balances(address)
        
        # Only return if balances is not None and not empty
        if balances and len(balances) > 0:
            processed_keys.add(key)
            return (address, balances, key)
            
    except Exception as e:
        print(f"Error processing key: {e}")
    return None

def main():
    try:
        w3_manager = Web3Manager()
        w3_manager.initialize_web3_instances()
        
        private_keys = validate_private_keys_file()
        balance_checker = BalanceChecker(w3_manager.get_next_w3())
        
        print(f"\nChecking {len(private_keys)} private keys...")
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(process_key, key, w3_manager, balance_checker) 
                for key in private_keys
            ]
            
            with tqdm(total=len(private_keys), desc="Checking keys", unit="key") as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
                    pbar.update(1)
                    if terminate_script:
                        break
        
        if results:
            OutputFormatter.save_results_to_txt(results, include_private_key=True)
            OutputFormatter.display_results(results, include_private_key=True)
        else:
            print("\n🔍 No addresses with balances found.")

    except ConfigurationError as e:
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()