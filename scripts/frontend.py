import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QTextEdit
from backend import register_loan, approve_loan, reject_loan, get_loans_by_user

class CreditApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Credit Management DApp")

        # Layout
        self.layout = QVBoxLayout()

        # --- Register Loan ---
        self.layout.addWidget(QLabel("Họ tên"))
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.layout.addWidget(QLabel("CMND"))
        self.cmnd_input = QLineEdit()
        self.layout.addWidget(self.cmnd_input)

        self.layout.addWidget(QLabel("Số tiền vay"))
        self.amount_input = QLineEdit()
        self.layout.addWidget(self.amount_input)

        self.layout.addWidget(QLabel("Lãi suất (%)"))
        self.interest_input = QLineEdit()
        self.layout.addWidget(self.interest_input)

        self.layout.addWidget(QLabel("Thời hạn (tháng)"))
        self.term_input = QLineEdit()
        self.layout.addWidget(self.term_input)

        self.register_btn = QPushButton("Đăng ký khoản vay")
        self.register_btn.clicked.connect(self.register_loan)
        self.layout.addWidget(self.register_btn)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # --- Loan History ---
        self.layout.addWidget(QLabel("Nhập địa chỉ ví để tra cứu"))
        self.user_input = QLineEdit()
        self.layout.addWidget(self.user_input)

        self.history_btn = QPushButton("Xem lịch sử vay")
        self.history_btn.clicked.connect(self.show_history)
        self.layout.addWidget(self.history_btn)

        self.history_text = QTextEdit()
        self.layout.addWidget(self.history_text)


        self.layout.addWidget(QLabel("Thanh toán LoanID"))
        self.pay_loan_input = QLineEdit()
        self.layout.addWidget(self.pay_loan_input)

        self.layout.addWidget(QLabel("Số tiền (wei)"))
        self.pay_amount_input = QLineEdit()
        self.layout.addWidget(self.pay_amount_input)

        self.pay_btn = QPushButton("Thanh toán khoản vay")
        self.pay_btn.clicked.connect(self.pay_loan)
        self.layout.addWidget(self.pay_btn)

        # Main Widget
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def register_loan(self):
        name = self.name_input.text()
        cmnd = self.cmnd_input.text()
        amount = int(self.amount_input.text())
        interest = int(self.interest_input.text())
        term = int(self.term_input.text())
        try:
            receipt = register_loan("0xUserAddress", name, cmnd, amount, interest, term)
            self.status_label.setText(f"Loan created: TxHash {receipt.transactionHash.hex()}")
        except Exception as e:
            self.status_label.setText(str(e))

    def show_history(self):
        user = self.user_input.text()
        loans = get_loans_by_user(user)
        display = ""
        for loan in loans:
            display += f"LoanID: {loan[0]}, Amount: {loan[4]}, Interest: {loan[5]}%, Term: {loan[6]} tháng, Status: {loan[7]}\n"
        self.history_text.setText(display)
    

    def pay_loan(self):
        loan_id = int(self.pay_loan_input.text())
        amount = int(self.pay_amount_input.text())

        try:
            receipt = pay_loan("0xUserAddress", loan_id, amount)
            self.status_label.setText(f"Paid Loan {loan_id}: Tx {receipt.transactionHash.hex()}")
        except Exception as e:
            self.status_label.setText(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreditApp()
    window.show()
    sys.exit(app.exec())
