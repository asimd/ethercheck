from web3 import Web3
from eth_utils import to_checksum_address
from ..utils.config import (
    MULTICALL_ADDRESS, MULTICALL_ABI, ERC20_ABI,
    TOKENS_TO_CHECK, TOKEN_DECIMALS, MIN_BALANCE
)

class BalanceChecker:
    def __init__(self, w3):
        self.w3 = w3
        
    def format_balance(self, balance, decimals):
        if balance == 0:
            return None
        
        adjusted_balance = balance / (10 ** decimals)
        
        # Return any non-zero balance
        if adjusted_balance > 0:
            if adjusted_balance < 0.000000001:  # Less than 1 Gwei
                formatted = f"{adjusted_balance:.18f}"
                return formatted
            elif adjusted_balance < 0.00001:
                formatted = f"{adjusted_balance:.12f}"
                return formatted
            elif adjusted_balance < 1:
                formatted = f"{adjusted_balance:.8f}"
                return formatted
            else:
                formatted = f"{adjusted_balance:.6f}"
                return formatted
            
        return None

    def get_all_balances(self, address):
        try:
            multicall = self.w3.eth.contract(address=MULTICALL_ADDRESS, abi=MULTICALL_ABI)
            
            # Fetch ETH balance
            eth_balance = self.w3.eth.get_balance(address)

            calls = []
            tokens = list(TOKENS_TO_CHECK.items())
            
            for token_name, token_address in tokens:
                token_contract = self.w3.eth.contract(
                    address=to_checksum_address(token_address),
                    abi=ERC20_ABI
                )
                call_data = token_contract.functions.balanceOf(address)._encode_transaction_data()
                calls.append((
                    to_checksum_address(token_address),
                    call_data
                ))

            # Execute the multicall to fetch token balances
            _, return_data = multicall.functions.aggregate(calls).call()

            # Process balances
            balances = {}
            
            # Add ETH balance
            eth_formatted = self.format_balance(eth_balance, 18)
            if eth_formatted:
                balances['ETH'] = eth_formatted

            # Process token balances
            for (token_name, _), data in zip(tokens, return_data):
                try:
                    balance = int(data.hex(), 16)
                    if balance > 0:
                        decimals = TOKEN_DECIMALS.get(token_name, 18)
                        formatted_balance = self.format_balance(balance, decimals)
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