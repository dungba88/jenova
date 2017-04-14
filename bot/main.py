"""Simple REST server"""

from app import APP_INSTANCE

# export WSGI application
application = APP_INSTANCE.api
APP_INSTANCE.run()
