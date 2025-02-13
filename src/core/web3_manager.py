from web3 import Web3
import os
import re
from ..utils.exceptions import ConfigurationError

class Web3Manager:
    def __init__(self):
        self.w3_instances = []
        self.current_index = 0
        
    def is_valid_infura_id(self, infura_id):
        """Check if the ID is not a placeholder"""
        # Skip if it matches pattern 'id1', 'id2', etc.
        if re.match(r'^id\d+$', infura_id):
            return False
        # Skip if shorter than 32 chars (Infura Project IDs are 32+ chars)
        if len(infura_id) < 32:
            return False
        return True
        
    def initialize_web3_instances(self):
        """Initialize multiple Web3 instances from Infura Project IDs"""
        infura_ids = os.getenv('INFURA_PROJECT_IDS', '').split(',')
        infura_ids = [id.strip() for id in infura_ids if id.strip() and self.is_valid_infura_id(id.strip())]
        
        if not infura_ids:
            raise ConfigurationError(
                "\n⚠️  ERROR: No valid Infura Project IDs configured!\n"
                "Please add your Infura Project IDs to the .env file:\n"
                "1. Create a .env file in the project root\n"
                "2. Add your Infura Project IDs as:\n"
                "   INFURA_PROJECT_IDS=your_id1,your_id2,your_id3\n"
                "3. Make sure the .env file is in the same directory as this script\n\n"
                "Current values are invalid or empty."
            )
        
        for infura_id in infura_ids:
            infura_url = f'https://mainnet.infura.io/v3/{infura_id}'
            w3 = Web3(Web3.HTTPProvider(
                infura_url,
                request_kwargs={'timeout': 30, 'verify': False}
            ))
            
            try:
                w3.eth.block_number
                self.w3_instances.append(w3)
            except Exception as e:
                print(f"Warning: Could not initialize Web3 with ID {infura_id[:8]}...{infura_id[-4:]}: {e}")
        
        if not self.w3_instances:
            raise ConfigurationError(
                "\n⚠️  ERROR: Could not connect to any Infura endpoints.\n"
                "Please check your Project IDs and internet connection."
            )
    
    def get_next_w3(self):
        """Get next available Web3 instance using round-robin"""
        if not self.w3_instances:
            raise ConfigurationError("No Web3 instances available")
        
        w3 = self.w3_instances[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.w3_instances)
        return w3 