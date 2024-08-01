# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ethercat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ethercat_msgs_pb2 as ethercat__msgs__pb2
import common_msgs_pb2 as common__msgs__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x65thercat.proto\x12\x12Nrmk.IndyFramework\x1a\x13\x65thercat_msgs.proto\x1a\x11\x63ommon_msgs.proto2\xb2\x19\n\x08\x45therCAT\x12P\n\x0fGetMasterStatus\x12\x19.Nrmk.IndyFramework.Empty\x1a .Nrmk.IndyFramework.MasterStatus\"\x00\x12N\n\x0eGetSlaveStatus\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1f.Nrmk.IndyFramework.SlaveStatus\"\x00\x12V\n\x11GetRxDomainStatus\x12\x19.Nrmk.IndyFramework.Empty\x1a$.Nrmk.IndyFramework.EcatDomainStatus\"\x00\x12V\n\x11GetTxDomainStatus\x12\x19.Nrmk.IndyFramework.Empty\x1a$.Nrmk.IndyFramework.EcatDomainStatus\"\x00\x12Q\n\rIsSystemReady\x12\x19.Nrmk.IndyFramework.Empty\x1a#.Nrmk.IndyFramework.EcatSystemReady\"\x00\x12I\n\tIsServoOn\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1f.Nrmk.IndyFramework.EcatServoOn\"\x00\x12P\n\x0fGetSlaveTypeNum\x12\x19.Nrmk.IndyFramework.Empty\x1a .Nrmk.IndyFramework.SlaveTypeNum\"\x00\x12L\n\x12ResetOverflowCount\x12\x19.Nrmk.IndyFramework.Empty\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12K\n\nSetServoRx\x12 .Nrmk.IndyFramework.ServoRxIndex\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12K\n\nGetServoRx\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x1b.Nrmk.IndyFramework.ServoRx\"\x00\x12K\n\nGetServoTx\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x1b.Nrmk.IndyFramework.ServoTx\"\x00\x12S\n\x0eSetServoRxKeba\x12$.Nrmk.IndyFramework.ServoRxIndexKeba\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12S\n\x0eGetServoRxKeba\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x1f.Nrmk.IndyFramework.ServoRxKeba\"\x00\x12S\n\x0eGetServoTxKeba\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x1f.Nrmk.IndyFramework.ServoTxKeba\"\x00\x12I\n\nSetServoOn\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12J\n\x0bSetServoOff\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12V\n\x13GetServoTemperature\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x1d.Nrmk.IndyFramework.ServoTemp\"\x00\x12U\n\x11GetServoErrorCode\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x1e.Nrmk.IndyFramework.ServoError\"\x00\x12I\n\nResetServo\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12Q\n\x12SetCOREManualBrake\x12\x1e.Nrmk.IndyFramework.ServoBrake\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12J\n\x0cSetEndtoolRx\x12\x1d.Nrmk.IndyFramework.EndtoolRx\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12J\n\x0cGetEndtoolRx\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1d.Nrmk.IndyFramework.EndtoolRx\"\x00\x12J\n\x0cGetEndtoolTx\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1d.Nrmk.IndyFramework.EndtoolTx\"\x00\x12X\n\x13GetEndtoolDockingTx\x12\x19.Nrmk.IndyFramework.Empty\x1a$.Nrmk.IndyFramework.EndtoolDockingTx\"\x00\x12J\n\x0cSetIOBoardRx\x12\x1d.Nrmk.IndyFramework.IOBoardRx\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12J\n\x0cGetIOBoardTx\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1d.Nrmk.IndyFramework.IOBoardTx\"\x00\x12J\n\x0cGetIOBoardRx\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1d.Nrmk.IndyFramework.IOBoardRx\"\x00\x12L\n\x05GetDI\x12\x1c.Nrmk.IndyFramework.DIOIndex\x1a#.Nrmk.IndyFramework.DIODigitalInput\"\x00\x12M\n\x05GetDO\x12\x1c.Nrmk.IndyFramework.DIOIndex\x1a$.Nrmk.IndyFramework.DIODigitalOutput\"\x00\x12J\n\x05SetDO\x12$.Nrmk.IndyFramework.DIODigitalOutput\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12Q\n\x0fGetMaxTorqueSDO\x12\x1d.Nrmk.IndyFramework.EcatIndex\x1a\x1d.Nrmk.IndyFramework.SDOIntVal\"\x00\x12R\n\x10GetProfileVelSDO\x12\x1d.Nrmk.IndyFramework.EcatIndex\x1a\x1d.Nrmk.IndyFramework.SDOIntVal\"\x00\x12R\n\x10GetProfileAccSDO\x12\x1d.Nrmk.IndyFramework.EcatIndex\x1a\x1d.Nrmk.IndyFramework.SDOIntVal\"\x00\x12R\n\x10GetProfileDecSDO\x12\x1d.Nrmk.IndyFramework.EcatIndex\x1a\x1d.Nrmk.IndyFramework.SDOIntVal\"\x00\x12N\n\x0fSetMaxTorqueSDO\x12\x1e.Nrmk.IndyFramework.ServoParam\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12O\n\x10SetProfileVelSDO\x12\x1e.Nrmk.IndyFramework.ServoParam\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12O\n\x10SetProfileAccSDO\x12\x1e.Nrmk.IndyFramework.ServoParam\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12O\n\x10SetProfileDecSDO\x12\x1e.Nrmk.IndyFramework.ServoParam\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12Y\n\x11GetRobotZeroCount\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\".Nrmk.IndyFramework.RobotZeroCount\"\x00\x12T\n\x15SetRobotZeroAsCurrent\x12\x1e.Nrmk.IndyFramework.ServoIndex\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ethercat_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ETHERCAT']._serialized_start=79
  _globals['_ETHERCAT']._serialized_end=3329
# @@protoc_insertion_point(module_scope)
