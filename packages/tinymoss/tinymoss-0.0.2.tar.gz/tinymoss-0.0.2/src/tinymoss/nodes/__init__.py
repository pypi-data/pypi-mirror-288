# coding : utf-8

import threading
import functools
import logging
import time
import pika
from tinymoss.rabbits import RabbitMQConnection
from pika.exchange_type import ExchangeType
from abc import ABC, abstractmethod
import uuid


class MossNode(threading.Thread, ABC):
  """_summary_

  Args:
      threading (_type_): _description_
  """
  
  def __init__(self, **kwargs):
    
    super(MossNode, self).__init__()
    self._reconnect_delay = 0
    self._amqp_url = 'amqp://admin:123456@localhost:5672/%2F'
    self._connection = RabbitMQConnection(self._amqp_url)
    self._logger = logging.getLogger(__name__)
    self.daemon =  True
    
    self.nodeId = kwargs['node_id'] if 'node_id' in kwargs else str(uuid.uuid4())
    self.services = kwargs['services'] if 'services' in kwargs else []
    list(map(lambda service: self._connection.sub_queue(f'moss_node_{service}', auto_delete=True), self.services))
    self._connection.add_on_message_callback(cb=self._on_messaged)

  
  @abstractmethod
  def on_running(self):
    raise NotImplementedError()
  
  
  @abstractmethod
  def on_messaged(self, route, payload):
    pass
  
  
  def _on_messaged(self, route, payload):
    
    self.on_messaged(route, payload)
  
  
  def pub_to_node(self, node_id:str, payload:str | bytes):
    _q = f'moss_node_{node_id}'
    if self._connection.check_queue(_q):
      self._connection.pub_queue(f'moss_node_{node_id}', payload)
    else:
      print('Trying to send a message to a queue that doesn\'t exist')
  
  
  def run(self):
      
      threading.Thread(target=self.on_running, daemon=True).start()
      while True:
          try:
              self._connection.run()
          except KeyboardInterrupt:
              self._connection.stop()
              break
          self._maybe_reconnect()

  def _maybe_reconnect(self):
      if self._connection.should_reconnect:
          self._connection.stop()
          reconnect_delay = self._get_reconnect_delay()
          self._logger.info('Reconnecting after %d seconds', reconnect_delay)
          time.sleep(reconnect_delay)
          self._connection = RabbitMQConnection(self._amqp_url)

  def _get_reconnect_delay(self):
      if self._connection.was_consuming:
          self._reconnect_delay = 0
      else:
          self._reconnect_delay += 1
      if self._reconnect_delay > 30:
          self._reconnect_delay = 30
      return self._reconnect_delay

  
  