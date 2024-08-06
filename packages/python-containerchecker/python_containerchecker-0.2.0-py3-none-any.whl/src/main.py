import argparse

from src.config import read_yaml
from src.log_handler import setup_logging
from src.ssh import process_server


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process servers and check for running containers."
    )
    parser.add_argument(
        "--file", type=str, default="servers.yaml", help="Path to servers.yaml"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()

    logger = setup_logging(args.verbose)

    if args.verbose:
        logger.debug("Verbose output enabled")

    servers = read_yaml(args.file)

    if servers is None:
        logger.error(f"Failed to read servers from {args.file}")
        return

    for server in servers.get("servers", []):
        host = server["host"]
        port = server.get("port", 22)
        user = server["user"]
        password = server.get("password")
        ssh_key = server.get("ssh_key")
        ssh_key_password = server.get("ssh_key_password")

        process_server(host, port, user, password, ssh_key, ssh_key_password)


if __name__ == "__main__":
    main()
