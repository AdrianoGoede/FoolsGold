import requests
from urllib.parse import urlparse
from src.blockchain import Blockchain

class FoolsGoldNode:

    def __init__(self, host) -> None:
        self.address = host
        self.mempool = []
        self.blockchain = Blockchain()
        self.nodes = set()

    def blockchain_size(self) -> int:
        return len(self.blockchain.chain)

    def get_block(self, index: int) -> dict:
        return self.blockchain.chain[index] if self.blockchain_size() >= (index + 1) else dict()

    def add_transaction(self, data: dict) -> dict:
        self.mempool.append({'Sender': data['sender'], 'Receiver': data['receiver'], 'Amount': data['amount']})
        return self.mempool[-1] if len(self.mempool) > 0 else dict()

    def mine_block(self) -> dict:
        self.replace_chain()
        previous_nonce = self.blockchain.last_block()['nonce']
        proof = self.blockchain.challenge(previous_nonce)
        block = self.blockchain.create_block(proof, self.mempool)
        self.mempool.clear()
        return block

    def add_node(self, address) -> None:
        parsed_address = urlparse(address)
        if parsed_address.netloc == self.address or parsed_address.netloc in self.nodes:
            return
        self.nodes.add(parsed_address.netloc)
        for node in (addr for addr in self.nodes if addr != parsed_address.netloc):
            requests.put(f'http://{node}/AddNode', ('{"address":"' + address + '"}'), headers={'Content-Type': 'application/json'})
        
    def replace_chain(self) -> bool:
        was_replaced = False
        for node in self.nodes:
            response = requests.get(f'http://{node}/GetChain')
            if response.status_code == 200:
                fetched_chain = response.json()
                if len(fetched_chain) > len(self.blockchain.chain):
                    self.blockchain.chain = fetched_chain
                    was_replaced = True
        return was_replaced