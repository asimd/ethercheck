from web3 import Web3
from dotenv import load_dotenv
import json
import os

# Load environment variables
load_dotenv()

# Multicall settings
MULTICALL_ADDRESS = os.getenv('MULTICALL_ADDRESS', '0xeefBa1e63905eF1D7ACbA5a8513c70307C1cE441')
MIN_BALANCE = float(os.getenv('MIN_BALANCE', '0.000000000000001'))  # 1 wei

# ABIs
MULTICALL_ABI = json.loads(os.getenv('MULTICALL_ABI', '''[{
    "constant":false,
    "inputs":[{"components":[{"name":"target","type":"address"},{"name":"callData","type":"bytes"}],"name":"calls","type":"tuple[]"}],
    "name":"aggregate",
    "outputs":[{"name":"blockNumber","type":"uint256"},{"name":"returnData","type":"bytes[]"}],
    "type":"function"
}]'''))

ERC20_ABI = json.loads(os.getenv('ERC20_ABI', '''[{
    "constant":true,
    "inputs":[{"name":"_owner","type":"address"}],
    "name":"balanceOf",
    "outputs":[{"name":"balance","type":"uint256"}],
    "type":"function"
}]'''))

# Token configurations
TOKENS_TO_CHECK = {
    'USDT': os.getenv('USDT_ADDRESS', '0xdAC17F958D2ee523a2206206994597C13D831ec7'),
    'USDC': os.getenv('USDC_ADDRESS', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'),
    'BNB': os.getenv('BNB_ADDRESS', '0xB8c77482e45F1F44dE1745F52C74426C631bDD52'),
    'BUSD': os.getenv('BUSD_ADDRESS', '0x4Fabb145d64652a948d72533023f6E7A623C7C53'),
    'LINK': os.getenv('LINK_ADDRESS', '0x514910771AF9Ca656af840dff83E8264EcF986CA'),
    'MATIC': os.getenv('MATIC_ADDRESS', '0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0'),
    'UNI': os.getenv('UNI_ADDRESS', '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'),
    'WBTC': os.getenv('WBTC_ADDRESS', '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'),
    'DAI': os.getenv('DAI_ADDRESS', '0x6B175474E89094C44Da98b954EedeAC495271d0F'),
    'SHIB': os.getenv('SHIB_ADDRESS', '0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE')
}

TOKEN_DECIMALS = {
    'USDT': int(os.getenv('USDT_DECIMALS', '6')),
    'USDC': int(os.getenv('USDC_DECIMALS', '6')),
    'BNB': int(os.getenv('BNB_DECIMALS', '18')),
    'BUSD': int(os.getenv('BUSD_DECIMALS', '18')),
    'LINK': int(os.getenv('LINK_DECIMALS', '18')),
    'MATIC': int(os.getenv('MATIC_DECIMALS', '18')),
    'UNI': int(os.getenv('UNI_DECIMALS', '18')),
    'WBTC': int(os.getenv('WBTC_DECIMALS', '8')),
    'DAI': int(os.getenv('DAI_DECIMALS', '18')),
    'SHIB': int(os.getenv('SHIB_DECIMALS', '18'))
} 