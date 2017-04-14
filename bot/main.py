"""Simple REST server"""

from app import APP_INSTANCE

# export WSGI application
# pylint: disable=invalid-name
application = APP_INSTANCE.api
APP_INSTANCE.run()
