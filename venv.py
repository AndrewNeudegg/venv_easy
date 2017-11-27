'''
    Defines the venv
'''
from .install_dependancies import InstallRequirements
from .venvBase import RemoveExistingVenv, CreateVirtualEnv, ActivateVirtualEnv, IsVenv, IsVenvActive, __GetWorkingDir_safe, InstallVirtualEnv
import os


class venv(object):
    '''
        Defines the venv
    '''
    _current_app = None
    _current_requirements = None
    _path = None
    _dependancies = None

    def __init__(self, app=None, refresh_env=None, requirements=None, path=None):
        # Send this over for execution.
        self._init_app(app=app, refresh_env=refresh_env,
                       requirements=requirements, path=path)

    def _init_app(self, app=None, refresh_env=None, requirements=None, path=None):
        # Validate we have something to work with.
        if not app:
            return
        self._current_app = app

        # Assign some defualts.
        if not refresh_env:
            refresh_env = False

        if not requirements:
            requirements = []

        if not path:
            path = __GetWorkingDir_safe()

        InstallVirtualEnv()

        # Check if we want it refreshed.
        if refresh_env:
            self.VenvRefresh(path=path)

        # Activate this venv.
        self.ActivateVenv(path=path)

        # Validate plugin installs.
        self.InstallDependancies(requirements)
        

    def VenvExists(self, path):
        return IsVenv(path)

    def VenvRefresh(self, path=None):
        '''Refreshes an existing installation of a Venv.'''
        RemoveExistingVenv(path)
        CreateVirtualEnv(path)

    def ActivateVenv(self, path=None):
        '''Activates a venv, with checks.'''
        if not IsVenvActive():
            if IsVenv(path):
                # Existing Venv
                ActivateVirtualEnv(path)
            else:
                # Possible first run.
                # Create Env.
                self.VenvRefresh(path)
                ActivateVirtualEnv(path)
                # Validate dependancy installation.
                self.InstallDependancies(self._dependancies)
                

    def InstallDependancies(self, dependancies):
        '''Installs any dependancies this application may have.'''
        # Install Requirements.
        if isinstance(dependancies, list):
            InstallRequirements(None, dependancies)
        elif os.path.exists(dependancies):
            InstallRequirements(dependancies, [])
        else:
            pass
