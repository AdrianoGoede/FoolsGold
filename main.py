import datetime
from src.blockchain import Blockchain
from flask import Flask, jsonify, request;

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/MineBlock', methods=['POST'])
def new_block():
    data = request.data.strip().decode()
    if len(data) == 0:
        return 'No data supplied!', 400
    previous_nonce = blockchain.last_block()['nonce']
    proof = blockchain.challenge(previous_nonce)
    block = blockchain.create_block(proof, data)
    return jsonify(block), 201

@app.route('/GetChain', methods=['GET'])
def get_blockchain():
    return jsonify(blockchain.chain), 200

@app.route('/GetChain/<index>', methods=['GET'])
def get_block(index):
    return jsonify([block for block in blockchain.chain if block['index'] == int(index)]), 200

@app.route('/Status', methods=['GET'])
def is_valid():
    return jsonify({'CurrentSize': len(blockchain.chain), 'Timestamp': datetime.datetime.now(), 'ValidState': blockchain.is_chain_valid()}), 200

app.run('localhost', 6666)