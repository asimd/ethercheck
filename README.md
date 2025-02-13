# Ethereum Balance Checker Scripts

A set of Python scripts to check ETH and ERC-20 token balances for Ethereum addresses and private keys.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Web3.py](https://img.shields.io/badge/web3.py-latest-green)

## 🚀 Features

- Check ETH balance for multiple addresses/private keys
- Check balances for 100+ popular ERC-20 tokens
- Detects even tiny dust amounts of ETH (down to 1 wei)
- Concurrent processing for faster results
- Progress bar to track checking process
- Formatted output for easy readability
- Results saved to text files
- Non-destructive operation (keeps input files intact)

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🛠️ Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/asimd/ethercheck.git
   cd ethercheck
   ```

2. Install required packages:
   ```bash
   pip3 install web3 tqdm python-dotenv
   ```

3. Create your environment file:
   ```bash
   cp .env.example .env
   ```

4. Add your Infura Project IDs to `.env`:
   ```
   INFURA_PROJECT_IDS=your_project_id_1,your_project_id_2,your_project_id_3
   ```
   Note: Multiple IDs are recommended to handle rate limiting

5. Create input files in the `data` directory if they don't exist:
   - For addresses: `data/ethereum_addresses.txt`
   - For private keys: `data/ethereum_private_keys.txt`

## 💻 Usage

### Run the interactive menu:
   ```bash
   python3 main.py
   ```

### Choose from the following options:

1. Check Private Keys
2. Check Addresses
3. Exit

## 📝 Input Files Format
### Private Keys (data/ethereum_private_keys.txt):
One private key per line (64 hex characters)
0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

### Addresses (data/ethereum_addresses.txt):
One address per line
0x123456789abcdef0123456789abcdef0123456789abcdef

## 📝 Output Format

Results are displayed in the console and saved to text files:
- Address checker: `data/ethereum_address_balance.txt`
- Private key checker: `data/ethereum_and_token_balances.txt`

The script will detect and display:
- Any non-zero ETH balance (even dust amounts)
- Any ERC-20 token balances
- Formatted amounts based on balance size:
  - < 1 Gwei: 18 decimal places
  - < 0.00001 ETH: 12 decimal places
  - < 1 ETH: 8 decimal places
  - ≥ 1 ETH: 6 decimal places

## ⚙️ Customization

You can customize the script behavior by modifying these variables:

- `TOKENS_TO_CHECK`: Add or remove ERC-20 tokens to check
- `TOKEN_DECIMALS`: Modify decimal places for specific tokens

## 🔒 Security Considerations

- Never share your private keys
- Use this tool in a secure environment
- Verify addresses and balances independently
- Keep your .env file secure and never commit it to version control

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