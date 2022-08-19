import datetime
from hashlib import sha256 as hash_function

LEADING_ZEROES = 5
HASH_SIZE_BYTES = 64

class Blockchain:
    
    def __init__(self) -> None:
        self.chain = []
        self.create_block(nonce = 1)

    def create_block(self, nonce: int, data: list = None) -> dict:
        block = {'index': len(self.chain), 
                 'nonce': nonce,
                 'timestamp': datetime.datetime.now(),
                 'data': list.copy(data) if data else [],
                 'previous_hash': self.last_block().get('hash') if len(self.chain) > 0 else ('0' * HASH_SIZE_BYTES)}
        block['hash'] = self.hash_item(block)
        self.chain.append(block)
        return block

    def last_block(self) -> dict:
        return self.chain[-1] if len(self.chain) > 0 else None

    def challenge(self, previous_nonce: int) -> int:
        current = 1
        while True:
            operation = self.hash_item((current ** 2) - (previous_nonce ** 2))
            if operation.startswith('0' * LEADING_ZEROES):
                return current
            current += 1

    def is_proof_valid(self, block: dict, previous_nonce: int) -> bool:
        return self.hash_item((block['nonce'] ** 2) - (previous_nonce ** 2)).startswith('000')

    def hash_item(self, item) -> str:
        return hash_function(str(item).encode()).hexdigest()

    def is_chain_valid(self) -> bool:
        current_index = 0
        prev_nonce = 1
        prev_hash = ('0' * 64)
        for block in self.chain:
            if block.get('index') != current_index:
                return False
            if block.get('previous_hash') != prev_hash:
                return False
            copy = dict.copy(block)
            copy.pop('hash')
            if self.hash_item(copy) != block['hash']:
                return False
            if not self.is_proof_valid(block, prev_nonce) and block['index'] != 0:
                return False
            current_index += 1
            prev_nonce = block['nonce']
            prev_hash = block.get('hash')
        return True