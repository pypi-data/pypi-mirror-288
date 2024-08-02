from .proxies.instance import InstanceProxy, InstanceArgs
from .proxies.target import TargetProxy, TargetArgs
from .proxies.emitter import EmitterProxy, EmitterArgs
from client import RshipExecClient

# Set info

rship_host = "10.147.20.13"
rship_port = "5155"
machine_id = "sdk-example"
machine_name = "SDK Example"
service_id = "example"
service_name = "Example"
instance_name = "Example"
service_type_code = "Example"
color = "#000000"

async def main():
  # Create a new rship client

  client = RshipExecClient(rship_host, rship_port)

  # Add an instance to the client

  instance = client.add_instance(InstanceArgs(
    name=instance_name,
    code=service_type_code,
    service_id=service_id,
    cluster_id="",
    machine_id=machine_id,
    color=color,
    message=""
  ))

  # Add a target to the instance

  target = await instance.add_target(TargetArgs(
    name="Example Target",
    short_id="example-target",
    category="Example"
  ))

  # Connect to rship

  await client.connect()

  print("Connected to rship")

if __name__ == "__main__":
    print("Hello, World!")