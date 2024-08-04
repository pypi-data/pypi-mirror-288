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
import warnings

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
warnings.filterwarnings("ignore")

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
    pass


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

    # Initialize the session with the current auth token
    # if not task.get_password(id_token):
    #     id_token, refresh_token, uid = auth.handle_token_refresh(refresh_token)
    #     if not id_token or not refresh_token or not uid:
    #         click.echo("Token, Refresh Token, or UID is invalid. Please log in again.")
    #     if not task.get_password(id_token):
    #         click.echo("Failed to retrieve password for session.")
    #         return

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
def device(device_type):
    device_file = os.path.expanduser("~/.thunder/dev")
    supported_devices = set(
        [
            "t4",
            "v100",
            "a100",
        ]
    )

    if device_type is None:
        with open(device_file, "r") as f:
            content = f.read().strip()

        if content not in supported_devices:
            # If not valid, set it to the default value
            content = "t4"
            with open(device_file, "w") as f:
                f.write(content)

        click.echo(f"Currently running on a {content.upper()} GPU")
        return

    if device_type.lower() not in supported_devices:
        click.echo(
            click.style(
                f"⛔ Unsupported device type: {device_type}. Please select one of T4, V100, or A100",
                fg="red",
            )
        )
        return

    with open(device_file, "w") as f:
        f.write(device_type.lower())

    click.echo(click.style(f"✅ Device set to {device_type.upper()}", fg="green"))


@cli.command(help="Start running in a thunder container!")
@click.option("-ns", "--no-sync", required=False, is_flag=True)
def start(no_sync):
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

    print("F",  keyfile)
    with yaspin(
        text=f"Connecting to Thunder Compute instance {ip} (this can take a few minutes)",
        color="blue",
    ) as spinner:
        ssh = paramiko.SSHClient()
        # ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        num_attempts = 0
        connection_successful = False
        while num_attempts < 5:
            try:
                ssh.connect(ip, username="ubuntu", key_filename=keyfile, timeout=10)
                connection_successful = True
                break
            except Exception as e:
                num_attempts += 1
                continue
            
        if connection_successful:
            spinner.ok("✅")
        else:
            spinner.fail("⛔")
            exit(1)

        ssh.exec_command("mkdir -p ~/.thunder && chmod 700 ~/.thunder")
        scp = SCPClient(ssh.get_transport())
        scp.put(join(basedir, "token"), remote_path="~/.thunder/token")

        devfile = join(basedir, "dev")
        if os.path.exists(devfile):
            scp.put(devfile, remote_path="~/.thunder/dev")


    if not no_sync:
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
    else:
        click.echo(
            click.style(
                f"✅ Skipping file sync",
                fg="blue",
            )
        )

    click.echo(
        click.style(
            f"⚡ You are connected to a Thunder Compute instance on {ip}! Press control-d to disconnect ⚡",
            fg="cyan",
        )
    )
    
    if no_sync:
        init_dir = '~'
    else:
        init_dir = f'~/{os.path.basename(os.getcwd())}'
    subprocess.run(
        [
            f"ssh ubuntu@{ip} -o StrictHostKeyChecking=accept-new -i {keyfile} -t 'pip install --upgrade tnr --quiet && cd {init_dir} && exec /home/ubuntu/.local/bin/tnr run /bin/bash'"
        ],
        shell=True,
    )
    click.echo(click.style("⚡ Exiting thunder instance ⚡", fg="cyan"))
    
    if not no_sync:
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
