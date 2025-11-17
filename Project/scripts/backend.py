from web3 import Web3
import hashlib
import json

# --- Connect to blockchain ---
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Ganache
contract_address = "0x4A0e405612286DEdE9f9F6fCc9a7A93B0DEf8999"
abi = [
    {"stateMutability": "nonpayable", "type": "function", "name": "add_admin", "inputs": [{"name": "admin", "type": "address"}], "outputs": []},
    {"stateMutability": "nonpayable", "type": "function", "name": "create_loan", "inputs": [{"name": "name", "type": "string"}, {"name": "id_hash", "type": "bytes32"}, {"name": "amount", "type": "uint256"}, {"name": "interest", "type": "uint256"}, {"name": "term", "type": "uint256"}], "outputs": []},
    {"stateMutability": "nonpayable", "type": "function", "name": "approve_loan", "inputs": [{"name": "loan_id", "type": "uint256"}], "outputs": []},
    {"stateMutability": "nonpayable", "type": "function", "name": "reject_loan", "inputs": [{"name": "loan_id", "type": "uint256"}], "outputs": []},
    {"stateMutability": "payable", "type": "function", "name": "pay_loan", "inputs": [{"name": "loan_id", "type": "uint256"}], "outputs": []},
    {"stateMutability": "view", "type": "function", "name": "get_loans_by_user", "inputs": [{"name": "user", "type": "address"}], "outputs": [{"name": "", "type": "tuple[]", "components": [{"name": "loan_id", "type": "uint256"}, {"name": "borrower", "type": "address"}, {"name": "name", "type": "string"}, {"name": "id_hash", "type": "bytes32"}, {"name": "amount", "type": "uint256"}, {"name": "interest", "type": "uint256"}, {"name": "term", "type": "uint256"}, {"name": "status", "type": "string"}, {"name": "paid_amount", "type": "uint256"}]}]},
    {"stateMutability": "view", "type": "function", "name": "owner", "inputs": [], "outputs": [{"name": "", "type": "address"}]},
    {"stateMutability": "view", "type": "function", "name": "loans", "inputs": [{"name": "arg0", "type": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "loan_id", "type": "uint256"}, {"name": "borrower", "type": "address"}, {"name": "name", "type": "string"}, {"name": "id_hash", "type": "bytes32"}, {"name": "amount", "type": "uint256"}, {"name": "interest", "type": "uint256"}, {"name": "term", "type": "uint256"}, {"name": "status", "type": "string"}, {"name": "paid_amount", "type": "uint256"}]}]},
    {"stateMutability": "view", "type": "function", "name": "loan_counter", "inputs": [], "outputs": [{"name": "", "type": "uint256"}]},
    {"stateMutability": "view", "type": "function", "name": "admins", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "bool"}]},
    {"stateMutability": "nonpayable", "type": "constructor", "inputs": [], "outputs": []}
]
# --- Accounts ---
admin_account = "0xAc4AF60CAe94C81b9d873E63E3B14086919dfE53"
user_account = "0x1Dce3F00D4f753cBeb3729Ab8d4243100e508c4f"
private_keys = {
    admin_account: "0xeac1960c59e065e898cc2dc9387b1c5ba01d608dcdda8e9302cc77480c426bae",
    user_account: "0x4e6f4883bc0b52afcf05fbee05bb80c107448a2152beebc85577ef0342451cbb"
}

# --- Helper to send transaction ---
def send_tx(account, func):
    tx = func.build_transaction({
        'from': account,
        'gas': 300000,
        'nonce': w3.eth.get_transaction_count(account)
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_keys[account])
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

# --- Register Loan ---
def register_loan(account, name, cmnd, amount, interest, term):
    id_hash = bytes.fromhex(hashlib.sha256(cmnd.encode()).hexdigest())
    func = contract.functions.create_loan(name, id_hash, amount, interest, term)
    return send_tx(account, func)

# --- Approve/Reject Loan ---
def approve_loan(account, loan_id):
    func = contract.functions.approve_loan(loan_id)
    return send_tx(account, func)

def reject_loan(account, loan_id):
    func = contract.functions.reject_loan(loan_id)
    return send_tx(account, func)

# --- Pay Loan ---
def pay_loan(account, loan_id, amount_wei):
    func = contract.functions.pay_loan(loan_id)
    tx = func.build_transaction({
        'from': account,
        'value': amount_wei,
        'gas': 300000,
        'nonce': w3.eth.get_transaction_count(account)
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_keys[account])
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

# --- Get Loan History ---
def get_loans_by_user(user):
    loans = contract.functions.get_loans_by_user(user).call()
    return loans
