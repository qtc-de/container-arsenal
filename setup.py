#!/usr/bin/python3

from os import makedirs
from os.path import expanduser, abspath, dirname, isdir, isfile
from shutil import copy

from setuptools import setup
from setuptools.command.install import install


name = 'car'
with open("README.md", "r") as fh:
    long_description = fh.read()


class PostInstall(install):
    '''
    Subclass to allow running commands after package installation. Required for setup of the
    completion script and the configuration file.
    '''
    def run(self):
        user_home = expanduser("~")
        module_path = abspath(dirname(__file__))

        PostInstall.setup_completion(user_home, module_path)
        PostInstall.setup_config(user_home, module_path)

        install.run(self)

    def setup_completion(user_home, module_path):
        '''
        Checks whether the '~/.bash_completion.d' folder exists and copies the autocompletion script
        into it. If the folder does not exist the function just returns. The completion script is
        expected to be sored in the path: {mdoule_path}/{name}/resources/bash_completion.d/{name}

        Parameters:
             user_home              (string)            Absolute path to the users home dir
             module_path            (string)            Absolute path to the module location

         Returns:
             None
        '''

        completion_dir = f'{user_home}/.bash_completion.d/'
        if not isdir(completion_dir):
            return

        completion_file = f'{module_path}/{name}/resources/bash_completion.d/{name}'
        completion_target = f'{completion_dir}/{name}'

        if not isfile(completion_file):
            return

        copy(completion_file, completion_target)

    def setup_config(user_home, module_path):
        '''
        The container arsenal ships a configuration file that is stored inside '~/.config/car'.
        This folder needs to be created and the default config needs to be copied. Additionally,
        the function creates a backup of the old configuration file (if present).

        Parameters:
             user_home              (string)            Absolute path to the users home dir
             module_path            (string)            Absolute path to the module location

         Returns:
             None
        '''
        config_dir = f'{user_home}/.config/car/'
        config_file = f'{user_home}/.config/car/car.toml'
        default_config = f'{module_path}/car/resources/car.toml'

        makedirs(config_dir, exist_ok=True)

        if isfile(config_file):
            copy(config_file, f'{config_file}.back')

        copy(default_config, config_file)


setup(
    url='https://github.com/qtc-de/container-arsenal',
    name='container-arsenal',
    author='Tobias Neitzel (@qtc_de)',
    version='1.1.2',
    author_email='',

    description='A small arsenal of useful docker containers and a script to easy start, stop and manage them.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    packages=['car'],
    package_data={
                        name: [
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
                        ]
                 },
    install_requires=[
                        'toml',
                     ],
    scripts=[
                f'bin/{name}',
            ],
    cmdclass={
                'install': PostInstall,
             },
    classifiers=[
                    'Programming Language :: Python :: 3',
                    'Operating System :: Unix',
                    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                ],
)
