from flask import Flask, render_template, request,redirect,url_for
import os
import fitz  # PyMuPDF
from translate import Translator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Set the default language for translation
default_language = 'en'

# Simulated user credentials (insecure, for demonstration purposes only)
users = {'user1': 'password1', 'user2': 'password2'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def create_upload_folder():
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

create_upload_folder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # In a real application, you would typically set up a session here.
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            # Simulated user registration (insecure, for demonstration purposes only)
            users[username] = password
            return redirect(url_for('login'))
        else:
            error = 'Username already exists. Please choose a different one.'

    return render_template('signup.html', error=error)

@app.route('/dashboard')
def dashboard():
    return 'Welcome to the Dashboard!'

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')



# Update your Flask app routes
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    create_upload_folder()

    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        pdf_text = extract_text_from_pdf(filename)

        # Get the selected language from the form or use the default language
        language = request.form.get('language', default_language)

        translated_text = translate_text(pdf_text, language)

        return render_template('result.html', pdf_text=pdf_text, translated_text=translated_text)

    return render_template('index.html', error='Invalid file format. Only PDF files are allowed.')

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()   

    doc.close()
    return text      

def translate_text(text, language=default_language):
    translator = Translator(to_lang=language)
    translation = translator.translate(text)
    return translation

if __name__ == '__main__':
    app.run(debug=True)








