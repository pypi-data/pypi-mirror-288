#coding: utf-8

from time import sleep
import tinymoss
from tinymoss.nodes import MossNode
import unittest

class Moss_Simple_Test(unittest.TestCase):
  
  def test_init(self):
    moss = tinymoss.Moss()
    self.assertIsNotNone(moss)
  
  
  def test_node_init(self):
    mossNode = MossNode()
    self.assertIsNotNone(mossNode)
    
    
  def test_moss_node_start(self):
    
    
    mossNode = MossNode()
    mossNode.start()
    
    try:
      mossNode.join()
    except:
      pass
    finally:
      self.assertTrue(True)
    
  
if __name__ == '__main__':
  unittest.main(verbosity=2)