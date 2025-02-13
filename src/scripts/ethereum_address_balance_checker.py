#!/usr/bin/env python3
import sys
import os
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning
from eth_utils import to_checksum_address

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.web3_manager import Web3Manager
from src.core.balance_checker import BalanceChecker
from src.core.output_formatter import OutputFormatter
from src.utils.helpers import ensure_data_directory, validate_addresses_file
from src.utils.exceptions import ConfigurationError

# Suppress SSL warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

def process_address(address, w3_manager, balance_checker):
    try:
        checksum_address = to_checksum_address(address)
        balances = balance_checker.get_all_balances(checksum_address)
        
        if balances and any(balances.values()):
            return (checksum_address, balances)
    except Exception as e:
        print(f"Error processing address: {e}")
    return None

def main():
    try:
        w3_manager = Web3Manager()
        w3_manager.initialize_web3_instances()
        
        addresses = validate_addresses_file()
        balance_checker = BalanceChecker(w3_manager.get_next_w3())
        
        print(f"\nChecking {len(addresses)} addresses...")
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(process_address, addr, w3_manager, balance_checker) 
                for addr in addresses
            ]
            
            with tqdm(total=len(addresses), desc="Checking addresses", unit="addr") as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
                    pbar.update(1)
        
        if results:
            OutputFormatter.save_results_to_txt(results)
            OutputFormatter.display_results(results)
        else:
            print("\n🔍 No addresses with balances found.")

    except ConfigurationError as e:
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()