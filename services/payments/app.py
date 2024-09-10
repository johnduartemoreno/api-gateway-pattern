from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/payments/')
def payments():
    return jsonify({"message": "Payments service"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)