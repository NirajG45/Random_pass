from flask import Flask, render_template, request, jsonify, session
import random, string
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Required for session management

def build_char_pool(options):
    pool = ''
    if options['upper']: pool += string.ascii_uppercase
    if options['lower']: pool += string.ascii_lowercase
    if options['digits']: pool += string.digits
    if options['symbols']: pool += string.punctuation
    return pool

def validate_options(length, options):
    if length < 4:
        return False, "Password length must be at least 4."
    if not any(options.values()):
        return False, "Select at least one character type."
    return True, ""

def generate_password(length, options):
    pool = build_char_pool(options)
    valid, msg = validate_options(length, options)
    if not valid:
        return None, msg

    password = []
    if options['upper']:
        password.append(random.choice(string.ascii_uppercase))
    if options['lower']:
        password.append(random.choice(string.ascii_lowercase))
    if options['digits']:
        password.append(random.choice(string.digits))
    if options['symbols']:
        password.append(random.choice(string.punctuation))

    remaining_length = length - len(password)
    password += random.choices(pool, k=remaining_length)
    random.shuffle(password)

    return ''.join(password), ""

def update_password_history(password):
    history = session.get('history', [])
    timestamped = {'password': password, 'time': datetime.now().strftime('%H:%M:%S')}
    history.insert(0, timestamped)
    session['history'] = history[:5]  # Keep only last 5
    log_password_to_file(password)

def log_password_to_file(password):
    with open("password_log.txt", "a") as f:
        f.write(f"{datetime.now()} : {password}\n")

def get_password_history():
    return session.get('history', [])

@app.route('/')
def password():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        length = int(data.get('length', 12))
        options = {
            'upper': data.get('upper', False),
            'lower': data.get('lower', False),
            'digits': data.get('digits', False),
            'symbols': data.get('symbols', False),
        }

        valid, message = validate_options(length, options)
        if not valid:
            return jsonify({'error': message}), 400

        password, error = generate_password(length, options)
        if error:
            return jsonify({'error': error}), 400

        update_password_history(password)
        return jsonify({'password': password})
    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

@app.route('/history')
def history():
    return jsonify({'history': get_password_history()})

if __name__ == '__main__':
    app.run(debug=True)
