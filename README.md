# Ethereum and Token Balance Checker

This project provides two Python scripts for checking Ethereum (ETH) and ERC-20 token balances for multiple Ethereum addresses. One script (`ethereum_private_key_balance_checker.py`) allows checking balances using private keys, and the other (`ethereum_address_balance_checker.py`) checks balances using Ethereum addresses directly. The scripts use the Web3.py library and Infura's Ethereum node service to interact with the Ethereum blockchain.

## Features

- Check ETH balance for multiple Ethereum addresses
- Check balances for 100+ popular ERC-20 tokens
- Concurrent processing for faster results
- Proper handling of tokens with different decimal places
- Formatted output for easy readability
- Progress bar to track the checking process
- Results saved to a text file

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup

1. Clone this repository or download the script.

2. Install the required Python packages:
   ```
   pip install web3 tqdm
   ```

3. Sign up for a free account at [Infura](https://infura.io/) and create a new project to get your Project ID.

4. Open the script and replace the `INFURA_PROJECT_ID` value with your Infura Project ID:
   ```python
   INFURA_PROJECT_ID = 'YOUR_INFURA_PROJECT_ID_HERE'
   ```

5. Create a text file named `ethereum_private_keys.txt` in the same directory as the script. Add one Ethereum private key per line in this file.

## Usage

Script 1: ethereum_private_key_balance_checker.py

This script checks balances for Ethereum addresses using private keys.

1. Add a private keys to the file named ethereum_private_keys.txt. Add one Ethereum private key per line in this file.

2. Run the script:

bash
python ethereum_private_key_balance_checker.py

3. The script will process each private key, checking balances for ETH and all configured ERC-20 tokens.

4. Progress will be displayed in the console, showing addresses that have balances.

5. After completion, results will be saved in ethereum_and_token_balances.txt.

Script 2: ethereum_address_balance_checker.py

This script checks balances for Ethereum addresses without needing private keys.

1. Add addresses to the file named ethereum_addresses.txt. Add one Ethereum address per line in this file.

2. Run the script:

bash
python ethereum_address_balance_checker.py

3. The script will process each address, checking balances for ETH and all configured ERC-20 tokens.

4. Progress will be displayed in the console, showing addresses that have balances.

5. After completion, results will be saved in ethereum_balances.txt.

## Output

For both scripts, the balance information will be displayed in the console and saved to a text file. The output format is as follows:

```
Found balances for address: 0x1234...5678
Private Key: 0xabcd...efgh
ETH Balance: 1.2345
USDT Balance: 100.0000
USDC Balance: 50.5000
... (other token balances)
```

## Customization

- To add or remove tokens, modify the `TOKENS_TO_CHECK` dictionary in the script.
- Adjust the `MIN_BALANCE` value to change the minimum balance threshold for display.
- Modify the `TOKEN_DECIMALS` dictionary if you need to add or change decimal places for specific tokens.

## Security Note

If you are using the ethereum_private_key_balance_checker.py script, be aware that it requires access to private keys. Ensure you are running it in a secure environment and never share your private keys or the resulting output file with untrusted parties.

## Disclaimer

This script is for educational and personal use only. Use it at your own risk. Always verify important financial information through official sources.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/ethereum-balance-checker/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)