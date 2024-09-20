#!/usr/bin/env python3
from web3 import Web3
from eth_account import Account
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import sys
import json

# Infura Project ID
INFURA_PROJECT_ID = '9071bae74ae946d5854cca16d3932705'
INFURA_URL = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'

# Initialize Web3 with Infura endpoint
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Minimum balance threshold (in Ether or tokens)
MIN_BALANCE = 0.01

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
    'AAVE': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9',
    'CRO': '0xA0b73E1Ff0B80914AB6fe0444E65848C4C34450b',
    'LEO': '0x2AF5D2aD76741191D15Dfe7bF6aC92d4Bd912Ca3',
    'FTT': '0x50D1c9771902476076eCFc8B2A83Ad6b9355a4c9',
    'THETA': '0x3883f5e181fccaF8410FA61e12b59BAd963fb645',
    'OKB': '0x75231F58b43240C9718Dd58B4967c5114342a86c',
    'ATOM': '0x8D983cb9388EaC77af0474fA441C4815500Cb7BB',
    'HT': '0x6f259637dcD74C767781E37Bc6133cd6A68aa161',
    'TUSD': '0x0000000000085d4780B73119b644AE5ecd22b376',
    'APE': '0x4d224452801ACEd8B2F0aebE155379bb5D594381',
    'VET': '0xD850942eF8811f2A866692A623011bDE52a462C1',
    'MKR': '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2',
    'FTM': '0x4E15361FD6b4BB609Fa63C81A2be19d873717870',
    'GRT': '0xc944E90C64B2c07662A292be6244BDf05Cda44a7',
    'SAND': '0x3845badAde8e6dFF049820680d1F14bD3903a5d0',
    'MANA': '0x0F5D2fB29fb7d3CFeE444a200298f468908cC942',
    'HBAR': '0x66a0f676479Cee1d7373f3DC2e2952778BfF5bd6',
    'AXS': '0xBB0E17EF65F82Ab018d8EDd776e8DD940327B28b',
    'CHZ': '0x3506424F91fD33084466F402d5D97f05F8e3b4AF',
    'FLOW': '0x5C147E74D63B1D31AA3Fd78Eb229B65161983B2b',
    'QNT': '0x4a220E6096B25EADb88358cb44068A3248254675',
    'KCS': '0xf34960d9d60be18cC1D5Afc1A6F012A723a28811',
    'ZIL': '0x05f4a42e251f2d52b8ed15E9FEdAacFcEF1FAD27',
    'BAT': '0x0D8775F648430679A709E98d2b0Cb6250d2887EF',
    'AMP': '0xfF20817765cB7f73d4bde2e66e067E58D11095C2',
    'ENJ': '0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c',
    'COMP': '0xc00e94Cb662C3520282E6f5717214004A7f26888',
    'NEXO': '0xB62132e35a6c13ee1EE0f84dC5d40bad8d815206',
    'HOT': '0x6c6EE5e31d828De241282B9606C8e98Ea48526E2',
    'CELO': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'SNX': '0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F',
    'LRC': '0xBBbbCA6A901c926F240b89EacB641d8Aec7AEafD',
    'YFI': '0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e',
    'QTUM': '0x9a642d6b3368ddc662CA244bAdf32cDA716005BC',
    'KNC': '0xdd974D5C2e2928deA5F71b9825b8b646686BD200',
    'CRV': '0xD533a949740bb3306d119CC777fa900bA034cd52',
    'OMG': '0xd26114cd6EE289AccF82350c8d8487fedB8A0C07',
    '1INCH': '0x111111111117dC0aa78b770fA6A738034120C302',
    'ANKR': '0x8290333ceF9e6D528dD5618Fb97a76f268f3EDD4',
    'SUSHI': '0x6B3595068778DD592e39A122f4f5a5cF09C90fE2',
    'REN': '0x408e41876cCCDC0F92210600ef50372656052a38',
    'ZRX': '0xE41d2489571d322189246DaFA5ebDe1F4699F498',
    'BNT': '0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C',
    'IOTX': '0x6fB3e0A217407EFFf7Ca062D46c26E5d60a14d69',
    'FET': '0xaea46A60368A7bD060eec7DF8CBa43b7EF41Ad85',
    'OCEAN': '0x967da4048cD07aB37855c090aAF366e4ce1b9F48',
    'ALPHA': '0xa1faa113cbE53436Df28FF0aEe54275c13B40975',
    'UMA': '0x04Fa0d235C4abf4BcF4787aF4CF447DE572eF828',
    'POLY': '0x9992eC3cF6A55b00978cdDF2b27BC6882d88D1eC',
    'DODO': '0x43Dfc4159D86F3A37A5A4B3D4580b888ad7d4DDd',
    'BAND': '0xBA11D00c5f74255f56a5E366F4F77f5A186d7f55',
    'SXP': '0x8CE9137d39326AD0cD6491fb5CC0CbA0e089b6A9',
    'RSR': '0x8762db106B2c2A0bccB3A80d1Ed41273552616E8',
    'NMR': '0x1776e1F26f98b1A5dF9cD347953a26dd3Cb46671',
    'STORJ': '0xB64ef51C888972c908CFacf59B47C1AfBC0Ab8aC',
    'AKNC': '0x7D2D3688Df45Ce7C552E19c27e007673da9204B8',
    'AAVE': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9',
    'RLC': '0x607F4C5BB672230e8672085532f7e901544a7375',
    'BAL': '0xba100000625a3754423978a60c9317c58a424e3D',
    'RLY': '0xf1f955016EcbCd7321c7266BccFB96c68ea5E49b',
    'RARI': '0xFca59Cd816aB1eaD66534D82bc21E7515cE441CF',
    'WNXM': '0x0d438F3b5175Bebc262bF23753C1E53d03432bDE',
    'DNT': '0x0AbdAce70D3790235af448C88547603b945604ea',
    'CREAM': '0x2ba592F78dB6436527729929AAf6c908497cB200',
    'FARM': '0xa0246c9032bC3A600820415aE600c6388619A14D',
    'STAKE': '0x0Ae055097C6d159879521C384F1D2123D1f195e6',
    'GHST': '0x3F382DbD960E3a9bbCeaE22651E88158d2791550',
    'AUDIO': '0x18aAA7115705e8be94bfFEBDE57Af9BFc265B998',
    'PERP': '0xbC396689893D065F41bc2C6EcbeE5e0085233447',
    'KP3R': '0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44',
    'BOND': '0x0391D2021f89DC339F60Fff84546EA23E337750f',
    'PICKLE': '0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
    'CVP': '0x38e4adB44ef08F22F5B5b76A8f0c2d0dCbE7DcA1',
    'ROOK': '0xfA5047c9c78B8877af97BDcb85Db743fD7313d4a',
    'DEXTF': '0x5F64Ab1544D28732F0A24F4713c2C8ec0dA089f0',
    'DOUGH': '0xad32A8e6220741182940c5aBF610bDE99E737b2D',
    'HEGIC': '0x584bC13c7D411c00c01A62e8019472dE68768430',
    'WISE': '0x66a0f676479Cee1d7373f3DC2e2952778BfF5bd6',
    'API3': '0x0b38210ea11411557c13457D4dA7dC6ea731B88a',
    'IDLE': '0x875773784Af8135eA0ef43b5a374AaD105c5D39e',
    'SAKE': '0x066798d9ef0833ccc719076Dab77199eCbd178b0',
    'RING': '0x9469D013805bFfB7D3DEBe5E7839237e535ec483',
    'NFTX': '0x87d73E916D7057945c9BcD8cdd94e42A6F47f776',
    'CORE': '0x62359Ed7505Efc61FF1D56fEF82158CcaffA23D7',
    'DPI': '0x1494CA1F11D487c2bBe4543E90080AeBa4BA3C2b',
    'FRAX': '0x853d955aCEf822Db058eb8505911ED77F175b99e',
    'FXS': '0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0'
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
    multicall = w3.eth.contract(address=MULTICALL_ADDRESS, abi=MULTICALL_ABI)
    erc20_contract = w3.eth.contract(abi=ERC20_ABI)

    calls = []
    tokens = list(TOKENS_TO_CHECK.items())
    
    for _, token_address in tokens:
        calls.append((
            Web3.to_checksum_address(token_address),
            erc20_contract.encodeABI("balanceOf", [address])
        ))

    try:
        # Get ETH balance separately
        eth_balance = w3.eth.get_balance(address)
        
        # Get token balances
        _, return_data = multicall.functions.aggregate(calls).call()

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

