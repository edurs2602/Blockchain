from blockchain import *
from flask import Flask, request, jsonify, make_response
from time import time
import sys

app = Flask(__name__)
blockchain = Blockchain()

port = 5000
if len(sys.argv) >= 2:
    if len(sys.argv[1]) != 4 | (not sys.argv[1].isnumeric()):
        print("Bad usage, the only acceptable param is a 4-digit number")
        exit()
    port = sys.argv[1]

@app.route("/transactions/create", methods=['POST'])
def createTranscation():
    data = request.get_json(force=True)
    sender = data["sender"]
    recipient = data["recipient"]
    amount = data["amount"]
    privWifKey = data["privWifKey"]
    blockchain.createTransaction(sender, recipient, amount, int(time()), privWifKey)

    return jsonify(blockchain.memPool[-1])


@app.route("/transactions/mempool", methods=['GET'])
def getMempool():
    return jsonify(blockchain.memPool)


@app.route("/mine", methods=['GET'])
def mine():
    newBlock = blockchain.createBlock()
    blockchain.mineProofOfWork(blockchain.prevBlock)
    return jsonify(newBlock)


@app.route("/chain", methods=['GET'])
def chain():
    return jsonify(blockchain.chain)

@app.route("/nodes/resolve", methods=['GET'])
def nodeResolve():
    blockchain.resolveConflicts()
    return jsonify("Resolved")

@app.route("/nodes/register", methods=['POST'])
def nodeRegister():
    nodes = request.get_json(force=True)
    newNode = nodes["node"]

    blockchain.nodes.add(newNode)
    return jsonify([node for node in blockchain.nodes])



if __name__ == '__main__':
    app.run(port=port)