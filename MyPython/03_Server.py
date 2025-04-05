from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_code():
    code = request.form['code']
    try:
        result = subprocess.run(['python3', '-c', code], capture_output=True, text=True, timeout=5)
        return jsonify({'output': result.stdout, 'error': result.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Code execution timed out'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)