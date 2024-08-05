# coding: utf-8

import logging

LOG_FORMAT = ('%(levelname) -4s %(asctime)s %(name) -4s : %(message)s')


class Moss(object):
  """Moss"""
  
  def __init__(self, conf:str = 'moss.nodes.json', **kwargs):
    """构造一个Moss实例

    Args:
        conf (str, optional): 指定用来构造Moss的配置文件. 默认 'moss.nodes.json'.
        **kwargs (dict, optional):: 
          - name (str, optional): 你可以通过指定name为Moss起一个名字
    """
    
    logging.basicConfig(level=logging.DEBUG,format = LOG_FORMAT)
    self._logger = logging.getLogger(__name__)
    pass
  
  
  def startup(self):
    """启动 Moss"""
    pass
  
  
  def shutdown(self):
    """关闭 Moss"""
    pass
  
  
  def reboot(self):
    """重启 Moss"""
    pass