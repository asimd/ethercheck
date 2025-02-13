import os
import sys

def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    os.makedirs('data', exist_ok=True)

def validate_private_keys_file():
    """Validate and create private keys input file if it doesn't exist"""
    input_file = 'data/ethereum_private_keys.txt'
    ensure_data_directory()
    
    if not os.path.exists(input_file):
        with open(input_file, 'w') as f:
            f.write("# Add your Ethereum private keys here (one per line)\n")
            f.write("# Example:\n")
            f.write("# 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef\n")
        print(f"\n⚠️  Created {input_file}")
        print("Please add your Ethereum private keys to this file and run the script again.")
        sys.exit(1)
    
    with open(input_file, 'r') as f:
        keys = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not keys:
        print(f"\n⚠️  No private keys found in {input_file}")
        print("Please add your Ethereum private keys to this file and run the script again.")
        sys.exit(1)
    
    return keys

def validate_addresses_file():
    """Validate and create addresses input file if it doesn't exist"""
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