from web3 import Web3
import hashlib
import time

# ---------------------------------------------
#  CONNECT TO GETH
# ---------------------------------------------
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    raise Exception("❌ Không kết nối được Geth!")

# Gas price cố định
GAS_PRICE = w3.to_wei(20, "gwei")

# ---------------------------------------------
#  CONTRACT
# ---------------------------------------------
contract_address = "0x4A0e405612286DEdE9f9F6fCc9a7A93B0DEf8999"

abi = [
    {"stateMutability": "nonpayable", "type": "function", "name": "add_admin", "inputs":[{"name":"admin","type":"address"}],"outputs":[]},
    {"stateMutability": "nonpayable", "type": "function", "name": "create_loan", "inputs":[
        {"name":"name","type":"string"},
        {"name":"id_hash","type":"bytes32"},
        {"name":"amount","type":"uint256"},
        {"name":"interest","type":"uint256"},
        {"name":"term","type":"uint256"}],
     "outputs":[]},
    {"stateMutability": "nonpayable", "type": "function", "name": "approve_loan", "inputs":[{"name":"loan_id","type":"uint256"}],"outputs":[]},
    {"stateMutability": "nonpayable", "type": "function", "name": "reject_loan", "inputs":[{"name":"loan_id","type":"uint256"}],"outputs":[]},
    {"stateMutability": "payable", "type": "function", "name": "pay_loan", "inputs":[{"name":"loan_id","type":"uint256"}],"outputs":[]},
    {"stateMutability": "view", "type": "function", "name": "get_loans_by_user", "inputs":[{"name":"user","type":"address"}],
     "outputs":[{"name":"","type":"tuple[]","components":[
        {"name":"loan_id","type":"uint256"},
        {"name":"borrower","type":"address"},
        {"name":"name","type":"string"},
        {"name":"id_hash","type":"bytes32"},
        {"name":"amount","type":"uint256"},
        {"name":"interest","type":"uint256"},
        {"name":"term","type":"uint256"},
        {"name":"status","type":"string"},
        {"name":"paid_amount","type":"uint256"}
    ]}]},
]

contract = w3.eth.contract(address=contract_address, abi=abi)

# ---------------------------------------------
#  ACCOUNTS + PRIVATE KEYS
# ---------------------------------------------
admin_account = "0xAc4AF60CAe94C81b9d873E63E3B14086919dfE53"
user_account = "0x1Dce3F00D4f753cBeb3729Ab8d4243100e508c4f"

private_keys = {
    admin_account: "0xeac1960c59e065e898cc2dc9387b1c5ba01d608dcdda8e9302cc77480c426bae",
    user_account:  "0x4e6f4883bc0b52afcf05fbee05bb80c107448a2152beebc85577ef0342451cbb"
}

# ---------------------------------------------
#  SEND TRANSACTION (PRIVATE KEY SIGNING)
# ---------------------------------------------
def send_tx(account, func, value=0):
    tx = func.build_transaction({
        'from': account,
        'gas': 300000,
        'gasPrice': GAS_PRICE,
        'nonce': w3.eth.get_transaction_count(account),
        'chainId': w3.eth.chain_id
    })
    if value > 0:
        tx['value'] = value

    signed = w3.eth.account.sign_transaction(tx, private_keys[account])
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    time.sleep(0.3)  # tránh lỗi nonce trên Geth
    return receipt

# ---------------------------------------------
#  TEST FUNCTIONS
# ---------------------------------------------
def test_add_admin():
    print("\n=== TEST: add_admin ===")
    receipt = send_tx(admin_account, contract.functions.add_admin(admin_account))
    print("SUCCESS add_admin, gas:", receipt.gasUsed)

def test_create_loan():
    print("\n=== TEST: create_loan ===")
    id_hash = bytes.fromhex(hashlib.sha256("123456".encode()).hexdigest())
    receipt = send_tx(user_account, contract.functions.create_loan("Nguyen Van A", id_hash, 1000000, 5, 6))
    print("Loan created, gas:", receipt.gasUsed)

def test_approve_loan():
    print("\n=== TEST: approve_loan ===")
    receipt = send_tx(admin_account, contract.functions.approve_loan(1))
    print("Loan approved, gas:", receipt.gasUsed)

def test_reject_loan():
    print("\n=== TEST: reject_loan ===")
    id_hash = bytes.fromhex(hashlib.sha256("999".encode()).hexdigest())
    send_tx(user_account, contract.functions.create_loan("Reject Loan", id_hash, 500000, 3, 4))
    receipt = send_tx(admin_account, contract.functions.reject_loan(2))
    print("Loan rejected, gas:", receipt.gasUsed)

def test_pay_loan():
    print("\n=== TEST: pay_loan ===")
    principal = 1_000_000
    interest = (principal * 5 * 6) // 100
    total = principal + interest
    receipt = send_tx(user_account, contract.functions.pay_loan(1), value=total)
    print("Loan paid, gas:", receipt.gasUsed)

def test_get_history():
    print("\n=== TEST: get_loans_by_user ===")
    loans = contract.functions.get_loans_by_user(user_account).call()
    print(f"User has {len(loans)} loans:")
    for loan in loans:
        print(f"LoanID={loan[0]}, Status={loan[7]}, Amount={loan[4]}, Paid={loan[8]}")

# ---------------------------------------------
#  RUN ALL TESTS
# ---------------------------------------------
if __name__ == "__main__":
    test_add_admin()
    test_create_loan()
    test_approve_loan()
    test_reject_loan()
    test_pay_loan()
    test_get_history()
    print("\n=== ALL TESTS DONE ===")
