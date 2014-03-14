#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:slots,utf8strings,new_style
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class Iface(object):
  def remove_server(self, server_id):
    """
    Parameters:
     - server_id
    """
    pass

  def create_event(self, event):
    """
    Parameters:
     - event
    """
    pass

  def remove_event(self, percolate_id):
    """
    Parameters:
     - percolate_id
    """
    pass

  def percolator_hit(self, logline, time, server_id, file_name, hits, search_id):
    """
    Parameters:
     - logline
     - time
     - server_id
     - file_name
     - hits
     - search_id
    """
    pass

  def increment_stat(self, stat_name):
    """
    Parameters:
     - stat_name
    """
    pass


class Client(Iface):
  def __init__(self, iprot, oprot=None):
    self._iprot = self._oprot = iprot
    if oprot is not None:
      self._oprot = oprot
    self._seqid = 0

  def remove_server(self, server_id):
    """
    Parameters:
     - server_id
    """
    self.send_remove_server(server_id)
    return self.recv_remove_server()

  def send_remove_server(self, server_id):
    self._oprot.writeMessageBegin('remove_server', TMessageType.CALL, self._seqid)
    args = remove_server_args()
    args.server_id = server_id
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_remove_server(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = remove_server_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "remove_server failed: unknown result");

  def create_event(self, event):
    """
    Parameters:
     - event
    """
    self.send_create_event(event)
    return self.recv_create_event()

  def send_create_event(self, event):
    self._oprot.writeMessageBegin('create_event', TMessageType.CALL, self._seqid)
    args = create_event_args()
    args.event = event
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_create_event(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = create_event_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "create_event failed: unknown result");

  def remove_event(self, percolate_id):
    """
    Parameters:
     - percolate_id
    """
    self.send_remove_event(percolate_id)
    return self.recv_remove_event()

  def send_remove_event(self, percolate_id):
    self._oprot.writeMessageBegin('remove_event', TMessageType.CALL, self._seqid)
    args = remove_event_args()
    args.percolate_id = percolate_id
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_remove_event(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = remove_event_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "remove_event failed: unknown result");

  def percolator_hit(self, logline, time, server_id, file_name, hits, search_id):
    """
    Parameters:
     - logline
     - time
     - server_id
     - file_name
     - hits
     - search_id
    """
    self.send_percolator_hit(logline, time, server_id, file_name, hits, search_id)

  def send_percolator_hit(self, logline, time, server_id, file_name, hits, search_id):
    self._oprot.writeMessageBegin('percolator_hit', TMessageType.CALL, self._seqid)
    args = percolator_hit_args()
    args.logline = logline
    args.time = time
    args.server_id = server_id
    args.file_name = file_name
    args.hits = hits
    args.search_id = search_id
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()
  def increment_stat(self, stat_name):
    """
    Parameters:
     - stat_name
    """
    self.send_increment_stat(stat_name)

  def send_increment_stat(self, stat_name):
    self._oprot.writeMessageBegin('increment_stat', TMessageType.CALL, self._seqid)
    args = increment_stat_args()
    args.stat_name = stat_name
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["remove_server"] = Processor.process_remove_server
    self._processMap["create_event"] = Processor.process_create_event
    self._processMap["remove_event"] = Processor.process_remove_event
    self._processMap["percolator_hit"] = Processor.process_percolator_hit
    self._processMap["increment_stat"] = Processor.process_increment_stat

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      self._processMap[name](self, seqid, iprot, oprot)
    return True

  def process_remove_server(self, seqid, iprot, oprot):
    args = remove_server_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = remove_server_result()
    result.success = self._handler.remove_server(args.server_id)
    oprot.writeMessageBegin("remove_server", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_create_event(self, seqid, iprot, oprot):
    args = create_event_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = create_event_result()
    result.success = self._handler.create_event(args.event)
    oprot.writeMessageBegin("create_event", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_remove_event(self, seqid, iprot, oprot):
    args = remove_event_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = remove_event_result()
    result.success = self._handler.remove_event(args.percolate_id)
    oprot.writeMessageBegin("remove_event", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_percolator_hit(self, seqid, iprot, oprot):
    args = percolator_hit_args()
    args.read(iprot)
    iprot.readMessageEnd()
    self._handler.percolator_hit(args.logline, args.time, args.server_id, args.file_name, args.hits, args.search_id)
    return

  def process_increment_stat(self, seqid, iprot, oprot):
    args = increment_stat_args()
    args.read(iprot)
    iprot.readMessageEnd()
    self._handler.increment_stat(args.stat_name)
    return


# HELPER FUNCTIONS AND STRUCTURES

class remove_server_args(object):
  """
  Attributes:
   - server_id
  """

  __slots__ = [ 
    'server_id',
   ]

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'server_id', None, None, ), # 1
  )

  def __init__(self, server_id=None,):
    self.server_id = server_id

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.server_id = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('remove_server_args')
    if self.server_id is not None:
      oprot.writeFieldBegin('server_id', TType.I32, 1)
      oprot.writeI32(self.server_id)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)


