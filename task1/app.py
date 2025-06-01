from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, REGISTRY
import time
import sys

app = Flask(__name__)

requests_total = Counter('flask_requests_total', 'Total HTTP Requests')
response_time = Counter('flask_response_time', 'Response Time in Seconds')

@app.route('/')
def index():
    start_time = time.time()
    requests_total.inc()
    response_time.inc(time.time() - start_time)
    return jsonify(message="Hello, SRE!")

@app.route('/stress')
def stress():
    start_time = time.time()
    # Выполняем CPU-интенсивную задачу (например, вычисляем факториал)
    result = 1
    for i in range(1, 100000):
        result *= i
    requests_total.inc()
    response_time.inc(time.time() - start_time)
    return jsonify(message="Stress test completed", result=str(result))

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)