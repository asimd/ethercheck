# 🔍 Ethereum Balance Checker

A powerful Python-based tool for checking Ethereum (ETH) and ERC-20 token balances across multiple addresses. This project provides two distinct scripts for different use cases - one for checking balances using private keys and another using Ethereum addresses directly.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Web3.py](https://img.shields.io/badge/web3.py-latest-green)

## ✨ Features

- 💰 Check ETH balance for multiple Ethereum addresses
- 🪙 Support for 100+ popular ERC-20 tokens
- ⚡ Concurrent processing for lightning-fast results
- 🎯 Precise handling of tokens with different decimal places
- 📊 Clean, formatted output for easy readability
- 📈 Real-time progress tracking
- 💾 Automatic results saving to file

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- An Infura account (free)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ethereum-balance-checker.git
   cd ethereum-balance-checker
   ```

2. Install required packages:
   ```bash
   pip install web3 tqdm
   ```

3. Set up your Infura credentials:
   - Sign up for a free account at [Infura](https://infura.io/)
   - Create a new project and copy your Project ID
   - Replace `INFURA_PROJECT_ID` in the script with your Project ID:
     ```python
     INFURA_PROJECT_ID = 'YOUR_INFURA_PROJECT_ID_HERE'
     ```

## 📚 Usage

### Script 1: Private Key Balance Checker

1. Create a text file named `ethereum_private_keys.txt` and add your private keys (one per line)
2. Run the script:
   ```bash
   python ethereum_private_key_balance_checker.py
   ```
3. Results will be saved in `ethereum_and_token_balances.txt`

### Script 2: Address Balance Checker

1. Create a text file named `ethereum_addresses.txt` and add your Ethereum addresses (one per line)
2. Run the script:
   ```bash
   python ethereum_address_balance_checker.py
   ```
3. Results will be saved in `ethereum_balances.txt`

## 📝 Output Format

The balance information is displayed in the console and saved to a text file in the following format:

```
Found balances for address: 0x1234...5678
Private Key: 0xabcd...efgh
ETH Balance: 1.2345
USDT Balance: 100.0000
USDC Balance: 50.5000
... (other token balances)
```

## ⚙️ Customization

You can customize the script behavior by modifying these variables:

- `TOKENS_TO_CHECK`: Add or remove ERC-20 tokens to check
- `MIN_BALANCE`: Adjust the minimum balance threshold for display
- `TOKEN_DECIMALS`: Modify decimal places for specific tokens

```python
TOKENS_TO_CHECK = {
    'USDT': '0xdac17f958d2ee523a2206206994597c13d831ec7',
    'USDC': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    # Add more tokens here
}
```

## 🔒 Security Considerations

- When using `ethereum_private_key_balance_checker.py`, ensure you're in a secure environment
- Never share your private keys or the resulting output files
- Keep your Infura Project ID confidential
- Consider using a hardware wallet for additional security

## ⚠️ Disclaimer

This tool is for educational and personal use only. Always verify important financial information through official sources. Use at your own risk.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Web3.py](https://web3py.readthedocs.io/) for Ethereum interaction
- [tqdm](https://github.com/tqdm/tqdm) for progress bars
- The Ethereum community for inspiration

## 📬 Contact

If you have any questions or suggestions, feel free to open an issue or reach out to the maintainers.

---
⭐ Found this project helpful? Give it a star!
