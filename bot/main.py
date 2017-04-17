"""Simple REST server"""

from app import APP_INSTANCE as app
from bootstrap import ApplicationBootstrap

app.bootstrap = ApplicationBootstrap()

# export WSGI application
application = app.api

# run the application
app.run()
