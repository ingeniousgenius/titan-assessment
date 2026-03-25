"""
Flask application for the multi-tenant catalogue service
25th March 2026
"""

import logging
import os

from database import setup_database
from flask import Flask, jsonify
from blueprint import graphql

app = Flask(__name__)
setup_database(app)
app.register_blueprint(graphql)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    PORT = os.environ.get('PORT') or 3025
    app.run(host="0.0.0.0", port=PORT, debug=True)