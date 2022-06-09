from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/status', methods=["GET"])
def response():
    print(request.args.keys())
    return jsonify({"data": "Pong"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
