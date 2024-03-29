import os
import sys
import toml
import yaml
import shutil
import termcolor
import subprocess
from pathlib import Path

this = sys.modules[__name__]

this.dry = None
this.config = None
this.containers = None
this.module_path = None
this.sudo_required = None
this.volume_base_path = None


def nested_lookup(nested_dict: dict, key: str) -> str:
    '''
    Find a key within a nested dictionary.

    Parameters:
        nested_dict         Nested dictionary
        key                 Key to look for

    Returns:
        str                 Result for the looked up key
    '''
    if key in nested_dict:
        return nested_dict[key]

    for value in filter(lambda x: type(x) == dict, nested_dict.values()):

        result = nested_lookup(value, key)

        if result is not None:
            return result

    return None


def keyword(key: str, suffix: str = None, end: str = "\n") -> None:
    '''
    Helper function that prints a highlighted keyword and an opional suffix.

    Parameters:
        key             Keyword to print
        suffix          Text to print after keyword
        end             End character for the last print

    Returns:
        None
    '''
    if suffix is None:
        termcolor.cprint(key, "yellow", end=end)

    else:
        termcolor.cprint(key, "yellow", end=" ")
        print(suffix, end=end)


def plain(text: str, key: str, text2: str = None, end: str = "\n") -> None:
    '''
    Helper function that prints a highlighted keyword, prefixed by non highlighted
    text and followed by an optional suffix.

    Parameters:
        text            Prefix text before the keyword
        key             Keyword to print
        text2           Text to print after keyword
        end             End character for the last print

    Returns:
        None
    '''
    print(text, end=" ")
    keyword(key, text2, end=end)


def info(text: str, key: str = None, text2: str = None, end: str = "\n") -> None:
    '''
    Helper function that prints a highlighted keyword, prefixed by non highlighted
    text and followed by an optional suffix. At the beginning of the line, the
    character sequence '[+]' is added.

    Parameters:
        text            Prefix text before the keyword
        key             Keyword to print
        text2           Text to print after keyword
        end             End character for the last print

    Returns:
        None
    '''
    if key is None:
        print("[+] " + text, end=end)
    else:
        print("[+] " + text, end=" ")
        keyword(key, text2, end)


def error(text: str, key: str = None, text2: str = None, end: str = "\n") -> None:
    '''
    Helper function that prints a highlighted keyword, prefixed by non highlighted
    text and followed by an optional suffix. At the beginning of the line, the
    character sequence '[-]' is added.

    Parameters:
        text            Prefix text before the keyword
        key             Keyword to print
        text2           Text to print after keyword
        end             End character for the last print

    Returns:
        None
    '''
    if key is None:
        print("[-] " + text, end=end)
    else:
        print("[-] " + text, end=" ")
        keyword(key, text2, end)


def display_env(env: dict) -> None:
    '''
    Takes an dictionary of environment variables and prints it color formatted.

    Paramaters:
        env             Environment for the subprocess.call function

    Returns:
        None
    '''
    info("Environment Variables:")
    for key, value in env.items():

        if key == "PATH":
            continue

        print("[+]", end="\t")
        termcolor.cprint(key.ljust(30), "blue", end="")

        if len(value) > 45:
            value = value[0:45] + "[...]"

        termcolor.cprint(value, "yellow")


def verbose_call(cmd: list[str], cwd: str = None, env: dict = None) -> None:
    '''
    Wrapper aroud subprocess.call that prints the specified command before executing it.

    Parameters:
        cmd             Command sequence to execute
        cwd             Current working directory for the command
        env             Environment for the subprocess.call function

    Returns:
        None
    '''
    if this.sudo_required:

        if env:
            cmd = ["sudo", "-E"] + cmd
        else:
            cmd = ["sudo"] + cmd

    if env:
        display_env(env)
        info("")

    info("Running:", ' '.join(cmd))
    if not this.dry:

        try:
            subprocess.call(cmd, cwd=cwd, env=env)

        except PermissionError:
            pass

        except KeyboardInterrupt:
            pass


def prepare_env(config: dict) -> dict:
    '''
    Helper function that turns car specific environment variables into a dictionary that can
    be passed as the 'env' argument in the subprocess.call function.

    Parameters:
        config          Container configuration

    Returns:
        env             Environment dictionary
    '''
    env = dict()
    env["PATH"] = os.environ.get("PATH")
    env["car_local_uid"] = str(os.getuid())

    for key, value in config.items():

        env_variable = f"car_{key}"

        if env_variable in os.environ:
            value = os.environ.get(env_variable)

        env[env_variable] = value

    return env


