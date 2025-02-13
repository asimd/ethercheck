#!/usr/bin/env python3
import sys
from src.scripts.ethereum_private_key_balance_checker import main as check_private_keys
from src.scripts.ethereum_address_balance_checker import main as check_addresses

def print_menu():
    print("\n🔍 Ethereum Balance Checker")
    print("=" * 50)
    print("1. Check Private Keys")
    print("2. Check Addresses")
    print("3. Exit")
    print("=" * 50)

def main():
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            check_private_keys()
        elif choice == "2":
            check_addresses()
        elif choice == "3":
            print("\nGoodbye! 👋")
            sys.exit(0)
        else:
            print("\n⚠️  Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 