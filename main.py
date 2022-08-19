import datetime
from src.FoolsGold import FoolsGoldNode
from flask import Flask, jsonify, request;
from uuid import uuid4 as uuid

app = Flask(__name__)
local_node = FoolsGoldNode()

node_address = str(uuid()).replace('-', '')

@app.route('/MineBlock', methods=['POST'])
def mine_block():
    block = local_node.mine_block()
    return jsonify(block), 201

@app.route('/AddTransaction', methods=['POST'])
def add_transaction():
    data = dict(request.get_json())
    keys = data.keys()
    if 'sender' not in keys or 'receiver' not in keys or 'amount' not in keys:
        return 'Invalid payload!', 400
    transaction = local_node.add_transaction(data)
    return jsonify(transaction), 201

@app.route('/AddNode', methods=['PUT'])
def add_node():
    data = dict(request.get_json())
    if not data.get('address'):
        return 'Invalid payload!', 400
    local_node.add_node(data.get('address'))
    return jsonify({'Message': f'Node {data.get("address")} sucessfuly added'}), 202

@app.route('/GetNodes', methods=['GET'])
def get_nodes():
    return jsonify({'Count': len(local_node.nodes), 'Nodes': tuple(local_node.nodes)}), 200

@app.route('/GetMempool', methods=['GET'])
def get_mempool():
    return jsonify(local_node.mempool), 200

@app.route('/GetChain', methods=['GET'])
def get_blockchain():
    return jsonify(local_node.blockchain.chain), 200

@app.route('/GetChain/<index>', methods=['GET'])
def get_block(index):
    return jsonify(local_node.get_block(int(index))), 200

@app.route('/Status', methods=['GET'])
def is_valid():
    return jsonify({'CurrentSize': local_node.blockchain_size(), 'Timestamp': datetime.datetime.now(), 'ValidState': local_node.blockchain.is_chain_valid()}), 200

@app.route('/UpdateChain', methods=['GET'])
def update_chain():
    if local_node.replace_chain():
        return jsonify({'Message': 'The chain was successfuly updated', 'Size': local_node.blockchain_size()}), 200
    else:
        return jsonify({'Message': 'The chain is already up to date', 'Size': local_node.blockchain_size()}), 200

app.run('localhost', 6666)