def get_compose_file(path: str = ".") -> str:
    '''
    Tries to open the docker-compose file from the current directory and returns its contents.

    Paramaters:
        path            Path to look for the compose file in

    Returns:
        content         Content of the compose file.
    '''
    compose_file = Path(path).joinpath("docker-compose.yml")

    try:
        return compose_file.read_text()

    except FileNotFoundError:
        error("Unable to load", "docker-compose.yml", "file from current working directory")
        sys.exit(1)


def get_compose_property(prop: str, path: str = ".") -> str:
    '''
    Reads the docker-compose file from the current working directory and returns the requested
    property from it:

    Parameters:
        prop            Property to look for
        path            Path to look for the compose file in

    Returns:
        name            Container name stored in docker-compose.yml file
    '''
    compose_file = get_compose_file(path)

    try:
        compose_yml = yaml.safe_load(compose_file)
        result = nested_lookup(compose_yml, prop)

        if result is not None:
            return result

        error("Unable to find property", prop, f"in {compose_file}")
        sys.exit(1)

    except yaml.parser.ParserError:
        error("The file", compose_file, "contains invalid content.")
        sys.exit(1)


def init(dry: bool) -> None:
    '''
    Initializes the car module by setting configuration options which were read in
    from a .toml file

    Parameters:
        dry             Only print docker-compose commands instead of running them

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


def list_containers() -> list[str]:
    '''
    Just returns a list of available containers.

    Paramaters:
        None

    Returns:
        containers              List of available containers
    '''
    return this.containers


def expand(raw: str) -> str:
    '''
    Takes some input containing placeholders and replaces them with the corresponding values.

    Parameters:
        raw                 Some input with placeholders.

    Returns:
        expanded            Path with expanded placeholders.
    '''
    expanded = raw.replace('<@:BASE:@>', this.volume_base_path)
    return expanded


def check_existence(name: str, verbose: bool = True, exit: bool = True) -> bool:
    '''
    Checks wheter the specified container is available inside the container arsenal.

    Parameters:
        name                Name of a container.
        verbose             Print error messages if not existend.
        exit                End execution if not existend.

    Returns:
        result              True or False ;)
    '''
    if name not in this.containers:

        if verbose:
            error("Unable to find container with name:", name)
        if exit:
            sys.exit(1)
        return False

    return True


def get_resource_folder(name: str) -> str:
    '''
    Returns the path of the top level ressource folder for the specified container.

    Parameters:
        name                Name of a container.

    Returns:
        path                Path to the top level ressource folder
    '''
    check_existence(name)
    return expand(this.config['containers'][name][f'{name}_folder'])


def create_resource_folder(name: str) -> None:
    '''
    Creates the resource folder for a container if it does not already exist.

    Parameters:
        name                Name of a container.

    Returns:
        None
    '''
    resource_folder = get_resource_folder(name)
    if not os.path.isdir(resource_folder):
        info("Resource folder", resource_folder, "does not exist.")
        info("Creating new resource folder.")
        os.makedirs(resource_folder)


def get_container_folder(name: str) -> str:
    '''
    Returns the path of the container directory, where the compose file is located.

    Parameters:
        name                Name of a container.

    Returns:
        path                Path to the top level ressource folder
    '''
    check_existence(name)
    return f'{this.module_path}/resources/containers/{name}'


def clean(name: str) -> None:
    '''
    Removes the top level resource folder of the specified container.

    Parameters:
        name                Name of a container.

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

    info("Removing top level resource folder", path, end=" ")
    plain("(container:", name, end="")
    print(")")

    subprocess.call(["rm", "-r", path])


def clean_all() -> None:
    '''
    Removes the top level resource folder of each container.

    Parameters:
        None

    Returns:
        None
    '''
    for container in this.containers:
        clean(container)


def get_container_config(name: str) -> dict:
    '''
    Returns container specific configurations from the car.toml file for the specified container

    Parameters:
        name                Name of a container.

    Returns:
        container_conf      Dictionary containing configuration options
    '''
    check_existence(name)
    container_conf = this.config['containers'][name]

    for key in container_conf:
        container_conf[key] = expand(container_conf[key])

    return container_conf


