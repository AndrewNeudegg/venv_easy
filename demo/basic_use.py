'''Basic use examples.'''

# Import venv.
from .. import venv

# Declare new venv.
# Also supports constructor init.
env = venv()
# Set the path, relative or absoloute.
path = '.venv'
# Check if this is a valid venv.
if env.VenvExists(path):
    # Resume working in this venv.
    env._init_app(app=__name__, path=path)
else:
    # Create a venv, and install django as a requirement.
    env._init_app(app=__name__, refresh_env=False, requirements=['django'], path=path)


# Requirements can also be loaded from file. 
# Venv can be refreshed upon each use.