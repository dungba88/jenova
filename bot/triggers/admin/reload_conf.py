"""Trigger implementation for reload configuration"""

from app import APP_INSTANCE as app

def run(execution_context):
    """run the action"""
    app.reload_config()
    execution_context.finish()
