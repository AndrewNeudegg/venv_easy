'''
    Manages virtual envs.
'''
import os
import shutil
import sys
__venv_activated = False


def RemoveExistingVenv(path=None, check_file='.venv-created'):
    ''' Removes existing virtualenv content. '''
    # Define specific files we wish to remove.
    _env_relative_files = [check_file]
    # Define the folders we wish to remove.
    _env_relative_dir = [
        'Include',
        'Lib',
        'Scripts',
        'tcl',
    ]
    # Define current directory.
    if not path:
        path = __GetWorkingDir_safe()
    # Remove folders.
    for _dir in _env_relative_dir:
        _current_dir = os.path.join(path, _dir)
        if os.path.exists(_current_dir):
            shutil.rmtree(_current_dir)
    # Remove files.
    for _file in _env_relative_files:
        _current_file = os.path.join(path, _file)
        if os.path.exists(_current_file):
            os.remove(os.path.join(_current_file))


def __GetWorkingDir_safe():
    '''Gets current working directory safely.'''
    return os.getcwd()


def InstallVirtualEnv():
    '''Installs the virtualenv package if it is not already installed.'''
    import pip
    pip.main(['install', 'virtualenv'])


def CreateVirtualEnv(path=None):
    '''Creates a new virtual environment.'''
    import virtualenv
    if not path:
        path = __GetWorkingDir_safe()
    # Create the control file.
    venv_dir = os.path.join(path)
    # Create the virutal environment.
    virtualenv.create_environment(venv_dir)
    __CreateVenvActivation(path)


def IsVenvActive():
    '''Checks if the script is in a venv now.'''
    global __venv_activated
    return __venv_activated


def __CorrectPaths(path):
    '''
        Modified source of the activate_this.py found within the venv.
    '''
    base = os.path.abspath(path)
    if sys.platform == 'win32':
        site_packages = os.path.join(base, 'Lib', 'site-packages')
    else:
        site_packages = os.path.join(
            base, 'lib', 'python%s' % sys.version[:3], 'site-packages')
    prev_sys_path = list(sys.path)
    import site
    site.addsitedir(site_packages)
    sys.real_prefix = sys.prefix
    sys.prefix = base
    # Move the added items to the front of the path:
    new_sys_path = []

    for item in list(sys.path):
        if item not in prev_sys_path:       
            new_sys_path.append(item)
            sys.path.remove(item)
        else:
            # Strip surplus.
            if 'site-packages' in item:
                sys.path.remove(item)
    sys.path[:0] = new_sys_path


def ActivateVirtualEnv(path=None, custom_paths=None):
    '''Activates a virtual environment.'''
    global __venv_activated
    if not path:
        path = __GetWorkingDir_safe()
    # Activates the virtual environment under this interpreter instance.
    # exec(open(os.path.join(path, "Scripts", "activate_this.py")).read())
    # The above will not work everytime, so custom loader code goes below.
    __CorrectPaths(path)
    __venv_activated = True


def IsVenv(path=None, check_file='.venv-created'):
    '''Checks if a virtualenv has been created using this tool.'''
    if not path:
        path = __GetWorkingDir_safe()
    if os.path.exists(os.path.join(path, check_file)):
        return True
    return False


def __CreateVenvActivation(path=None, check_file='.venv-created'):
    '''Creates the Venv activation file.'''
    if not path:
        path = __GetWorkingDir_safe()
    if os.path.exists(os.path.join(path, check_file)):
        # Already activated. So we return false.
        return False
    open(os.path.join(path, check_file), 'w+')
    # We just activated it, return True.
    # Abort on error.
    return True
