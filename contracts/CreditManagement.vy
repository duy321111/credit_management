# SPDX-License-Identifier: MIT

struct Loan:
    loan_id: uint256
    borrower: address
    name: String[64]
    id_hash: bytes32
    amount: uint256
    interest: uint256
    term: uint256
    status: String[16]
    paid_amount: uint256

owner: public(address)
loans: public(HashMap[uint256, Loan])
loan_counter: public(uint256)
admins: public(HashMap[address, bool])

# --- Constructor ---
@deploy
def __init__():
    self.owner = msg.sender
    self.loan_counter = 0


# --- Admin management ---
@external
def add_admin(admin: address):
    assert self.admins[msg.sender], "Only admin can add"
    self.admins[admin] = True

# --- Create loan ---
@external
def create_loan(name: String[64], id_hash: bytes32, amount: uint256, interest: uint256, term: uint256):
    assert amount > 0, "Amount must be >0"
    assert term >= 1 and term <= 12, "Term 1-12 months"

    self.loan_counter += 1
    self.loans[self.loan_counter] = Loan(
        loan_id=self.loan_counter,
        borrower=msg.sender,
        name=name,
        id_hash=id_hash,
        amount=amount,
        interest=interest,
        term=term,
        status="Pending",
        paid_amount=0
    )


# --- Approve loan ---
@external
def approve_loan(loan_id: uint256):
    assert self.admins[msg.sender], "Only admin"
    loan: Loan = self.loans[loan_id]
    assert loan.status == "Pending", "Only pending loan"
    loan.status = "Approved"
    self.loans[loan_id] = loan

# --- Reject loan ---
@external
def reject_loan(loan_id: uint256):
    assert self.admins[msg.sender], "Only admin"
    loan: Loan = self.loans[loan_id]
    assert loan.status == "Pending", "Only pending loan"
    loan.status = "Rejected"
    self.loans[loan_id] = loan

# --- Pay loan ---
@external
@payable
def pay_loan(loan_id: uint256):
    loan: Loan = self.loans[loan_id]
    assert msg.sender == loan.borrower, "Only borrower"
    assert loan.status == "Approved", "Only approved loans"
    loan.paid_amount += msg.value

    total_due: uint256 = loan.amount + (loan.amount * loan.interest * loan.term) // 100

    if loan.paid_amount >= total_due:
        loan.status = "Completed"

        # Refund nếu thanh toán dư
        if loan.paid_amount > total_due:
            refund: uint256 = loan.paid_amount - total_due
            send(msg.sender, refund)
            loan.paid_amount = total_due

    self.loans[loan_id] = loan



@external
@view
def get_loans_by_user(user: address) -> DynArray[Loan, 100]:
    result: DynArray[Loan, 100] = []
    for i:uint256 in range(1, 101):  
        if i <= self.loan_counter:
            if self.loans[i].borrower == user:
                result.append(self.loans[i])
    return result


