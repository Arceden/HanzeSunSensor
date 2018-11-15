from flask import Flask
from dash import Dash

# specify the server
server = Flask(__name__, root_path='/myproject')

# initialise app
app = Dash(server=server)

# configure callback exceptions to be supressed for smooth execution
app.config['suppress_callback_exceptions']=True
