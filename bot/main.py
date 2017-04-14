"""Simple REST server"""

from app import APP_INSTANCE as app
from bootstrap import ApplicationBootstrap

app.bootstrap = ApplicationBootstrap()
app.run()

# export WSGI application
application = app.api
