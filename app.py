from flask import Flask, jsonify
import psycopg
from prometheus_client import Counter, generate_latest, REGISTRY
import time
import sys

app = Flask(__name__)

# Метрики Prometheus
requests_total = Counter('flask_requests_total', 'Total HTTP Requests')
response_time = Counter('flask_response_time', 'Response Time in Seconds')

# Подключение к базе с ожиданием
def get_db_connection():
    max_retries = 10
    retry_interval = 5
    for i in range(max_retries):
        try:
            conn = psycopg.connect("dbname=app_db user=user password=password host=db")
            return conn
        except psycopg.OperationalError as e:
            if i == max_retries - 1:
                print(f"Failed to connect to database after {max_retries} attempts: {e}")
                sys.exit(1)
            print(f"Database connection failed, retrying in {retry_interval} seconds... ({i+1}/{max_retries})")
            time.sleep(retry_interval)

@app.route('/')
def index():
    start_time = time.time()
    requests_total.inc()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 'Hello, SRE!'")
    result = cur.fetchone()
    cur.close()
    conn.close()
    response_time.inc(time.time() - start_time)
    return jsonify(message=result[0])

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)