from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton,QLineEdit,QHBoxLayout
import sys
class ChatUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Agent")
        self.resize(500, 600)

        layout = QVBoxLayout()

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""background-color: #343541;
                                        color: #D1D5DB;                 
                                        font-family: 'Arial';           
                                        font-size: 14px;                
                                        font-weight: bold;  """)
        layout.addWidget(self.chat_area)

        self.input_box = QLineEdit()
        self.input_box.setStyleSheet("""
                    background-color: #40414F;      /* Dark input background */
                    color: #FFFFFF;                 /* Typed text color */
                    font-family: 'Arial';
                    font-size: 14px;
                    border: 1px solid #6B7280;      /* Optional border */
                    border-radius: 5px;             /* Rounded corners */
                    padding: 5px;
                """)
        row = QHBoxLayout()
        self.input_box.setPlaceholderText("Type your question")
        row.addWidget(self.input_box)
        layout.addLayout(row)
        send_btn = QPushButton("Send")
        self.input_box.returnPressed.connect(self.send_message)
        send_btn.clicked.connect(self.send_message)
        send_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;   /* White background */
                    color: #111111;              /* Dark text */
                    font-family: 'Arial';
                    font-size: 14px;
                    font-weight: bold;
                    border: 1px solid #CCCCCC;  /* Light gray border */
                    border-radius: 8px;          /* Rounded corners */
                    padding: 8px 16px;           /* Vertical and horizontal padding */
                }
                QPushButton:hover {
                    background-color: #F0F0F0;   /* Slightly gray on hover */
                }
                QPushButton:pressed {
                    background-color: #E0E0E0;   /* Darker gray when pressed */
                }
            """)

        layout.addWidget(send_btn)
        self.setLayout(layout)
    
    def send_message(self):
        action = self.input_box.text()
        self.input_box.clear()
        self.chat_area.append(f"You: {action}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatUI()
    window.setStyleSheet("""
    background-color: #343541;       /* Dark chat background */
    border-radius: 10px;             /* Rounded corners for modern look */
""")
    window.show()
    sys.exit(app.exec())