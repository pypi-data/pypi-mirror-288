import logging
import os
import time
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Callable, Type

import paramiko
from mbodied.types.motion.control import HandControl, Pose
from pydantic import BaseModel
from rich.logging import RichHandler
from scp import SCPClient as SCPClientLib

from embrpc.rpc import AbstractClientServer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(RichHandler())

def backoff_hdlr(details) -> None:
    logging.info(f"Retrying {details['tries']} times.")



class SCPClient(AbstractClientServer):
    """Communicates with a remote server via SSH and SCP."""

    def __init__(self, 
        host: str,
        user: str,
        password: str,
        port: int = 22,
        inbound_path="~/data_in.json",
        outbound_path="~/data_out.json",
        key_path: str = None,
        inbound_model: Type[BaseModel] = None,
        outbound_model: Type[BaseModel] = None,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.ssh = None
        self.printed = False
        self.key_path = key_path
        self.inbound_path = inbound_path
        self.outbound_path = outbound_path

        self.inbound_model = inbound_model
        self.outbound_model = outbound_model
        super().__init__(default_model=outbound_model)

    def _connect(self):
        self.ssh = paramiko.SSHClient()
        if self.key_path is not None:
            self.ssh.load_system_host_keys()
            self.ssh.load_host_keys(self.key_path)
        else:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, self.port, self.user, self.password)

    def _send_data(self, data: BaseModel) -> None:
        with SCPClientLib(self.ssh.get_transport()) as scp, NamedTemporaryFile(mode="w", delete=True) as f:
            f.write(data.model_dump_json(round_trip=True))
            scp.put(f.name, self.outbound_path)
        logging.info(f"File {f.name} sent.")

    def _recieve_data(self) -> str:
        with SCPClientLib(self.ssh.get_transport()) as scp, NamedTemporaryFile(delete=True) as f:
            scp.get(self.inbound_path, f.name)
            if not self.printed:
                logging.info(f"File {self.remote_path} recieved.")
                self.printed = True
            return self.inbound_model.model_validate_json(f.read())
        
    def is_resource_available(self) -> bool:
        return True
        


    def close(self) -> None:
        self.ssh.close()


class SCPServer(AbstractClientServer):
    def __init__(self, inbound_path: str, outbound_path: str,inbound_model: Type[BaseModel], outbound_model: Type[BaseModel]) -> None:
        self.inbound_path: str = inbound_path
        self.outbound_path: str = inbound_path
        self.inbound_model: Type[BaseModel] = inbound_model
        self.outbound_model: Type[BaseModel] = outbound_model


    def is_resource_available(self) -> bool:
        return Path(self.inbound_path).exists()
    
    def _reset_resource(self) -> None:
        if Path(self.inbound_path).exists():
            Path(self.inbound_path).unlink()

    def handle_request(self, message) -> BaseModel:
        return self.model.model_validate_json(message)

    def respond(self, message: BaseModel) -> None:
        with Path(self.outbound_path).open("w") as f:
            f.write(message.model_dump_json(round_trip=True))
        logging.info(f"File {self.outbound_path} written.")

   


if __name__ == "__main__":
    client = SCPClient(
        # host="10.4.20.28",
        host="64.247.206.58",
        user="user",
        password="granny12c",  # noqa: S106
        inbound_model=HandControl,
        outbound_model=HandControl,
        inbound_path="~/data_in.json",
        outbound_path="~/data_out.json",
    )
    client.send_data(HandControl(pose=Pose(x=0.1, y=0.1, z=0.1, roll=0.1, pitch=0.1, yaw=0.1)))
    data = client.receive_data()
    logging.info(data)

    locobot_server = SCPServer(
        inbound_path="~/data_in.json",
        outbound_path="~/data_out.json",
        inbound_model=HandControl,
        outbound_model=HandControl,
    )
    execute = lambda x: print(f"Executing {x}")
    locobot_server.poll(execute)