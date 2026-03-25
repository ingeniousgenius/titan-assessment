"""
Flask application for the multi-tenant catalogue service
25th March 2026
"""

import logging
import os

from database import setup_database
from flask import Flask, jsonify
from blueprint import graphql
from tasks import init_tasks

app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
setup_database(app)
app.register_blueprint(graphql)
init_tasks(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})
