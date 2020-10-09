import os
import sys
import toml
import shutil
import termcolor
import subprocess

this = sys.modules[__name__]

this.dry = None
this.config = None
this.containers = None
this.module_path = None
this.sudo_required = None
this.volume_base_path = None


def keyword(key, suffix=None, end="\n"):
    '''
    Helper function that prints a highlighted keyword and an opional suffix.

    Parameters:
        key             (string)                Keyword to print
        suffix          (string)                Text to print after keyword
        end             (string)                End character for the last print
    '''
    if suffix is None:
        termcolor.cprint(key, "yellow", end=end)
    else:
        termcolor.cprint(key, "yellow", end=" ")
        print(suffix, end=end)


def plain(text, key, text2=None, end="\n"):
    '''
    Helper function that prints a highlighted keyword, prefixed by non highlighted
    text and followed by an optional suffix.

    Parameters:
        text            (string)                Prefix text before the keyword
        key             (string)                Keyword to print
        text2           (string)                Text to print after keyword
        end             (string)                End character for the last print
    '''
    print(text, end=" ")
    keyword(key, text2, end=end)


def info(text, key=None, text2=None, end="\n"):
    '''
    Helper function that prints a highlighted keyword, prefixed by non highlighted
    text and followed by an optional suffix. At the beginning of the line, the
    character sequence '[+]' is added.

    Parameters:
        text            (string)                Prefix text before the keyword
        key             (string)                Keyword to print
        text2           (string)                Text to print after keyword
        end             (string)                End character for the last print
    '''
    if key is None:
        print("[+] " + text, end=end)
    else:
        print("[+] " + text, end=" ")
        keyword(key, text2, end)


def error(text, key=None, text2=None, end="\n"):
    '''
    Helper function that prints a highlighted keyword, prefixed by non highlighted
    text and followed by an optional suffix. At the beginning of the line, the
    character sequence '[-]' is added.

    Parameters:
        text            (string)                Prefix text before the keyword
        key             (string)                Keyword to print
        text2           (string)                Text to print after keyword
        end             (string)                End character for the last print
    '''
    if key is None:
        print("[-] " + text, end=end)
    else:
        print("[-] " + text, end=" ")
        keyword(key, text2, end)


def verbose_call(cmd, cwd=None):
    '''
    Wrapper aroud subprocess.call that prints the specified command before executing it.

    Parameters:
        cmd             (list[string])          Command sequence to execute
        sudo            (boolean)               Prefix the command by sudo
        dry             (boolean)               Don't execute the command
        cwd             (string)                Current working directory for the command
    '''
    if this.sudo_required:
        cmd = ["sudo"] + cmd

    info("Running: ", ' '.join(cmd))
    if not this.dry:

        try:
            subprocess.call(cmd, cwd=cwd)

        except PermissionError:
            pass

        except KeyboardInterrupt:
            pass


def prepare_call(config, cmds=None):
    '''
    Helper function that turns car specific environment variables into a list that can be
    prefixed befor a docker-compose command.

    Parameters:
        config          (dict)                  Container configuration
        cmd             (list[string])          Optional commands to follow the environment
    '''
    cmd = []
    for key, value in config.items():

        env_variable = f"car_{key}"

        if env_variable in os.environ:
            value = os.environ.get(env_variable)

        cmd.append(f'{env_variable}={value}')

    for command in cmds:
        cmd.append(command)

    return cmd


def init(dry):
    '''
    Initializes the car module by setting configuration options which were read in
    from a .toml file

    Parameters:
        dry             (boolean)               Only print docker-compose commands instead of running them

    Returns:
        None
    '''
    user_home = os.path.expanduser("~")
    user_config = user_home + "/.config/car/car.toml"
    module_path = os.path.abspath(os.path.dirname(__file__))
    path = module_path + "/resources/car.toml"

    # if the user has specified his own config file, read this one
    if os.path.isfile(user_config):
        path = user_config

    module_config = toml.load(path)

    this.volume_base_path = module_config['containers']['volume_base_path']
    this.volume_base_path = os.path.expanduser(this.volume_base_path)

    this.containers = os.listdir(f'{module_path}/resources/containers')
    this.config = module_config
    this.module_path = module_path
    this.sudo_required = module_config['containers']['sudo_required']
    this.dry = dry

    if not os.path.isdir(this.volume_base_path):
        info("Creating volume base directory at", this.volume_base_path)
        os.makedirs(this.volume_base_path)


def list_containers():
    '''
    Just returns a list of available containers.

    Paramaters:
        None

    Returns:
        containers              (list)              List of available containers
    '''
    return this.containers


