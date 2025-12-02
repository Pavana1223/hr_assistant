from flask import Flask, request, jsonify
from agent import answer_query

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.json or {}
    q = data.get("question", "")
    if not q:
        return jsonify({"error": "question required"}), 400
    resp = answer_query(q)
    return jsonify(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)