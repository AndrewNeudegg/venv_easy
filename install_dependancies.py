'''
    Python based extension installer.
'''
import os

def InstallRequirements(requirements_file_path=None, requirments_list=None):
    '''
        Installs any requirements from file or from from a list.
    '''
    import pip
    # Install Requirements from list.
    if requirements_file_path:
        if os.path.exists(requirements_file_path):
            pip.main(['install', '-r', requirements_file_path])
    # Install singular packages.
    if requirments_list:
        for item in requirments_list:
            pip.main(['install', item])