def expand(raw):
    '''
    Takes some input containing placeholders and replaces them with the corresponding values.

    Parameters:
        raw                 (string)                Some input with placeholders.

    Returns:
        expanded            (string)                Path with expanded placeholders.
    '''
    expanded = raw.replace('<@:BASE:@>', this.volume_base_path)
    return expanded


def check_existence(name, verbose=True, exit=True):
    '''
    Checks wheter the specified container is available inside the container arsenal.

    Parameters:
        name                (string)                Name of a container.
        verbose             (boolean)               Print error messages if not existend.
        exit                (boolean)               End execution if not existend.

    Returns:
        result              (boolean)               True or False ;)
    '''
    if name not in this.containers:

        if verbose:
            error("Unable to find container with name:", name)
        if exit:
            sys.exit(1)
        return False

    return True


def get_resource_folder(name):
    '''
    Returns the path of the top level ressource folder for the specified container.

    Parameters:
        name                (string)                Name of a container.

    Returns:
        path                (string)                Path to the top level ressource folder
    '''
    check_existence(name)
    return expand(this.config['containers'][name][f'{name}_folder'])


def get_container_folder(name):
    '''
    Returns the path of the container directory, where the compose file is located.

    Parameters:
        name                (string)                Name of a container.

    Returns:
        path                (string)                Path to the top level ressource folder
    '''
    check_existence(name)
    return f'{this.module_path}/resources/containers/{name}'


def clean(name):
    '''
    Removes the top level resource folder of the specified container.

    Parameters:
        name                (string)                Name of a container.

    Returns:
        None
    '''
    check_existence(name)
    path = get_resource_folder(name)
    path = os.path.normpath(path)

    # The folder does not exist, so we are done
    if not os.path.isdir(path):
        return

    # Well, we can't catch everything but at least some very dumb calls
    if path == "/" or path == "/home" or path == os.path.expanduser("~"):
        error("Removing", path, "is probably a mistake.")
        error('Stopping script execution.')
        sys.exit(1)

    # The next restriction could be annoying. But I guess we keep it for security reasons:
    if not path.endswith(name):
        error("Top level resource directories need the same name as the container.")
        error("Stopping script execution.")
        sys.exit(1)

    info("Removing top level resource folder ", path, end=" ")
    plain("(container:", name, end="")
    print(")")
    shutil.rmtree(path)


def clean_all():
    '''
    Removes the top level resource folder of each container.

    Parameters:
        None

    Returns:
        None
    '''
    for container in this.containers:
        clean(container)


def get_container_config(name):
    '''
    Returns container specific configurations from the car.toml file for the specified container

    Parameters:
        name                (string)                Name of a container.

    Returns:
        container_conf      (dict)                  Dictionary containing configuration options
    '''
    check_existence(name)
    container_conf = this.config['containers'][name]

    for key in container_conf:
        container_conf[key] = expand(container_conf[key])

    return container_conf


def start_container(name, rebuild=False, remove=False):
    '''
    Starts the specified container. This is done by running 'sudo docker-compose up' with a current
    working directory set to the corresponding container directory. All configuration options from the
    car.toml file will we supplied as environment variables to the 'sudo docker-compose up' call.

    Parameters:
        name                (string)                Name of a container
        rebuild             (boolean)               Force rebuilding of the container
        remove              (boolean)               Autoremove container after shutdown

    Returns:
        None
    '''
    check_existence(name)

    base_folder = get_container_folder(name)
    container_conf = get_container_config(name)

    if rebuild:
        cmd = prepare_call(container_conf, ['docker-compose', 'build'])
        verbose_call(cmd, cwd=base_folder)

    # While the permissions of volumes are handeled by the docker containers,
    # the actual resource folders will be created by the docker deamon and
    # are owned by root. To allow an easy cleanup process, we create non existing
    # resource folders during container startup with permissions of the current user
    resource_folder = get_resource_folder(name)
    if not os.path.isdir(resource_folder):

        info("Resource folder", resource_folder, "does not exist.")
        info("Creating new resource folder.")
        os.makedirs(resource_folder)

    cmd = prepare_call(container_conf, ['docker-compose', 'up'])
    verbose_call(cmd, cwd=base_folder)

    if remove:
        cmd = prepare_call(container_conf, ['docker-compose', 'down'])
        verbose_call(cmd, cwd=base_folder)