class remove_server_result(object):
  """
  Attributes:
   - success
  """

  __slots__ = [ 
    'success',
   ]

  thrift_spec = (
    (0, TType.BOOL, 'success', None, None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.BOOL:
          self.success = iprot.readBool();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('remove_server_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.BOOL, 0)
      oprot.writeBool(self.success)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)


class create_event_args(object):
  """
  Attributes:
   - event
  """

  __slots__ = [ 
    'event',
   ]

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'event', (Event, Event.thrift_spec), None, ), # 1
  )

  def __init__(self, event=None,):
    self.event = event

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.event = Event()
          self.event.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('create_event_args')
    if self.event is not None:
      oprot.writeFieldBegin('event', TType.STRUCT, 1)
      self.event.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)


class create_event_result(object):
  """
  Attributes:
   - success
  """

  __slots__ = [ 
    'success',
   ]

  thrift_spec = (
    (0, TType.STRING, 'success', None, None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRING:
          self.success = iprot.readString().decode('utf-8')
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('create_event_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRING, 0)
      oprot.writeString(self.success.encode('utf-8'))
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)


class remove_event_args(object):
  """
  Attributes:
   - percolate_id
  """

  __slots__ = [ 
    'percolate_id',
   ]

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'percolate_id', None, None, ), # 1
  )

  def __init__(self, percolate_id=None,):
    self.percolate_id = percolate_id

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.percolate_id = iprot.readString().decode('utf-8')
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('remove_event_args')
    if self.percolate_id is not None:
      oprot.writeFieldBegin('percolate_id', TType.STRING, 1)
      oprot.writeString(self.percolate_id.encode('utf-8'))
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)


class remove_event_result(object):
  """
  Attributes:
   - success
  """

  __slots__ = [ 
    'success',
   ]

  thrift_spec = (
    (0, TType.BOOL, 'success', None, None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.BOOL:
          self.success = iprot.readBool();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('remove_event_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.BOOL, 0)
      oprot.writeBool(self.success)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)


class percolator_hit_args(object):
  """
  Attributes:
   - logline
   - time
   - server_id
   - file_name
   - hits
   - search_id
  """

  __slots__ = [ 
    'logline',
    'time',
    'server_id',
    'file_name',
    'hits',
    'search_id',
   ]

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'logline', None, None, ), # 1
    (2, TType.STRING, 'time', None, None, ), # 2
    (3, TType.I32, 'server_id', None, None, ), # 3
    (4, TType.STRING, 'file_name', None, None, ), # 4
    (5, TType.SET, 'hits', (TType.STRING,None), None, ), # 5
    (6, TType.STRING, 'search_id', None, None, ), # 6
  )

  def __init__(self, logline=None, time=None, server_id=None, file_name=None, hits=None, search_id=None,):
    self.logline = logline
    self.time = time
    self.server_id = server_id
    self.file_name = file_name
    self.hits = hits
    self.search_id = search_id

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.logline = iprot.readString().decode('utf-8')
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.time = iprot.readString().decode('utf-8')
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.server_id = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.file_name = iprot.readString().decode('utf-8')
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.SET:
          self.hits = set()
          (_etype10, _size7) = iprot.readSetBegin()
          for _i11 in xrange(_size7):
            _elem12 = iprot.readString().decode('utf-8')
            self.hits.add(_elem12)
          iprot.readSetEnd()
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.STRING:
          self.search_id = iprot.readString().decode('utf-8')
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('percolator_hit_args')
    if self.logline is not None:
      oprot.writeFieldBegin('logline', TType.STRING, 1)
      oprot.writeString(self.logline.encode('utf-8'))
      oprot.writeFieldEnd()
    if self.time is not None:
      oprot.writeFieldBegin('time', TType.STRING, 2)
      oprot.writeString(self.time.encode('utf-8'))
      oprot.writeFieldEnd()
    if self.server_id is not None:
      oprot.writeFieldBegin('server_id', TType.I32, 3)
      oprot.writeI32(self.server_id)
      oprot.writeFieldEnd()
    if self.file_name is not None:
      oprot.writeFieldBegin('file_name', TType.STRING, 4)
      oprot.writeString(self.file_name.encode('utf-8'))
      oprot.writeFieldEnd()
    if self.hits is not None:
      oprot.writeFieldBegin('hits', TType.SET, 5)
      oprot.writeSetBegin(TType.STRING, len(self.hits))
      for iter13 in self.hits:
        oprot.writeString(iter13.encode('utf-8'))
      oprot.writeSetEnd()
      oprot.writeFieldEnd()
    if self.search_id is not None:
      oprot.writeFieldBegin('search_id', TType.STRING, 6)
      oprot.writeString(self.search_id.encode('utf-8'))
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)


class increment_stat_args(object):
  """
  Attributes:
   - stat_name
  """

  __slots__ = [ 
    'stat_name',
   ]

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'stat_name', None, None, ), # 1
  )

  def __init__(self, stat_name=None,):
    self.stat_name = stat_name

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.stat_name = iprot.readString().decode('utf-8')
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('increment_stat_args')
    if self.stat_name is not None:
      oprot.writeFieldBegin('stat_name', TType.STRING, 1)
      oprot.writeString(self.stat_name.encode('utf-8'))
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)

