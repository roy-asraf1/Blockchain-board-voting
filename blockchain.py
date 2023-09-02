
# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify
import Directors


# Part 1 - Building a Blockchain

# defined the class
class Blockchain:

    def __init__(self):
        self.chain = []  # the chain in the blockchain
        self.create_block(proof=1, previous_hash='0')  # first block in the blockhcain, the first
        self.Directors = Directors
        self.voted = []

# the block containing: index,time, previoush hash, id, stocks , decision
    def create_block(self, proof, previous_hash, id):
        id_sum_stocks = self.Directors.hash_table.get_stocks(id)
        decision = input("Do you support the decision?")
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'id member of the director ' : id,
                 'stocks': id_sum_stocks,
                 'decision': decision,
                 }
        self.chain.append(block)
        self.voted.append(id)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def get_previous_vote(self):
        return self.voted[-1]

    def get_previous_stocks(self):
        member = self.get_previous_vote()
        return self.Directors.Directors.get_stocks(member)

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1
        return True


# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
hash_table = Directors(10, 80000)
# insert some values
hash_table.set_stocks('302211958', '40000')
print(hash_table)
print()

hash_table.set_stocks('302211966', '40000')
print(hash_table)
print()

# search/access a record with key
print(hash_table.get_stocks('302211958'))
print()

# delete or remove a value
hash_table.delete_stocks('302211966')
print(hash_table)
# Creating a Blockchain
blockchain = Blockchain(hash_table)


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_vote = blockchain.get_previous_vote()
    sum_of_stocks = blockchain.get_previous_stocks()

    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)



    response = {'message': 'Congratulations, you just mined a new block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'previous_block ': previous_block,
                'previous_vote': previous_vote,
                'sum_of_stocks': sum_of_stocks

                }
    return jsonify(response), 200


# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Checking if the Blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


# Running the app
app.run(host='0.0.0.0', port=5000)