def start_container(name: str, rebuild: bool = False, remove: bool = False) -> None:
    '''
    Starts the specified container. This is done by running 'sudo docker-compose up' with a current
    working directory set to the corresponding container directory. All configuration options from the
    car.toml file will we supplied as environment variables to the 'sudo docker-compose up' call.

    Parameters:
        name                Name of a container
        rebuild             Force rebuilding of the container
        remove              Autoremove container after shutdown

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)

    container_conf = get_container_config(name)
    env = prepare_env(container_conf)

    if rebuild:
        verbose_call(['docker-compose', 'build'], cwd=base_folder, env=env)

    # While the permissions of volumes are handeled by the docker containers,
    # the actual resource folders will be created by the docker deamon and
    # are owned by root. To allow an easy cleanup process, we create non existing
    # resource folders during container startup with permissions of the current user
    create_resource_folder(name)
    verbose_call(['docker-compose', 'up'], cwd=base_folder, env=env)

    if remove:
        verbose_call(['docker-compose', 'down'], cwd=base_folder, env=env)


def start_local(rebuild: bool = False, remove: bool = False) -> None:
    '''
    Basically the same as the 'start_container(...)' function, but does always launch from the current working
    directory. In this case, many checks like container existence or the creation of resource folders is skipped.
    What remains is basically just a wrapper around 'docker-compose.up'.

    Parameters:
        rebuild             Force rebuilding of the container
        remove              Autoremove container after shutdown

    Returns:
        None
    '''
    if rebuild:
        cmd = ['docker-compose', 'build']
        verbose_call(cmd)

    if not os.path.isfile('./.car_name'):
        error("Unable to find", ".car_name", "file.")
        error("Resource folder is not generated automatically.")

    else:
        with open('./.car_name') as name_file:
            name = name_file.readline().strip()
        check_existence(name)
        create_resource_folder(name)

    cmd = ['docker-compose', 'up']
    verbose_call(cmd)

    if remove:
        cmd = ['docker-compose', 'down']
        verbose_call(cmd)


def stop_container(name: str) -> None:
    '''
    Stops the specified container. This is the preffered method to shutdown a running container.
    However, one can also hit ctrl-c to shutdown a container.

    Parameters:
        name                Name of a container.

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)
    container_conf = get_container_config(name)

    env = prepare_env(container_conf)
    verbose_call(['docker-compose', 'stop'], cwd=base_folder, env=env)


def stop_local() -> None:
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


def rm_container(name: str) -> None:
    '''
    Removes a stopped container.

    Parameters:
        name                Name of a container.

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)
    container_conf = get_container_config(name)

    env = prepare_env(container_conf)
    verbose_call(['docker-compose', 'down'], cwd=base_folder, env=env)


def rm_all_containers() -> None:
    '''
    Removes all stopped containers that are known by the arsenal.

    Parameters:
        None

    Returns:
        None
    '''
    for container in this.containers:
        rm_container(container)


def rm_local() -> None:
    '''
    Removes the container that was started by the current directory 'docker-compose.yml'.

    Parameters:
        None

    Returns:
        None
    '''
    cmd = ['docker-compose', 'down']
    verbose_call(cmd)


def mirror(name: str) -> None:
    '''
    Copies a container folder to the current working directory. All environment variables
    inside the 'docker-compose.yml' are replaced with their corresponding values specified
    inside the 'car.toml' configuration file.

    Paramaters:
        name                Name of a container

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

    content = content.replace('${car_local_uid}', str(os.getuid()))

    with open(f'./{name}/docker-compose.yml', 'w') as compose_file:
        compose_file.write(content)

    with open(f'./{name}/.car_name', 'w') as name_file:
        name_file.write(name)

    info("Done.")


def exec(name: str, command: str, interactive: str = False):
    '''
    Execute {cmd} inside a running car container.

    Paramaters:
        name                Name of a container
        command             Command to execute
        interactive         Interactive command?

    Returns:
        None
    '''
    check_existence(name)

    base_folder = get_container_folder(name)
    container_name = get_compose_property("container_name", base_folder)

    cmd = ['docker', 'exec']

    if interactive:
        cmd.append('-it')

    cmd.append(container_name)
    cmd.append(command)

    verbose_call(cmd)


