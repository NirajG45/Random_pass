from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

def generate_password(length):
    if length < 4:
        return "Length too short!"

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # At least one character from each category
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]

    all_chars = lowercase + uppercase + digits + symbols
    password += random.choices(all_chars, k=length - 4)
    random.shuffle(password)
    return ''.join(password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    length = int(data['length'])
    password = generate_password(length)
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True)
