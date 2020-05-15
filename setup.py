import os
import shutil
import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install


def additional_setup():
    '''
    The container arsenal ships configuration files and autocompletion scripts that need to be
    installed manually, since pip cannot help us here. This function creates the required folders
    and copies the corresponding configuration files.

    Parameters:
         None

     Returns:
         None
    '''
    user_home = os.path.expanduser("~")
    module_path = os.path.abspath(os.path.dirname(__file__))

    #creating the .config/car folder
    config_dir = '/.config/car/'
    if not os.path.isdir(user_home + config_dir):
        os.makedirs(user_home + config_dir, exist_ok=True)

    #copying car.toml file
    config_file = config_dir + 'car.toml'
    if not os.path.isfile(user_home + config_file):
        shutil.copy(module_path + '/car/resources/car.toml', user_home + config_file)

    #creating a .bash_completion.d directory
    config_dir = "/.bash_completion.d/"
    if not os.path.isdir(user_home + config_dir):
        os.makedirs(user_home + config_dir, exist_ok=True)

    #creating a .bash_completion file
    config_file = "/.bash_completion"
    if not os.path.isfile(user_home + config_file):
        shutil.copy(module_path + "/car/resources/bash_completion", user_home + config_file)

    #creating bash autocomplete script
    config_file = config_dir + "car"
    shutil.copy(module_path + "/car/resources/bash_completion.d/car", user_home + config_file)

    #creating a .zsh directory
    #config_dir = "/.zsh/"
    #if not os.path.isdir(user_home + config_dir):
    #    os.makedirs(user_home + config_dir, exist_ok=True)

    ##creating zsh autocomplete script
    #config_file = config_dir + "_car"
    #shutil.copy(module_path + "/car/resources/zsh_completion.d/_car", user_home + config_file)


class PostDevelopCommand(develop):
    '''
    Simple hook to create the necessary directory structure atfer devlopment install

    Parameters:
         develop                 (Unkown)                Some argument provided by setup.py
 
    Returns:
         None
    '''
    def run(self):
        additional_setup()
        develop.run(self)


class PostInstallCommand(install):
    '''
    Simple hook to create the necessary directory structure atfer install

    Parameters:
         install                 (Unkown)                Some argument provided by setup.py

    Returns:
         None
    '''
    def run(self):
        additional_setup()
        install.run(self)


with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name="car",
        version="1.0.0",
        author="Tobias Neitzel (qtc)",
        author_email="",
        description="car - A small container arsenal",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=[
                            'toml',
                         ],
        packages=setuptools.find_packages(),
        package_data = {
            'car': [
                'resources/*',
                'resources/bash_completion.d/*',
                'resources/containers/*',
                'resources/containers/*',
                'resources/containers/ajp/*',
                'resources/containers/ajp/config/*',
                'resources/containers/ajp/scripts/*',
                'resources/containers/ftp/*',
                'resources/containers/ftp/config/*',
                'resources/containers/ftp/scripts/*',
                'resources/containers/h2b/*',
                'resources/containers/h2b/scripts/*',
                'resources/containers/mysql/*',
                'resources/containers/mysql/config/*',
                'resources/containers/mysql/scripts/*',
                'resources/containers/neo4j/*',
                'resources/containers/neo4j/scripts/*',
                'resources/containers/nginx/*',
                'resources/containers/nginx/config/*',
                'resources/containers/nginx/scripts/*',
                'resources/containers/nginx/ssl/*',
                'resources/containers/samba/*',
                'resources/containers/samba/config/*',
                'resources/containers/samba/scripts/*',
                'resources/containers/ssh/*',
                'resources/containers/ssh/config/*',
                'resources/containers/ssh/scripts/*',
                'resources/containers/ssh/resources/*',
                'resources/containers/tftp/*',
                'resources/containers/tftp/scripts/*',
                'resources/containers/tftp/config/*',
                #'resources/zsh_completion.d/*',
                ]},


        scripts=[
                'bin/car',
                ],

        cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
        },

        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
        ],
    )
