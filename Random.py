from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

def build_char_pool(options):
    """Builds the pool of characters based on user selection."""
    pool = ''
    if options['upper']:
        pool += string.ascii_uppercase
    if options['lower']:
        pool += string.ascii_lowercase
    if options['digits']:
        pool += string.digits
    if options['symbols']:
        pool += string.punctuation
    return pool

def validate_options(length, options):
    """Ensures user has given valid password constraints."""
    if length < 4:
        return False, "Password length must be at least 4."
    if not any(options.values()):
        return False, "At least one character type must be selected."
    return True, ""

def generate_password(length, options):
    """Generates a secure password based on user options."""
    pool = build_char_pool(options)

    # Validate again
    valid, msg = validate_options(length, options)
    if not valid:
        return None, msg

    # Guarantee at least one of each selected type
    password = []
    if options['upper']:
        password.append(random.choice(string.ascii_uppercase))
    if options['lower']:
        password.append(random.choice(string.ascii_lowercase))
    if options['digits']:
        password.append(random.choice(string.digits))
    if options['symbols']:
        password.append(random.choice(string.punctuation))

    # Fill remaining characters from the pool
    remaining_length = length - len(password)
    password += random.choices(pool, k=remaining_length)

    # Shuffle the result to make it secure
    random.shuffle(password)

    return ''.join(password), ""

@app.route('/')
def index():
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

        return jsonify({'password': password})

    except Exception as e:
        return jsonify({'error': 'Internal server error: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