def process_key(priv):
    try:
        account = Account.from_key(priv)
        eth_addr = account.address
        balances = get_all_balances(eth_addr)
        
        if balances:
            return (eth_addr, balances, priv)
    except Exception as e:
        print(f"Error processing key: {e}")
    return None

def save_results_to_txt(results, filename='data/ethereum_and_token_balances.txt'):
    with open(filename, 'w') as txtfile:
        for addr, balances, priv in results:
            txtfile.write(f"Address: {addr}\n")
            txtfile.write(f"Private Key: {priv}\n")
            for token, balance in balances.items():
                txtfile.write(f"{token} Balance: {balance}\n")
            txtfile.write("\n")
    print(f"\nResults saved to {filename}")

def main():
    # Read private keys from file
    with open('data/ethereum_private_keys.txt', 'r') as file:
        private_keys = [line.strip() for line in file if line.strip()]

    results = []
    total_keys = len(private_keys)

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_key, priv) for priv in private_keys]
        
        with tqdm(total=total_keys, desc="Checking keys", unit="key") as pbar:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    addr, balances, priv = result
                    results.append(result)
                    print(f"\nFound balances for address: {addr}")
                    print(f"Private Key: {priv}")
                    for token, balance in balances.items():
                        print(f"{token} Balance: {balance}")
                pbar.update(1)
                sys.stdout.flush()  # Ensure output is immediately displayed

    # Save results to TXT
    if results:
        save_results_to_txt(results)
    else:
        print("\nNo addresses with balance found.")

if __name__ == "__main__":
    main()