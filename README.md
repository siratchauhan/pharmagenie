# Pharmacist AI Assistant
The Pharmacist AI Assistant is an intelligent web-based tool designed to assist pharmacists and healthcare professionals in managing prescriptions efficiently. The application leverages OCR (Optical Character Recognition) to extract text from uploaded prescriptions, verifies medication names using RxNorm API, and allows users to create and manage orders seamlessly.

## Features
* Prescription OCR Processing: Extracts text from uploaded prescription images using Tesseract OCR.
* Medication Verification: Checks drug validity using RxNorm API.
* Order Management System: Allows pharmacists to create, store, and manage prescription orders in an SQLite database.
* User-Friendly Interface: Built using Flask, HTML, CSS, and JavaScript.
* Secure and Scalable: Ensures privacy and data integrity with secure handling of patient information.

## Demo
Watch the project in action: [Screen Recording](https://drive.google.com/file/d/1c74VzPkbdrUPye7JRUNNYkSEYuwjoeSI/view?usp=drive_link)

## Technologies Used
* Programming Languages: Python, HTML, CSS, JavaScript
* Frameworks & Libraries:
          * Flask (Backend framework)
          * SQLite (Database)
* OpenCV & NumPy (Image processing)
* Tesseract OCR (Text recognition)
* Requests (API calls)
* APIs Used:
          * RXNorm API (Drug validation)
  
## Required Libraries
Flask<br>
OpenCV<br>
NumPy<br>
pytesseract<br>
SQLite3<br>
Requests<br>

## Installation & Setup
Clone the Repository<br>
git clone https://github.com/yourusername/pharmacist-ai-assistant.git<br>
cd pharmacist-ai-assistant

Create a Virtual Environment (Optional but Recommended)
python -m venv venv<br>
source venv/bin/activate  # On Windows use: venv\Scripts\activate<br>

Install Dependencies
pip install -r requirements.txt

Initialize the Database
python app.py<br>
(This will create the pharmacist.db file automatically.)

Run the Flask App<br>
flask run

Access the Application<br>
Open your browser and go to: http://127.0.0.1:5000

## Usage
* Upload a Prescription Image: The OCR will extract text automatically.
* Verify Drug Validity: Use the drug checker to confirm medicine authenticity.
* Create and Manage Orders: Add medications to the order system and process them.

## Contact
For any queries, reach out at tanishaverma081@example.com or open an issue on GitHub.
