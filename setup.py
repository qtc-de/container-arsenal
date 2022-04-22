#!/usr/bin/python3

from shutil import copy
from pathlib import Path
from setuptools import setup
from setuptools.command.install import install


name = 'car'
with open("README.md", "r") as fh:
    long_description = fh.read()


class PostInstall(install):
    '''
    Subclass to allow running commands after package installation. Required for
    setup of the completion script and the configuration file.
    '''
    def run(self):
        module_path = Path(__file__).parent

        PostInstall.setup_completion(module_path)
        PostInstall.setup_config(module_path)

        install.run(self)

    def setup_completion(module_path: Path) -> None:
        '''
        Checks whether the '~/.bash_completion.d' folder exists and copies the
        autocompletion script into it. If the folder does not exist the function
        just returns. The completion script is expected to be sored in the path:
        {mdoule_path}/{name}/resources/bash_completion.d/{name}

        Parameters:
             module_path        Absolute path to the module location

         Returns:
             None
        '''
        completion_dir = Path.home().joinpath('.bash_completion.d')
        completion_file = Path(f"{name}/resources/bash_completion.d/{name}")

        if not completion_dir.is_dir():
            return

        completion_file = module_path.joinpath(completion_file)
        completion_target = completion_dir.joinpath(name)

        if not completion_file.is_file():
            return

        copy(completion_file, completion_target)

    def setup_config(module_path: Path) -> None:
        '''
        The container arsenal ships a configuration file that is stored inside
        '~/.config/car'. This folder needs to be created and the default config
        needs to be copied. Additionally, the function creates a backup of the
        old configuration file (if present).

        Parameters:
             module_path         Absolute path to the module location

         Returns:
             None
        '''
        config_dir = Path.home().joinpath('.config/car')
        config_file = config_dir.joinpath('car.toml')
        default_config = module_path.joinpath('car/resources/car.toml')

        config_dir.mkdir(exist_ok=True)

        if not default_config.is_file():
            return

        if config_file.is_file():
            copy(config_file, f'{config_file}.back')

        copy(default_config, config_file)


setup(
    url='https://github.com/qtc-de/container-arsenal',
    name='container-arsenal',
    author='Tobias Neitzel (@qtc_de)',
    version='2.2.0',
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
                            'resources/containers/ajp/resources/*',
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
                            'resources/containers/php/*',
                            'resources/containers/php/config/*',
                            'resources/containers/php/scripts/*',
                            'resources/containers/php/ssl/*',
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
                        'PyYAML',
                        'termcolor',
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
