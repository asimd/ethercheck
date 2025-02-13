import os
import sys
from ..utils.helpers import ensure_data_directory

class OutputFormatter:
    @staticmethod
    def display_results(results, include_private_key=False):
        print("\n🎉 Found balances:")
        print("=" * 80)
        
        for result in results:
            if include_private_key:
                addr, balances, priv = result
                print(f"\n📍 Address: {addr} | Private Key: {priv}")
            else:
                addr, balances = result
                print(f"\n📍 Address: {addr}")
            
            # Display ETH balance first if it exists
            if 'ETH' in balances:
                print(f"  • ETH: {balances['ETH']} ETH")
            
            # Display other token balances
            for token, amount in balances.items():
                if token != 'ETH':
                    print(f"  • {token}: {amount} {token}")
            
            print("-" * 80)

        print(f"\n✨ Total addresses with balances: {len(results)}")
        print(f"💾 Results saved to: {OutputFormatter.get_output_filename(include_private_key)}")

    @staticmethod
    def save_results_to_txt(results, include_private_key=False):
        filename = OutputFormatter.get_output_filename(include_private_key)
        with open(filename, 'w') as txtfile:
            for result in results:
                if include_private_key:
                    addr, balances, priv = result
                    txtfile.write(f"Address: {addr} | Private Key: {priv}\n")
                else:
                    addr, balances = result
                    txtfile.write(f"Address: {addr}\n")
                
                if 'ETH' in balances:
                    txtfile.write(f"ETH: {balances['ETH']} ETH\n")
                
                for token, amount in balances.items():
                    if token != 'ETH':
                        txtfile.write(f"{token}: {amount} {token}\n")
                txtfile.write("-" * 80 + "\n")

    @staticmethod
    def get_output_filename(include_private_key):
        ensure_data_directory()  # Make sure data directory exists
        return 'data/ethereum_and_token_balances.txt' if include_private_key else 'data/ethereum_address_balance.txt' 