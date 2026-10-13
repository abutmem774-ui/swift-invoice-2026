import os
from flask import Flask, render_template, request, redirect, url_for
from pypdf import PdfReader

app = Flask(__name__)

def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_data = None
    if request.method == 'POST':
        # التحقق من وجود الملفات المرفوعة
        swift_file = request.files.get('swift_file')
        invoice_file = request.files.get('invoice_file')
        
        if swift_file and invoice_file:
            swift_path = os.path.join('/tmp', swift_file.filename)
            invoice_path = os.path.join('/tmp', invoice_file.filename)
            
            swift_file.save(swift_path)
            invoice_file.save(invoice_path)
            
            swift_text = extract_text_from_pdf(swift_path)
            invoice_text = extract_text_from_pdf(invoice_path)
            
            extracted_data = {
                'swift_text': swift_text,
                'invoice_text': invoice_text
            }
            
            # حذف الملفات المؤقتة لتنظيف الذاكرة
            try:
                os.remove(swift_path)
                os.remove(invoice_path)
            except:
                pass

    return render_template('index.html', data=extracted_data)

if __name__ == '__main__':
    app.run(debug=True)
