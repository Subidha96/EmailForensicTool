# EmailForensicTool
Email Forensic Tool

Overview

The Email Forensic Tool is a Python-based application that allows users to analyze and extract metadata from email files (.eml). It provides details such as the sender, recipient, subject, headers, authentication results (SPF, DKIM, DMARC), and attachments. The tool supports both a command-line interface (CLI) and a graphical user interface (GUI) using Tkinter.

Features

Parses and extracts metadata from .eml files

Retrieves email headers, including SPF, DKIM, and DMARC authentication results

Extracts email body (plain text or HTML)

Identifies and lists attachments

Provides a graphical user interface (GUI) for ease of use

Saves analysis reports to a text file

Validates email addresses for proper formatting

Requirements

Python 3.x

Required Python libraries:

email

re

os

tkinter

Installation

Ensure you have Python 3 installed.

Install required dependencies (Tkinter is included with Python by default):

pip install tk

Clone or download the project files.

Run the script using:

python email_parser.py

Usage

CLI Mode

Run the script and select CLI mode by entering 1 when prompted.

Provide the path to the .eml file when asked.

The email details will be displayed in the console.

GUI Mode

Run the script and select GUI mode by entering 2 when prompted.

Click "Browse" to select an .eml file.

Click "Analyze Email" to display email metadata.

Click "Save Report" to store the analysis results in a text file.

Click "Validate Email" to check if the email addresses are in a valid format.

Click "Clear" to reset the interface.

Click "Exit" to close the application.
