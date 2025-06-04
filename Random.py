from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    pool = ''
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    if not pool:
        return "Select at least one character type."

    password = ''.join(random.choices(pool, k=length))
    return password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    length = int(data['length'])
    password = generate_password(
        length,
        data.get('upper'),
        data.get('lower'),
        data.get('digits'),
        data.get('symbols')
    )
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True)
