# rpc



## Installation

```bash
pip install rpc
```

## Usage

```python
from embrpc.rpcscp import SCPServer, SCPClient


    class HandControl(BaseModel):
        x: float
        y: float
        z: float
        roll: float
        pitch: float
        yaw: float

    """Feed an LLM output to the robot running a server."""
    client = SCPClient(
        host="10.4.20.28",
        # host="1.2.3.4",
        user="user",
        password="pass",  # noqa: S106
        inbound_model=HandControl,
        outbound_model=HandControl,
        inbound_path="~/data_in.json",
        outbound_path="~/data_out.json",
    )

    client.send_data(HandControl(x=0.1, y=0.2, z=0.3, roll=0.4, pitch=0.5, yaw=0.6))
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
```