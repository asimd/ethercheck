Ethereum and Token Balance Checker
This project provides two Python scripts for checking Ethereum (ETH) and ERC-20 token balances for multiple Ethereum addresses. One script (ethereum_private_key_balance_checker.py) allows checking balances using private keys, and the other (ethereum_address_balance_checker.py) checks balances using Ethereum addresses directly. The scripts use the Web3.py library and Infura's Ethereum node service to interact with the Ethereum blockchain.

Features
Check ETH balance for multiple Ethereum addresses.
Check balances for 100+ popular ERC-20 tokens.
Supports both address-based and private key-based balance checking.
Concurrent processing for faster results.
Proper handling of tokens with different decimal places.
Formatted output for easy readability.
Progress bar to track the balance-checking process.
Results saved to a text file.
Prerequisites
Python 3.7 or higher.
pip (Python package installer).
Setup
Clone this repository or download the scripts.

Install the required Python packages:

bash
Copy code
pip install web3 tqdm
Sign up for a free account at Infura and create a new project to get your Project ID.

Open the script and replace the INFURA_PROJECT_ID value with your Infura Project ID in both scripts:

python
Copy code
INFURA_PROJECT_ID = 'YOUR_INFURA_PROJECT_ID_HERE'
Usage
Script 1: ethereum_private_key_balance_checker.py
This script checks balances for Ethereum addresses using private keys.

Create a text file named ethereum_private_keys.txt in the same directory as the script. Add one Ethereum private key per line in this file.

Run the script:

bash
Copy code
python ethereum_private_key_balance_checker.py
The script will process each private key, checking balances for ETH and all configured ERC-20 tokens.

Progress will be displayed in the console, showing addresses that have balances.

After completion, results will be saved in ethereum_and_token_balances.txt.

Script 2: ethereum_address_balance_checker.py
This script checks balances for Ethereum addresses without needing private keys.

Create a text file named ethereum_addresses.txt in the same directory as the script. Add one Ethereum address per line in this file.

Run the script:

bash
Copy code
python ethereum_address_balance_checker.py
The script will process each address, checking balances for ETH and all configured ERC-20 tokens.

Progress will be displayed in the console, showing addresses that have balances.

After completion, results will be saved in ethereum_balances.txt.

Output
For both scripts, the balance information will be displayed in the console and saved to a text file. The output format is as follows:

yaml
Copy code
Found balances for address: 0x1234...5678
Private Key: 0xabcd...efgh (for private key script)
ETH Balance: 1.2345
USDT Balance: 100.0000
USDC Balance: 50.5000
... (other token balances)
Customization
To add or remove tokens, modify the TOKENS_TO_CHECK dictionary in the scripts.
Adjust the MIN_BALANCE value to change the minimum balance threshold for display.
Modify the TOKEN_DECIMALS dictionary if you need to add or change decimal places for specific tokens.
Security Note
If you are using the ethereum_private_key_balance_checker.py script, be aware that it requires access to private keys. Ensure you are running it in a secure environment and never share your private keys or the resulting output file with untrusted parties.

Disclaimer
These scripts are for educational and personal use only. Use them at your own risk. Always verify important financial information through official sources.