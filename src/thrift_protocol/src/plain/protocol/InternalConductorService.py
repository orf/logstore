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
  def percolator_hit(self, logline, time, server_id, file_name, hits):
    """
    Parameters:
     - logline
     - time
     - server_id
     - file_name
     - hits
    """
    pass


class Client(Iface):
  def __init__(self, iprot, oprot=None):
    self._iprot = self._oprot = iprot
    if oprot is not None:
      self._oprot = oprot
    self._seqid = 0

  def percolator_hit(self, logline, time, server_id, file_name, hits):
    """
    Parameters:
     - logline
     - time
     - server_id
     - file_name
     - hits
    """
    self.send_percolator_hit(logline, time, server_id, file_name, hits)

  def send_percolator_hit(self, logline, time, server_id, file_name, hits):
    self._oprot.writeMessageBegin('percolator_hit', TMessageType.CALL, self._seqid)
    args = percolator_hit_args()
    args.logline = logline
    args.time = time
    args.server_id = server_id
    args.file_name = file_name
    args.hits = hits
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["percolator_hit"] = Processor.process_percolator_hit

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

  def process_percolator_hit(self, seqid, iprot, oprot):
    args = percolator_hit_args()
    args.read(iprot)
    iprot.readMessageEnd()
    self._handler.percolator_hit(args.logline, args.time, args.server_id, args.file_name, args.hits)
    return


# HELPER FUNCTIONS AND STRUCTURES

class percolator_hit_args(object):
  """
  Attributes:
   - logline
   - time
   - server_id
   - file_name
   - hits
  """

  __slots__ = [ 
    'logline',
    'time',
    'server_id',
    'file_name',
    'hits',
   ]

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'logline', None, None, ), # 1
    (2, TType.STRING, 'time', None, None, ), # 2
    (3, TType.I32, 'server_id', None, None, ), # 3
    (4, TType.STRING, 'file_name', None, None, ), # 4
    (5, TType.SET, 'hits', (TType.STRING,None), None, ), # 5
  )

  def __init__(self, logline=None, time=None, server_id=None, file_name=None, hits=None,):
    self.logline = logline
    self.time = time
    self.server_id = server_id
    self.file_name = file_name
    self.hits = hits

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

