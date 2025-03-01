import email
import re
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from email import policy
from email.parser import BytesParser

class EmailParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_email(self):
        try:
            with open(self.file_path, 'rb') as file:
                msg = BytesParser(policy=policy.default).parse(file)

            email_details = {
                "Subject": msg.get("Subject", "N/A"),
                "From": msg.get("From", "N/A"),
                "To": msg.get("To", "N/A"),
                "CC": msg.get("Cc", "N/A"),
                "BCC": msg.get("Bcc", "N/A"),
                "Reply-To": msg.get("Reply-To", "N/A"),
                "Date": msg.get("Date", "N/A"),
                "Message-ID": msg.get("Message-ID", "N/A"),
                "MIME Version": msg.get("MIME-Version", "N/A"),
                "Content Type": msg.get_content_type(),
                "Encoding": msg.get("Content-Transfer-Encoding", "N/A"),
                "Received Headers": self.get_received_headers(msg),
                "SPF/DKIM/DMARC": self.get_authentication_results(msg),
                "Attachments": self.get_attachments(msg)
            }

            parsed_text = "\n".join([f"{key}: {value}" for key, value in email_details.items()])
            return f"Email Analysis:\n{parsed_text}\n"

        except Exception as e:
            return f"Error parsing email: {e}\n"

    def get_email_body(self, msg, subtype):
        """Extracts the plain text or HTML body from the email."""
        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_type() == f"text/{subtype}":
                    try:
                        return part.get_payload(decode=True).decode(part.get_content_charset(), errors="replace")
                    except Exception as e:
                        return f"Error decoding body: {e}"
        else:
            try:
                return msg.get_payload(decode=True).decode(msg.get_content_charset(), errors="replace")
            except Exception as e:
                return f"Error decoding body: {e}"
        return "N/A"

    def get_received_headers(self, msg):
        """Extracts all Received headers to trace email routing."""
        received_headers = msg.get_all("Received", [])
        return "\n".join(received_headers) if received_headers else "N/A"

    def get_authentication_results(self, msg):
        """Extracts SPF, DKIM, and DMARC authentication results."""
        spf = msg.get("Authentication-Results", "N/A")
        dkim = msg.get("DKIM-Signature", "N/A")
        dmarc = msg.get("ARC-Authentication-Results", "N/A")
        return f"SPF: {spf}\nDKIM: {dkim}\nDMARC: {dmarc}"

    def get_attachments(self, msg):
        """Extracts attachment filenames from the email."""
        attachments = []
        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_disposition() == "attachment":
                    filename = part.get_filename()
                    if filename:
                        attachments.append(filename)
        return ", ".join(attachments) if attachments else "No Attachments"

def main():
    print("Choose an interface:")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        cli_interface()
    elif choice == "2":
        run_gui()
    else:
        print("Invalid choice. Please restart and enter 1 or 2.")

def cli_interface():
    file_path = input("Enter the path of the email file (.eml): ").strip('"')
    if not os.path.exists(file_path):
        print("Error: File not found!")
        return
    
    parser = EmailParser(file_path)
    result = parser.parse_email()
    print(result)

def run_gui():
    root = tk.Tk()
    app = EmailForensicTool(root)
    root.mainloop()

class EmailForensicTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Forensic Tool")
        self.root.geometry("600x500")

        self.label = tk.Label(root, text="Select Email File (.eml)", font=("Arial", 12))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.select_button = tk.Button(root, text="Browse", font=("Arial", 10, "bold"), bg="blue", fg="white", command=self.load_email, width=15, height=2, relief="solid", highlightbackground="black")
        self.select_button.grid(row=1, column=0, pady=5)

        self.analyze_button = tk.Button(root, text="Analyze Email", font=("Arial", 10, "bold"), bg="green", fg="white", command=self.analyze_email, width=15, height=2, relief="solid", highlightbackground="black")
        self.analyze_button.grid(row=1, column=1, pady=5)

        self.save_button = tk.Button(root, text="Save Report", font=("Arial", 10, "bold"), bg="orange", fg="white", command=self.save_report, width=15, height=2, relief="solid", highlightbackground="black")
        self.save_button.grid(row=1, column=2, pady=5)

        self.clear_button = tk.Button(root, text="Clear", font=("Arial", 10, "bold"), bg="red", fg="white", command=self.clear_text, width=15, height=2, relief="solid", highlightbackground="black")
        self.clear_button.grid(row=2, column=0, pady=5)

        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 10, "bold"), bg="gray", fg="white", command=root.quit, width=15, height=2, relief="solid", highlightbackground="black")
        self.exit_button.grid(row=2, column=1, pady=5)

        self.validate_button = tk.Button(root, text="Validate Email", font=("Arial", 10, "bold"), bg="purple", fg="white", command=self.validate_email, width=15, height=2, relief="solid", highlightbackground="black")
        self.validate_button.grid(row=2, column=2, pady=5)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Arial", 10))
        self.text_area.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.file_path = ""
        self.result_text = ""

    def load_email(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Email Files", "*.eml")])
        if self.file_path:
            self.label.config(text=f"Loaded: {self.file_path}")

    def analyze_email(self):
        if not self.file_path:
            self.text_area.insert(tk.END, "No file selected!\n")
            return

        parser = EmailParser(self.file_path)
        self.result_text = parser.parse_email()
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, self.result_text)

    def save_report(self):
        if not self.result_text:
            self.text_area.insert(tk.END, "No analysis to save.\n")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as report_file:
                report_file.write(self.result_text)
            self.text_area.insert(tk.END, f"Report saved as: {save_path}\n")

    def clear_text(self):
        self.text_area.delete('1.0', tk.END)
        self.label.config(text="Select Email File (.eml)")

    def validate_email(self):
        if not self.file_path:
            self.text_area.insert(tk.END, "No file selected for validation.\n")
            return

        try:
            with open(self.file_path, 'rb') as file:
                msg = BytesParser(policy=policy.default).parse(file)
            sender = msg.get("From", "N/A")
            recipient = msg.get("To", "N/A")
            # Fixed regex pattern to validate email addresses
            if re.match(r"[^@]+@[^@]+\.[^@]+", sender) and re.match(r"[^@]+@[^@]+\.[^@]+", recipient):
                self.text_area.insert(tk.END, "Email is in valid format.\n")
            else:
                self.text_area.insert(tk.END, "Invalid email format.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"Error validating email: {e}\n")

if __name__ == "__main__":
    main()










