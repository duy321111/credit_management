from web3 import Web3
import hashlib

# --- Connect to GETH ---
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Check connect
print("Connected:", w3.is_connected())

# --- Geth accounts ---
admin_account = "0xAc4AF60CAe94C81b9d873E63E3B14086919dfE53"
user_account = "0x1Dce3F00D4f753cBeb3729Ab8d4243100e508c4f"

account_password = "123"     # password tạo khi import private key

# --- Contract setup ---
contract_address = "0x4A0e405612286DEdE9f9F6fCc9a7A93B0DEf8999"
contract = w3.eth.contract(address=contract_address, abi=abi)

# Unlock Geth account
def unlock(account):
    w3.geth.personal.unlock_account(account, account_password, 300)

# --- Send TX using Geth node signing ---
def send_tx(account, func, value=0):
    unlock(account)

    tx = func.build_transaction({
        'from': account,
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account),
        'chainId': w3.eth.chain_id
    })

    if value > 0:
        tx['value'] = value

    tx_hash = w3.eth.send_transaction(tx)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

# --- Register Loan ---
def register_loan(account, name, cmnd, amount, interest, term):
    id_hash = bytes.fromhex(hashlib.sha256(cmnd.encode()).hexdigest())
    func = contract.functions.create_loan(name, id_hash, amount, interest, term)
    return send_tx(account, func)

# --- Approve Loan ---
def approve_loan(account, loan_id):
    func = contract.functions.approve_loan(loan_id)
    return send_tx(account, func)

# --- Reject Loan ---
def reject_loan(account, loan_id):
    func = contract.functions.reject_loan(loan_id)
    return send_tx(account, func)

# --- Pay Loan ---
def pay_loan(account, loan_id, amount_wei):
    func = contract.functions.pay_loan(loan_id)
    return send_tx(account, func, value=amount_wei)

# --- Get Loan List ---
def get_loans_by_user(user):
    return contract.functions.get_loans_by_user(user).call()