def show_env(name: str) -> None:
    '''
    Display possible environment variables for the corresponding container.

    Paramaters:
        name                Name of a container

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)
    container_conf = get_container_config(name)

    env_info_file = base_folder + "/env_info.txt"
    env = prepare_env(container_conf)

    offset1, offset2 = (0, 0)
    for key, value in env.items():

        if key == 'PATH':
            continue

        if len(key) > offset1:
            offset1 = len(key)

        if len(value) > offset2:
            offset2 = len(value)

    offset1 += 5
    offset2 += 5

    info("Available environment variables are:")
    info("")
    info("Name".ljust(offset1), end="")
    print("Current Value".ljust(offset2), end="")
    print("Description")

    try:

        with open(env_info_file) as f:

            lines = f.readlines()
            for line in lines:

                filtered = " ".join(line.split())
                split = filtered.split()

                variable_name = split[0]
                variable_desc = " ".join(split[1:])
                variable_value = env.get(variable_name, "")

                print("[+] ", end="")
                termcolor.cprint(variable_name.ljust(offset1), "yellow", end="")
                termcolor.cprint(variable_value.ljust(offset2), "yellow", end="")
                termcolor.cprint(variable_desc, "blue")

    except FileNotFoundError:

        error("Unable to find", "env_info.txt", "for container", end=" ")
        termcolor.cprint(name, "yellow", end="")
        print(".")


def wipe(name: str) -> None:
    '''
    Removes the image of the specified container.

    Paramaters:
        name                Name of a container

    Returns:
        None
    '''
    check_existence(name)

    base_folder = get_container_folder(name)
    image_name = get_compose_property("image", base_folder)

    cmd = ['docker', 'image', 'rm', image_name]
    verbose_call(cmd)


def wipe_all() -> None:
    '''
    Removes all car images.

    Parameters:
        None

    Returns:
        None
    '''
    for container in this.containers:
        wipe(container)


def build(name: str) -> None:
    '''
    Builds the specified container.

    Paramaters:
        name                Name of a container

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)
    container_conf = get_container_config(name)

    env = prepare_env(container_conf)
    verbose_call(['docker-compose', 'build'], cwd=base_folder, env=env)


def build_all() -> None:
    '''
    Build all containers of the arsenal.

    Paramaters:
        None

    Returns:
        None
    '''
    for container in this.containers:
        build(container)


def build_local() -> None:
    '''
    Builds the container from the current working directory.
    Basically just an alias for 'docker-compose build'.

    Paramaters:
        None

    Returns:
        None
    '''
    cmd = ['docker-compose', 'build']
    verbose_call(cmd)


def show_images() -> None:
    '''
    Print a list of currently build car images.

    Paramaters:
        None

    Returns:
        None
    '''
    cmd = ['docker', 'images']
    if this.sudo_required:
        cmd = ["sudo"] + cmd

    info("Running:", ' '.join(cmd))
    output = subprocess.check_output(cmd)
    output = output.decode('utf-8')
    lines = output.split('\n')

    info(lines[0])
    for line in lines[1:]:

        if line.startswith("ghcr.io/qtc-de/container-arsenal"):
            info(line)


def shell(name: str) -> None:
    '''
    Execute an interactive shell (sh) inside a running car container.

    Paramaters:
        name                Name of a container

    Returns:
        None
    '''
    check_existence(name)

    base_folder = get_container_folder(name)
    container_name = get_compose_property("container_name", base_folder)

    cmd = ['docker', 'exec', '-it', container_name, 'sh']
    verbose_call(cmd)


def shell_local() -> None:
    '''
    Spawn an interactive shell inside the container specified by the
    docker-compose.yml from the current working directory.

    Paramaters:
        None

    Returns:
        None
    '''
    container_name = get_compose_property('container_name')

    cmd = ['docker', 'exec', '-it', container_name, 'sh']
    verbose_call(cmd)


def exec_local(command: str, interactive: bool = False) -> None:
    '''
    Execute {cmd} inside the container specified by the current docker-compose.yml
    file.

    Paramaters:
        command             Command to execute
        interactive         Interactive command?

    Returns:
        None
    '''
    container_name = get_compose_property('container_name')

    cmd = ['docker', 'exec']

    if interactive:
        cmd.append('-it')

    cmd.append(container_name)
    cmd.append(command)

    verbose_call(cmd)


def wipe_local() -> None:
    '''
    Removes the docker image specified in the current docker-compose.yml file.

    Paramaters:
        None

    Returns:
        None
    '''
    image_name = get_compose_property('image')

    cmd = ['docker', 'image', 'rm', image_name]
    verbose_call(cmd)


def pull(name: str) -> None:
    '''
    Pulls a prebuild container from GitHub.

    Parameters:
        name                Name of a container.

    Returns:
        None
    '''
    check_existence(name)
    base_folder = get_container_folder(name)

    container_conf = get_container_config(name)
    env = prepare_env(container_conf)

    verbose_call(['docker-compose', 'pull'], cwd=base_folder, env=env)


def pull_all() -> None:
    '''
    Pulls all containers that are available on GitHub.

    Parameters:
        None

    Returns:
        None
    '''
    for container in this.containers:
        pull(container)
