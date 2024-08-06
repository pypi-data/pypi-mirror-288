import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    import click
    from thunder import auth
    import sys
    import os
    from os.path import join
    from scp import SCPClient
    import paramiko
    import getpass
    import subprocess
    from io import StringIO
    from multiprocessing import Process, Event
    import time

    from thunder import thunder_helper
    from thunder import container_helper
    from thunder.file_sync import start_file_sync
    from importlib.metadata import version
    import requests
    from packaging import version as version_parser
    from thunder import api
    from yaspin import yaspin

PACKAGE_NAME = "tnr"  # update if name changes
# Get the directory of the current file (thunder.py), then go up two levels to the root
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..", "..")

# Add the src directory to sys.path
sys.path.append(root_dir)


class DefaultCommandGroup(click.Group):
    def resolve_command(self, ctx, args: list):
        try:
            # Try to resolve the command normally
            check_for_update()
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
        except click.exceptions.UsageError:
            # If no command is found, default to 'run' and include the args
            return "run", run, args


@click.group(
    cls=DefaultCommandGroup,
    help="This CLI is the interface between you and Thunder Compute.",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.pass_context
@click.version_option(version=version(PACKAGE_NAME))
def cli(ctx):
    setup = '''__tnr_setup() {
    if [[ "$(type -t tnr)" == "function" ]]; then
        return
    fi
    
    if [[ $LD_PRELOAD != *"libthunder.so"* ]]; then
        # We aren't running in a thunder shell
        return
    fi

    export __TNR_BINARY_PATH=$(command -v tnr)
    export __DEFAULT_PS1=$PS1
    PS1="(⚡$($__TNR_BINARY_PATH device --raw)) $__DEFAULT_PS1"

    tnr() {
        if [ "$1" = "device" ]; then
            if [ $# -eq 1 ]; then
                # Handle the case for 'tnr device' with no additional arguments
                "$__TNR_BINARY_PATH" "$@"
            elif [ "$2" = "cpu" ]; then
                # Handle the case for 'tnr device cpu'
                "$__TNR_BINARY_PATH" "$@"
                unset LD_PRELOAD
                PS1="(⚡CPU) $__DEFAULT_PS1"
            else
                # Handle other 'tnr device' commands
                "$__TNR_BINARY_PATH" "$@"
                if [ $? -eq 0 ]; then
                    export LD_PRELOAD=`readlink -f ~/.thunder/libthunder.so`
                    PS1="(⚡${2^^}) $__DEFAULT_PS1"
                fi

            fi
        else
            # Forward the command to the actual tnr binary for all other cases
            "$__TNR_BINARY_PATH" "$@"
        fi
    }
}

__tnr_setup'''
    basedir = join(os.path.expanduser("~"), ".thunder")
    if not os.path.exists(basedir):
        os.makedirs(basedir)
        
    scriptfile = join(basedir, 'setup.sh')
    if not os.path.exists(scriptfile):
        with open(scriptfile, 'w') as f:
            f.write(setup)
        os.chmod(scriptfile, 0o555)
        
        bashrc = join(os.path.expanduser('~'), '.bashrc')
        with open(bashrc, 'a') as f:
            f.write(f'\n# start tnr setup\n. {scriptfile}\n# end tnr setup\n')
    
    device_file = join(basedir, "dev")
    if not os.path.exists(device_file):
        # If not valid, set it to the default value
        with open(device_file, "w") as f:
            f.write("t4")


@cli.command(
    help="Runs a specified task on Thunder Compute. This is the default behavior of the tnr command. Please see thundergpu.net for detailed documentation.",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.option("--ngpus", default=1, help="Specify the number of GPUs to use.")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def run(ngpus, args):
    if not args:  # Check if args is empty
        click.echo("No arguments provided. Exiting...")
        sys.exit(0)

    id_token, refresh_token, uid = auth.load_tokens()

    if not id_token or not refresh_token:
        click.echo("Please log in to begin using Thunder Compute.")
        id_token, refresh_token, uid = auth.login()

        if not id_token or not refresh_token:
            return

    id_token, refresh_token, uid = auth.handle_token_refresh(refresh_token)

    # Create an instance of Task with required arguments
    task = thunder_helper.Task(ngpus, args, uid)

    # Execute the task
    if not task.execute_task(id_token):
        return

    # Close the session
    if not task.close_session(id_token):
        click.echo("Failed to close the session.")


@click.option(
    "--port",
    "-p",
    multiple=True,
    help="Port(s) to forward from the container. To specify a continuous range use <start_port>:<end_port> syntax. To specify multiple port / ranges add another --port / -p flag.",
)
@cli.command(
    help="Creates a Docker container for running commands on Thunder Compute in MacOS and Windows. If you are having trouble in your linux environment, this command may help."
)
def container(port):
    container_helper.create_docker_container(port)


@cli.command(help="Logs in to Thunder Compute.")
def login():
    auth.login()


@cli.command(help="Logs out from the Thunder Compute CLI.")
def logout():
    auth.logout()


@cli.command(help="Set which type of GPU to run on.")
@click.argument("device_type", required=False)
@click.option("-n", "--ngpus", type=int)
@click.option("--raw", required=False, is_flag=True)
def device(device_type, ngpus, raw):
    basedir = join(os.path.expanduser("~"), ".thunder")
    device_file = join(basedir, "dev")
    num_file = join(basedir, "ngpus")
    supported_devices = set(
        [
            "cpu",
            "t4",
            "v100",
            "a100",
            "l4",
            "p4",
            "p100",
            "h100",
        ]
    )
    
    if not os.path.exists(basedir):
        os.makedirs(basedir)
        
    if not os.path.exists(device_file):
        with open(device_file, "w") as f:
            f.write("t4")
    if not os.path.exists(num_file):
        with open(num_file, "w") as f:
            f.write("1")
                
    if device_type is None:
        with open(device_file, "r") as f:
            device = f.read().strip()

        if device not in supported_devices:
            # If not valid, set it to the default value
            device = "t4"
            with open(device_file, "w") as f:
                f.write(device)
                
        if ngpus is None:
            with open(num_file, "r") as f:
                content = f.read().strip()

            if not content.isnumeric():
                # If not valid, set it to the default value
                ngpus = 1
                with open(num_file, "w") as f:
                    f.write(str(ngpus))
            else:
                ngpus = int(content)

        if raw is not None and raw:
            click.echo(device.upper())
            return
        
        if device.lower() == 'cpu':
            click.echo(click.style("ℹ️ No GPU selected - use `tnr device <gpu-type>` to select a GPU", fg="cyan"))
            return

        if ngpus == 1:
            click.echo(click.style(f"ℹ️ Current GPU: {device.upper()}", fg="cyan"))
        else:
            click.echo(click.style(f"ℹ️ Current GPUs: {ngpus} x {device.upper()}", fg="cyan"))
        return

    if device_type.lower() not in supported_devices:
        click.echo(
            click.style(
                f"⛔ Unsupported device type: {device_type}. Please select one of CPU, T4, V100, A100, L4, P4, P100, or H100",
                fg="red",
            )
        )
        exit(1)
        
    if device_type.lower() == 'cpu':
        with open(device_file, "w") as f:
            f.write(device_type.lower())

        with open(num_file, "w") as f:
            f.write("0")

        click.echo(click.style(f"✅ Device set to CPU, you are now disconnected from any GPUs.", fg="green"))
        return 
    
    with open(device_file, "w") as f:
        f.write(device_type.lower())
    
    if ngpus is None:
        ngpus = 1
        
    with open(num_file, "w") as f:
        f.write(str(ngpus))

    click.echo(click.style(f"✅ Device set to {ngpus} x {device_type.upper()}", fg="green"))


@cli.command(help="Start running in a thunder container!")
@click.option("-s", "--sync", required=False, is_flag=True)
def start(sync):
    id_token, refresh_token, uid = auth.load_tokens()
    if not id_token or not refresh_token:
        click.echo("Please log in to begin using Thunder Compute.")
        id_token, refresh_token, uid = auth.login()

        if not id_token or not refresh_token:
            return

    if not api.is_token_valid(id_token):
        id_token, refresh_token, uid = auth.handle_token_refresh(refresh_token)

    with yaspin(text="Setting up Thunder Compute instance", color="blue") as spinner:
        create_instance_url = "https://create-ec2-instance-b7ngwrgpka-uc.a.run.app"
        try:
            headers = {
                "Authorization": "Bearer " + id_token,
                "Content-Type": "application/json",
            }

            response = requests.post(create_instance_url, headers=headers, timeout=120)
            if response.status_code == 401:
                # Retry with refreshed token
                id_token, refresh_token, uid = auth.handle_token_refresh(refresh_token)
                headers = {
                    "Authorization": "Bearer " + id_token,
                    "Content-Type": "application/json",
                }
                response = requests.post(
                    create_instance_url, headers=headers, timeout=120
                )

            if response.status_code != 200:
                spinner.ok("⛔")
                click.echo(
                    click.style(
                        f"Failed to setup Thunder Compute instance for the following reason: {response.text}",
                        fg="red",
                    )
                )
                exit(1)

        except Exception as _:
            msg = "Failed to create a Thunder Compute instance. Please report this issue to the developers!"
            click.echo(click.style(msg, fg="red"))
            exit(1)

        if response.status_code != 200:
            exit(1)

        basedir = join(os.path.expanduser("~"), ".thunder")
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        keyfile = join(basedir, "id_rsa")
        if "pem_key" in response.json():
            if os.path.exists(keyfile):
                os.chmod(keyfile, 0o600)

            with open(keyfile, "w") as f:
                f.write(response.json()["pem_key"])
            os.chmod(keyfile, 0o400)

        ip = response.json()["public_ip"]
        spinner.ok("✅")

    with yaspin(
        text=f"Connecting to Thunder Compute instance {ip} (this can take about a minute)",
        color="blue",
    ) as spinner:
        
        start_time = time.time()
        connection_successful = False
        while start_time + 60 > time.time():
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username="ubuntu", key_filename=keyfile, timeout=10)
                connection_successful = True
                break
            except Exception as e:
                continue
            
        if connection_successful:
            spinner.ok("✅")
        else:
            spinner.fail("⛔")
            click.echo(
                click.style(
                    "Failed to connect to the thunder compute instance within a minute. Please retry this command or contant the developers at support@thundercompute.com if this issue persists.",
                    fg="red",
                )
            )
            exit(1)

        ssh.exec_command("mkdir -p ~/.thunder && chmod 700 ~/.thunder")
        scp = SCPClient(ssh.get_transport())
        scp.put(join(basedir, "token"), remote_path="~/.thunder/token")

        devfile = join(basedir, "dev")
        if os.path.exists(devfile):
            scp.put(devfile, remote_path="~/.thunder/dev")


    if sync:
        with yaspin(
            text="Copying current directory over recursively", color="blue"
        ) as spinner:
            scp.put(os.getcwd(), recursive=True)
            spinner.ok("✅")

        with yaspin(text="Setting up automatic file syncing", color="blue") as spinner:
            is_done_event = Event()
            file_sync_process = Process(
                target=start_file_sync,
                args=(
                    is_done_event,
                    ip,
                ),
            )
            file_sync_process.start()
            spinner.ok("✅")

    click.echo(
        click.style(
            f"⚡ You are connected to a Thunder Compute instance on {ip}! Press control-d to disconnect ⚡",
            fg="cyan",
        )
    )
    
    if sync:
        init_dir = f'~/{os.path.basename(os.getcwd())}'
    else:
        init_dir = '~'
    subprocess.run(
        [
            f"ssh ubuntu@{ip} -o StrictHostKeyChecking=accept-new -i {keyfile} -t 'pip install --upgrade tnr --quiet && cd {init_dir} && exec /home/ubuntu/.local/bin/tnr run /bin/bash'"
        ],
        shell=True,
    )
    click.echo(click.style("⚡ Exiting thunder instance ⚡", fg="cyan"))
    
    if sync:
        is_done_event.set()

    ssh.close()


def check_for_update():
    try:
        current_version = version(PACKAGE_NAME)
        response = requests.get(f"https://pypi.org/pypi/{PACKAGE_NAME}/json", timeout=1)
        json_data = response.json() if response else {}
        latest_version = json_data.get("info", {}).get("version", None)
        if version_parser.parse(current_version) < version_parser.parse(latest_version):
            click.echo(
                f"Update available: {latest_version}. Run `pip install --upgrade {PACKAGE_NAME}` to update.",
                err=True,
            )
    except Exception as e:
        click.echo(f"Error checking for update: {e}", err=True)


if __name__ == "__main__":
    cli()
