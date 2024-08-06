import logging
import warnings

from cryptography.utils import CryptographyDeprecationWarning

with warnings.catch_warnings(action="ignore", category=CryptographyDeprecationWarning):
    import paramiko
from rich import print

from src.constants import console
from src.containers import check_installed_package, display_containers

logger = logging.getLogger("rich")


def create_ssh_client(
    hostname, port, username, password=None, key_filename=None, key_password=None
):
    """Create an SSH client object."""
    logger.debug(f"Creating SSH client for {hostname}")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key_filename:
            # if using rsa keys then need to use RSAKey instead of Ed25519Key
            key = paramiko.Ed25519Key.from_private_key_file(
                key_filename, password=key_password
            )
            ssh.connect(hostname, port, username=username, pkey=key)
        else:
            ssh.connect(hostname, port, username=username, password=password)
        return ssh
    except paramiko.AuthenticationException as e:
        logger.exception(f"Authentication failed: {e}")
    except paramiko.SSHException as e:
        logger.exception(f"SSH connection failed: {e}")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    return None


def process_server(host, port, user, password, ssh_key, ssh_key_password):
    """Process a server."""
    logger.debug(f"Processing server: {host}")
    try:
        ssh_client = create_ssh_client(
            host, port, user, password, ssh_key, ssh_key_password
        )

        if ssh_client is None:
            console.print(f"Failed to connect to {host}")
            return

        if check_installed_package(ssh_client, "podman"):
            display_containers(ssh_client, "podman", host)
        elif check_installed_package(ssh_client, "docker"):
            display_containers(ssh_client, "docker", host)
        else:
            print(
                f"Neither Podman nor Docker is installed on [bold yellow]{host}[/bold yellow]."
            )

    except Exception as e:
        logger.exception(f"Failed to connect to {host}: {e}")
    finally:
        if "ssh_client" in locals() and ssh_client:
            ssh_client.close()
