from ..models import Action

from typing import Callable, Dict

class ActionArgs():
  def __init__(self, name: str, short_id: str, schema):
    self.name = name
    self.short_id = short_id
    self.schema = schema

class ActionProxy():
  def __init__(self, target_proxy, args:ActionArgs, client, handler: Callable[[ActionArgs, Dict], None]):
    self.target = target_proxy
    self.args = args
    self.client = client
    self.handler = handler


  async def save(self):
    action = Action(
      id=self.id(),
      name=self.args.name,
      schema=self.args.schema,
      target_id=self.target.id(),
      service_id=self.target.instance.args.service_id,
    )
    
    await self.client.set_data(action, 'Action')
    

  def id(self) -> str:
    return f"{self.target.instance.args.service_id}:{self.target.args.short_id}:{self.args.short_id}"
  
  async def take(self, data: any):
    self.handler(self.args, data)