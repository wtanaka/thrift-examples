#!/usr/bin/env python
# coding=utf-8
# Copyright (C) 2015 Wesley Tanaka
"""Typecheck behavior in Thrift in Python

Tested with Thrift version 0.9.0

From
http://techblog.ridewithvia.com/post/37118173720
"""
from __future__ import print_function

import sys

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TProtocol
from thrift.protocol import TCompactProtocol

from typecheck.ttypes import Place
from typecheck.ttypes import Point
from typecheck.ttypes import Review

def SerializeThriftMsg(msg, protocol_type=TBinaryProtocol.TBinaryProtocol):
  """Serialize a thrift message using the given protocol.

  The default protocol is binary.

  Args:
      msg: the Thrift object to serialize.
      protocol_type: the Thrift protocol class to use.

  Returns:
      A string of the serialized object.
  """
  msg.validate()
  transportOut = TTransport.TMemoryBuffer()
  protocolOut = protocol_type(transportOut)
  msg.write(protocolOut)
  return transportOut.getvalue()

def DeserializeThriftMsg(msg, data,
    protocol_type=TBinaryProtocol.TBinaryProtocol):
  """Deserialize a thrift message using the given protocol.

  The default protocol is binary.

  Args:
      msg: the Thrift object to serialize.
      data: the data to read from.
      protocol_type: the Thrift protocol class to use.

  Returns:
      Message object passed in (post-parsing).
  """
  transportIn = TTransport.TMemoryBuffer(data)
  protocolIn = protocol_type(transportIn)
  msg.read(protocolIn)
  msg.validate()
  return msg

def main():
  point = Point(x=1.5, y=2.75)
  point.validate()
  SerializeThriftMsg(point)

  point = Point(x=1.5)
  try:
    point.validate()
    assert False
  except TProtocol.TProtocolException as e:
    pass

  point = Point(x=1.5, y="asdf")
  try:
    point.validate()
    print("String was accepted when int was expected", file=sys.stderr)
  except TProtocol.TProtocolException as e:
    pass

  place = Place(name="wtanaka.com", location=Point(x=1.5, y=2.75))
  place.validate()
  SerializeThriftMsg(place)

  place = Place(name="wtanaka.com", location=Point(x=1.5, y=2.75),
      review=Review(rating=4,
          text="4 stars would come again"))
  place.validate()
  SerializeThriftMsg(place)

  place = Place(name="wtanaka.com", location=Point(x=1.5, y=2.75),
      review=Point(x=1.5, y=2.75))
  place.validate()
  print("Point was accepted when Review was expected", file=sys.stderr)
  SerializeThriftMsg(place)

if __name__ == "__main__":
   main()
