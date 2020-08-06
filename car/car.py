import os
import sys
import toml
import shutil
import subprocess

this = sys.modules[__name__]

this.config = None
this.containers = None
this.module_path = None
this.volume_base_path = None


def init():
    '''
    Initializes the car module by setting configuration options which were read in
    from a .toml file

    Parameters:
        None

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

    if not os.path.isdir(this.volume_base_path):
        print(f"[+] Creating volume base directory at '{this.volume_base_path}'")
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
            print(f"[-] Unable to find container with name: '{name}'")
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
        print(f"[-] Removing '{path}' is probably a mistake.")
        print('[-] Stopping script execution.')
        sys.exit(1)

    # The next restriction could be annoying. But I guess we keep it for security reasons:
    if not path.endswith(name):
        print("[-] Top level resource directories need the same name as the container.")
        print("[-] Stopping script execution.")
        sys.exit(1)

    print(f"[+] Removing top level resource folder '{path}' (container: {name})")
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

        cmd = ['sudo']
        for key, value in container_conf.items():
            cmd.append(f'car_{key}={value}')
        cmd.append('docker-compose')
        cmd.append('build')
        print(f"[+] Running: '{' '.join(cmd)}'")
        subprocess.call(cmd, cwd=base_folder)

    # While the permissions of volumes are handeled by the docker containers,
    # the actual resource folders will be created by the docker deamon and
    # are owned by root. To allow an easy cleanup process, we create non existing
    # resource folders during container startup with permissions of the current user
    resource_folder = get_resource_folder(name)
    if not os.path.isdir(resource_folder):
        print(f"[+] Resource folder '{resource_folder}' does not exist.")
        print("[+] Creating new resource folder.")
        os.makedirs(resource_folder)

    cmd = ['sudo']
    for key, value in container_conf.items():
        cmd.append(f'car_{key}={value}')

    cmd.append('docker-compose')
    cmd.append('up')

    # When using ctrl-c to kill the container, subprocess will try to
    # kill it on its own and receive a permission denied, since it tries
    # to send a signal to a root process. However, the ctrl-c is still
    # catched by the container and therefore we can just catch the exception
    # and do nothing.
    try:
        print(f"[+] Running: '{' '.join(cmd)}'")
        subprocess.call(cmd, cwd=base_folder)
    except PermissionError:
        pass
    except KeyboardInterrupt:
        pass

    if remove:
        cmd = ['sudo']
        for key, value in container_conf.items():
            cmd.append(f'car_{key}={value}')
        cmd.append('docker-compose')
        cmd.append('down')
        print(f"[+] Running: '{' '.join(cmd)}'")
        subprocess.call(cmd, cwd=base_folder)


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
        cmd = ['sudo', 'docker-compose', 'build']
        print(f"[+] Running: '{' '.join(cmd)}'")
        subprocess.call(cmd)

    try:
        cmd = ['sudo', 'docker-compose', 'up']
        print(f"[+] Running: '{' '.join(cmd)}'")
        subprocess.call(cmd)
    except PermissionError:
        pass
    except KeyboardInterrupt:
        pass

    if remove:
        cmd = ['sudo', 'docker-compose', 'down']
        print(f"[+] Running: '{' '.join(cmd)}'")
        subprocess.call(cmd)


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

    cmd = ['sudo']

    for key, value in container_conf.items():
        cmd.append(f'car_{key}={value}')

    cmd.append('docker-compose')
    cmd.append('stop')

    print(f"[+] Running: '{' '.join(cmd)}'")
    subprocess.call(cmd, cwd=base_folder)


def stop_local():
    '''
    Basically the same as the 'stop_container(...)' method, but uses the 'docker-compose.yml'
    from the current working directory.

    Parameters:
        None

    Returns:
        None
    '''
    cmd = ['sudo']
    cmd.append('docker-compose')
    cmd.append('stop')

    print(f"[+] Running: '{' '.join(cmd)}'")
    subprocess.call(cmd)


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

    cmd = ['sudo']

    for key, value in container_conf.items():
        cmd.append(f'car_{key}={value}')

    cmd.append('docker-compose')
    cmd.append('down')

    print(f"[+] Running: '{' '.join(cmd)}'")
    subprocess.call(cmd, cwd=base_folder)


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
    cmd = ['sudo']
    cmd.append('docker-compose')
    cmd.append('down')

    print(f"[+] Running: '{' '.join(cmd)}'")
    subprocess.call(cmd)


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
        print(f"[-] Directory/File with name '{name}' does already exist in the current folder.")
        print("[-] Stopping mirror process.")
        sys.exit(1)

    print(f"[+] Copying base folder of container '{name}' to current working directory.")
    shutil.copytree(base_folder, f'./{name}')

    with open(f'./{name}/docker-compose.yml', 'r') as compose_file:
        content = compose_file.read()

    container_conf = get_container_config(name)
    for key, value in container_conf.items():
        content = content.replace('${car_' + key + '}', value)

    with open(f'./{name}/docker-compose.yml', 'w') as compose_file:
        compose_file.write(content)

    print("[+] Done.")


def exec(name, command, interactive=False):
    '''
    Execute {cmd} inside a running car container.

    Paramaters:
        name                (string)                Name of a container

    Returns:
        None
    '''
    check_existence(name)
    container_name = f'car.{name}'

    cmd = ['sudo', 'docker', 'exec']

    if interactive:
        cmd.append('-it')

    cmd.append(container_name)
    cmd.append(command)

    try:
        print(f"[+] Running: '{' '.join(cmd)}'")
        subprocess.call(cmd)
    except PermissionError:
        pass
    except KeyboardInterrupt:
        pass
