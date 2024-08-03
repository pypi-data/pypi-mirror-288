import click
from thunder import auth
import sys
import os
from scp import SCPClient
import paramiko
import getpass
import subprocess
from io import StringIO
from multiprocessing import Process, Event

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

    if not api.is_token_valid(id_token):
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
    if device_type is None:
        raise click.UsageError("You must specify a device type, e.g., tnr device v100")

    supported_devices = set(
        [
            "t4",
            "v100",
            "a100",
        ]
    )
    if device_type.lower() not in supported_devices:
        click.echo(
            f"Unsupported device type: {device_type}. Please select one of T4, V100, or A100"
        )
        return

    device_file = os.path.expanduser("~/.thunder/dev")
    with open(device_file, "w") as f:
        f.write(device_type.lower())

    click.echo(f"Device set to {device_type.upper()}")


@cli.command(help="Start running in a thunder container!")
def start():
    # Generate public/private key for session
    # key = paramiko.RSAKey.generate(2048)
    # private_key = StringIO()
    # key.write_private_key(private_key)
    # public_key = f"{key.get_name()} {key.get_base64()}"
    # public_key, private_key.getvalue())
    # print(public_key, private_key)
    # private_key.getvalue(), public_key

    # TODO: Get the ip from the firebase function
    with yaspin(text="Setting up instance", color="blue") as spinner:
        ip = "34.122.72.236"

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip)
        spinner.ok("✅")

    with yaspin(text="Copying current directory over", color="blue") as spinner:
        ssh.exec_command('mkdir -p ~/.thunder && chmod 700 ~/.thunder')
        scp = SCPClient(ssh.get_transport())
        scp.put(os.path.expanduser('~/.thunder/token'), remote_path='~/.thunder/token')
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
    subprocess.run(
        [
            f"ssh {ip} -t 'cd ~/{os.path.basename(os.getcwd())} && exec tnr run /bin/bash'"
        ],
        shell=True,
    )
    click.echo(click.style("⚡ Exiting thunder instance ⚡", fg="cyan"))
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
