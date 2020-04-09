import hashlib
import requests

import sys
import json


coin = 0 #coin counter

def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    print("proof of work process starting")
    block_string = json.dumps(block["last_block"], sort_keys=True)
    proof = 0
    while not valid_proof(block_string, proof):
        proof += 1
    return proof
    # return proof,"proof of work process is finished"


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    if guess_hash[:3] == "000":
        print(block_string,proof,guess_hash)
    return guess_hash[:3] == "000"


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    '''
    step 1: get last block
    step 2: initiate proof of work process
    step 3: when proof is found, call mine endpoint and send proof with user id (pulled from text file)
    step 4a: get a positive response (receive one coin) 
    step 4b: if failure, go back to step 1 because someone else might have generated the block  
    '''

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            last_block_response = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        new_proof = proof_of_work(last_block_response) #generating valid hash from 

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        if data["message"] == "New Block Forged":
            coin += 1 
            print("You have succesfully mined one coin!!!")
        else:
            print("invalid proof format")

        
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
