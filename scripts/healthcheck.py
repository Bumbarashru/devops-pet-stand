import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify

app = Flask(__name__)

logger = logging.getLogger('healthcheck_app')
logger.setLevel(logging.INFO)

handler = RotatingFileHandler('/var/log/healthcheck.log', maxBytes=1*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

logger.addHandler(handler)

@app.route('/health')
def health():
    logger.info("OK")
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(404)
def not_found(e):
    logger.warning("FAIL (HTTP 404)")
    return jsonify({"error": "Not Found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)