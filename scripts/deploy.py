from ape import accounts, project

def main():
    # --- 1. Load account để deploy ---
    deployer = accounts.load("credit_deployer")
    deployer.set_autosign(True, passphrase="123456789")  # tự động ký giao dịch

    # --- 2. Deploy contract ---
    # project.creditmanagement = tên project + tên contract (lowercase)
    contract = project.CreditManagement.deploy(sender=deployer)

    # --- 3. In địa chỉ contract và thông tin ---
    print(f"CreditManagement contract deployed at: {contract.address}")
    print(f"Deployer address: {deployer.address}")