def start_local(rebuild=False, remove=False):
    '''
    Basically the same as the 'start_container(...)' function, but does always launch from the current working
    directory. In this case, many checks like container existence or the creation of resource folders is skipped.
    What remains is basically just a wrapper around 'docker-compose.up'.

    Parameters:
        rebuild             (boolean)               Force rebuilding of the container
        remove              (boolean)               Autoremove container after shutdown

    Returns:
        None
    '''
    if rebuild:
        cmd = ['docker-compose', 'build']
        verbose_call(cmd)

    cmd = ['docker-compose', 'up']
    verbose_call(cmd)

    if remove:
        cmd = ['docker-compose', 'down']
        verbose_call(cmd)


def stop_container(name):
    '''
    Stops the specified container. This is the preffered method to shutdown a running container.
    However, one can also hit ctrl-c to shutdown a container.

    Parameters:
        name                (string)                Name of a container.

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)
    container_conf = get_container_config(name)

    cmd = prepare_call(container_conf, ['docker-compose', 'stop'])
    verbose_call(cmd, cwd=base_folder)


def stop_local():
    '''
    Basically the same as the 'stop_container(...)' method, but uses the 'docker-compose.yml'
    from the current working directory.

    Parameters:
        None

    Returns:
        None
    '''
    cmd = ['docker-compose', 'stop']
    verbose_call(cmd)


def rm_container(name):
    '''
    Removes a stopped container.

    Parameters:
        name                (string)                Name of a container.

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)
    container_conf = get_container_config(name)

    cmd = prepare_call(container_conf, ['docker-compose', 'down'])
    verbose_call(cmd, cwd=base_folder)


def rm_all_containers():
    '''
    Removes all stopped containers that are known by the arsenal.

    Parameters:
        None

    Returns:
        None
    '''
    for container in this.containers:
        rm_container(container)


def rm_local():
    '''
    Removes the container that was started by the current directory 'docker-compose.yml'.

    Parameters:
        None

    Returns:
        None
    '''
    cmd = ['docker-compose', 'down']
    verbose_call(cmd)


def mirror(name):
    '''
    Copies a container folder to the current working directory. All environment variables
    inside the 'docker-compose.yml' are replaced with their corresponding values specified
    inside the 'car.toml' configuration file.

    Paramaters:
        name                (string)                Name of a container

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)

    if os.path.exists(f'./{name}'):
        error("Directory/File with name", name, "does already exist in the current folder.")
        error("Stopping mirror process.")
        sys.exit(1)

    info("Copying base folder of container", name, "to current working directory.")
    shutil.copytree(base_folder, f'./{name}')

    with open(f'./{name}/docker-compose.yml', 'r') as compose_file:
        content = compose_file.read()

    container_conf = get_container_config(name)
    for key, value in container_conf.items():
        content = content.replace('${car_' + key + '}', value)

    with open(f'./{name}/docker-compose.yml', 'w') as compose_file:
        compose_file.write(content)

    info("Done.")


def exec(name, command, interactive=False):
    '''
    Execute {cmd} inside a running car container.

    Paramaters:
        name                (string)                Name of a container
        command             (string)                Command to execute
        interactive         (boolean)               Interactive command?

    Returns:
        None
    '''
    check_existence(name)
    container_name = f'car.{name}'

    cmd = ['docker', 'exec']

    if interactive:
        cmd.append('-it')

    cmd.append(container_name)
    cmd.append(command)

    verbose_call(cmd)


def show_env(name):
    '''
    Display possible environment variables for the corresponding container.

    Paramaters:
        name                (string)                Name of a container

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)
    env_info_file = base_folder + "/env_info.txt"

    offset = 30
    info("Available variables are:")
    info("Name".ljust(offset), end="")
    print("Value".ljust(offset), end="")
    print("Description")

    try:

        with open(env_info_file) as f:

            lines = f.readlines()
            for line in lines:

                filtered = " ".join(line.split())
                split = filtered.split()

                variable_name = split[0]
                variable_value = split[1]
                variable_desc = split[2]

                print("[+] ", end="")
                termcolor.cprint(variable_name.ljust(offset), "yellow", end="")
                termcolor.cprint(variable_value.ljust(offset), "yellow", end="")
                termcolor.cprint(variable_desc, "blue")

    except FileNotFoundError:

        error("Unable to find", "env_info.txt", "for container", end=" ")
        termcolor.cprint(name, "yellow")


def wipe(name):
    '''
    Removes the image of the specified container.

    Paramaters:
        name                (string)                Name of a container

    Returns:
        None
    '''
    check_existence(name)
    container_name = f'car/{name}'

    cmd = ['docker', 'image', 'rm', container_name]
    verbose_call(cmd)


def wipe_all():
    '''
    Removes all car images.

    Parameters:
        None

    Returns:
        None
    '''
    for container in this.containers:
        wipe(container)
