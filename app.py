import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
import pytesseract
from PIL import Image
import requests

app = Flask(__name__)
app.secret_key = '71b6f0974d4389d11a804f625da8f325'

DATABASE = 'pharmacist.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            medication TEXT NOT NULL,
            dosage TEXT,
            prescription_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/drug-checker', methods=['GET', 'POST'])
def drug_checker():
    result = None
    if request.method == 'POST':
        medicine_name = request.form['medicine_name'].strip()
        rxnav_url = f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={medicine_name}"

        try:
            response = requests.get(rxnav_url)
            data = response.json()
            if "idGroup" in data and "rxnormId" in data["idGroup"] and data["idGroup"]["rxnormId"]:
                result = f"✅ {medicine_name} is a recognized drug."
            else:
                result = f"❌ {medicine_name} is NOT recognized as a registered drug."
        except Exception as e:
            result = f"⚠️ Error: Unable to fetch data. ({str(e)})"
    
    return render_template('drug_checker.html', result=result)

# Fixed the route - now it matches the form action and function name
@app.route('/upload', methods=['GET', 'POST'])
def upload_prescription():
    if request.method == 'POST':
        print("POST request received")  # Debug print
        
        # Check if file part exists
        if 'prescription_image' not in request.files:
            print("No file part in request")  # Debug print
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['prescription_image']
        print(f"File received: {file.filename}")  # Debug print
        
        # Check if file was selected
        if file.filename == '':
            print("No file selected")  # Debug print
            flash('No selected file')
            return redirect(request.url)
            
        if file and file.filename:
            print(f"Processing file: {file.filename}")  # Debug print
            
            # Create uploads directory if it doesn't exist
            upload_dir = 'static/uploads'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
                print(f"Created directory: {upload_dir}")
            
            image_path = os.path.join(upload_dir, file.filename)
            
            try:
                file.save(image_path)
                print(f"File saved to: {image_path}")  # Debug print
                
                # For now, let's skip OCR and use dummy data
                extracted_text = "Paracetamol\nAspirin\nVitamin C"
                print(f"Extracted text: {extracted_text}")  # Debug print
                
                return render_template('upload_result.html', 
                                     prescription_text=extracted_text, 
                                     extracted_text=extracted_text,
                                     image_path=image_path)
                                     
            except Exception as e:
                print(f"Error processing file: {e}")  # Debug print
                flash(f"Error processing image: {e}")
                return redirect(request.url)
        else:
            print("File validation failed")  # Debug print
            flash('Invalid file')
            return redirect(request.url)
            
    return render_template('upload.html')

@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        try:
            print("Create order POST request received")  # Debug print
            
            patient_name = request.form.get('patient_name', '').strip()
            medications = request.form.getlist('medication[]')
            dosages = request.form.getlist('dosage[]')
            prescription_text = request.form.get('prescription_text', '')
            
            print(f"Patient name: {patient_name}")  # Debug print
            print(f"Medications: {medications}")  # Debug print
            print(f"Dosages: {dosages}")  # Debug print
            print(f"Prescription text: {prescription_text}")  # Debug print
            
            # Validate required fields
            if not patient_name:
                flash('Patient name is required!')
                return redirect(request.url)
            
            if not medications or not any(med.strip() for med in medications):
                flash('At least one medication is required!')
                return redirect(request.url)
            
            if not dosages or len(medications) != len(dosages):
                flash('Each medication must have a dosage!')
                return redirect(request.url)
            
            # Database operations
            conn = get_db_connection()
            print("Database connection established")  # Debug print
            
            for i, (medication, dosage) in enumerate(zip(medications, dosages)):
                if medication.strip():  # Only insert non-empty medications
                    print(f"Inserting order {i+1}: {medication} - {dosage}")  # Debug print
                    conn.execute('INSERT INTO orders (patient_name, medication, dosage, prescription_text) VALUES (?, ?, ?, ?)',
                                 (patient_name, medication.strip(), dosage.strip(), prescription_text))
            
            conn.commit()
            conn.close()
            print("Orders inserted successfully")  # Debug print
            
            flash('Order created successfully!')
            return redirect(url_for('list_orders'))
            
        except Exception as e:
            print(f"Error in create_order: {str(e)}")  # Debug print
            import traceback
            traceback.print_exc()  # Print full error traceback
            flash(f'Error creating order: {str(e)}')
            return redirect(request.url)
    
    return render_template('create_order.html')

@app.route('/orders')
def list_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/order_placed/<int:order_id>', methods=['POST'])
def order_placed(order_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()
    flash('Order placed successfully and removed from the list!', 'success')
    return redirect(url_for('list_orders'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
