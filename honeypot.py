#!/usr/bin/env python

# importing libraries
import argparse
import threading
import socket
import sys
from os.path import isfile
import traceback
import logging
import json
import paramiko
from paramiko.rsakey import RSAKey

# init SSH banner
SSH_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-Not-a-Honeypot-4ubuntu0.1"

HOST_KEY = None

# init arrow keys character sequence, to filter them out
UP_KEY = "\x1b[A".encode()
DOWN_KEY = "\x1b[B".encode()
RIGHT_KEY = "\x1b[C".encode()
LEFT_KEY = "\x1b[D".encode()
BACK_KEY = "\x7f".encode()

# init logger for logging all activity
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="ssh-honeypot.log",
)


def handle_cmd(cmd, chan, ip):
    """the function handling the different commands sent to the SSH server"""
    response = ""
    cmd = cmd.strip()
    cmds = []
    if isfile("cmd-directory.json"):
        file = open("cmd-directory.json")
        cmds = json.load(file)["commands"]
    else:
        raise Exception("Command directory file not found!")
    if cmd in cmds:
        response = cmds[cmd]
    else:
        response = f"sh: 1: {cmd.split()[0]}: not found"

    if response != "":
        logging.info("Response from honeypot ({}): ".format(ip, response))
        response = response + "\r\n"
    chan.send(response)


class SshHoneypot(paramiko.ServerInterface):
    """the custom implementation of the Paramiko SSH server"""

    client_ip = None

    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        """determine if a channel request of a given type will be granted, called in server when the client requests a channel, after authentication is complete"""

        logging.info(
            "client called check_channel_request ({}): {}".format(self.client_ip, kind)
        )
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED

    def get_allowed_auths(self, username):
        """return a list of authentication methods supported by the server"""

        logging.info(
            "client called get_allowed_auths ({}) with username {}".format(
                self.client_ip, username
            )
        )
        return "password"

    def check_auth_password(self, username, password):
        """determine if a given username and password supplied by the client is acceptable for use in authentication"""

        # Accept all passwords as valid by default
        logging.info(
            "new client credentials ({}): username: {}, password: {}".format(
                self.client_ip, username, password
            )
        )
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        """determine if a shell will be provided to the client on the given channel"""

        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        """determine if a pseudo-terminal of the given dimensions (usually requested for shell access) can be provided on the given channel"""

        return True

    def check_channel_exec_request(self, channel, command):
        """determine if a shell command will be executed for the client"""

        command_text = str(command.decode("utf-8"))

        logging.info(
            "client sent command via check_channel_exec_request ({}): {}".format(
                self.client_ip, command_text
            )
        )
        return True


def handle_connection(client, addr):
    """the function handling the new client connections to the SSH server"""

    client_ip = addr[0]
    logging.info("New connection from: {}".format(client_ip))
    print("New connection is here from: {}".format(client_ip))

    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        # changing banner to appear more convincing
        transport.local_version = SSH_BANNER
        server = SshHoneypot(client_ip)
        try:
            transport.start_server(server=server)

        except paramiko.SSHException:
            print("*** SSH negotiation failed.")
            raise Exception("SSH negotiation failed")

        # waiting 30 seconds for auth to complete
        chan = transport.accept(60)
        if chan is None:
            print("*** No channel (from " + client_ip + ").")
            raise Exception("No channel")

        chan.settimeout(None)

        if transport.remote_mac != "":
            logging.info("Client mac ({}): {}".format(client_ip, transport.remote_mac))

        if transport.remote_compression != "":
            logging.info(
                "Client compression ({}): {}".format(
                    client_ip, transport.remote_compression
                )
            )

        if transport.remote_version != "":
            logging.info(
                "Client SSH version ({}): {}".format(
                    client_ip, transport.remote_version
                )
            )

        if transport.remote_cipher != "":
            logging.info(
                "Client SSH cipher ({}): {}".format(client_ip, transport.remote_cipher)
            )

        server.event.wait(10)
        if not server.event.is_set():
            logging.info("** Client ({}): never asked for a shell".format(client_ip))
            raise Exception("No shell request")

        try:
            # sending a convincing MOTD to the client
            chan.send(
                f"{'*'*25}\n\rWelcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-128-generic x86_64)\n\rPlease rest assured you are NOT in a Honeypot Server :)\n\r{'*'*25}\r\n\r\n"
            )
            run = True
            while run:
                chan.send("$ ")
                command = ""
                while not command.endswith("\r"):
                    transport = chan.recv(1024)
                    print(client_ip + "- received:", transport)
                    # echo input to pseudo-simulate a basic terminal
                    if (
                        transport != UP_KEY
                        and transport != DOWN_KEY
                        and transport != LEFT_KEY
                        and transport != RIGHT_KEY
                        and transport != BACK_KEY
                    ):
                        chan.send(transport)
                        command += transport.decode("utf-8")

                chan.send("\r\n")
                command = command.rstrip()
                logging.info("Command received ({}): {}".format(client_ip, command))
                # handling commands to the SSH server
                if command == "exit":
                    print(f"Connection closed (via exit command) from: {client_ip}")
                    logging.info(
                        "Connection closed (via exit command): " + client_ip + "\n"
                    )
                    run = False

                else:
                    handle_cmd(command, chan, client_ip)

        except Exception as err:
            print("!!! Exception: {}: {}".format(err.__class__, err))
            try:
                transport.close()
            except Exception:
                pass

        chan.close()

    except Exception as err:
        print("!!! Exception: {}: {}".format(err.__class__, err))
        try:
            transport.close()
        except Exception:
            pass


threads = []


def start_server(port, bind):
    """init and run the ssh server"""

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind, port))
    except Exception as err:
        print("*** Bind failed: {}".format(err))
        traceback.print_exc()
        sys.exit(1)
    # using multi-threading to handle parallel connections
    while True:
        try:
            sock.listen(100)
            print("Listening for connection on port {} ...".format(port))
            client, addr = sock.accept()
        except Exception as err:
            print("*** Listen/accept failed: {}".format(err))
            traceback.print_exc()
        new_thread = threading.Thread(target=handle_connection, args=(client, addr))
        new_thread.daemon = True
        new_thread.start()
        threads.append(new_thread)


if __name__ == "__main__":
    # parse arguments passed to the executable
    parser = argparse.ArgumentParser(description="Run an SSH Honeypot Server")
    parser.add_argument(
        "--port",
        "-p",
        help="The port to bind the ssh server to (default: 2222)",
        default=2222,
        type=int,
        action="store",
    )
    parser.add_argument(
        "--bind",
        "-b",
        help="The address to bind the ssh server to (default: 0.0.0.0)",
        default="0.0.0.0",
        type=str,
        action="store",
    )
    args = parser.parse_args()
    # check for a server private key, if not generate a new one
    try:
        if isfile("server.key"):
            print("Server RSA key found")
            HOST_KEY = RSAKey(filename="server.key")
        else:
            print("No RSA key found, creating one")
            HOST_KEY = RSAKey.generate(bits=2048)
            HOST_KEY.write_private_key_file(filename="server.key")
        start_server(args.port, args.bind)
    except KeyboardInterrupt as e:
        print("\r\nExiting program through keyboard interrupt.")
        sys.exit(0)
