# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: control.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import control_msgs_pb2 as control__msgs__pb2
import config_msgs_pb2 as config__msgs__pb2
import common_msgs_pb2 as common__msgs__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rcontrol.proto\x12\x12Nrmk.IndyFramework\x1a\x12\x63ontrol_msgs.proto\x1a\x11\x63onfig_msgs.proto\x1a\x11\x63ommon_msgs.proto2\xc6-\n\x07\x43ontrol\x12N\n\x0eGetControlInfo\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1f.Nrmk.IndyFramework.ControlInfo\"\x00\x12[\n\x0f\x41\x63tivateIndySDK\x12\".Nrmk.IndyFramework.SDKLicenseInfo\x1a\".Nrmk.IndyFramework.SDKLicenseResp\"\x00\x12\x45\n\x05MoveJ\x12\x1c.Nrmk.IndyFramework.MoveJReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12G\n\x06MoveJT\x12\x1d.Nrmk.IndyFramework.MoveJTReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12\x45\n\x05MoveL\x12\x1c.Nrmk.IndyFramework.MoveLReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12G\n\x06MoveLT\x12\x1d.Nrmk.IndyFramework.MoveLTReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12\x45\n\x05MoveC\x12\x1c.Nrmk.IndyFramework.MoveCReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12G\n\x06MoveCT\x12\x1d.Nrmk.IndyFramework.MoveCTReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12G\n\x06WaitIO\x12\x1d.Nrmk.IndyFramework.WaitIOReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12K\n\x08WaitTime\x12\x1f.Nrmk.IndyFramework.WaitTimeReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12S\n\x0cWaitProgress\x12#.Nrmk.IndyFramework.WaitProgressReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12K\n\x08WaitTraj\x12\x1f.Nrmk.IndyFramework.WaitTrajReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12O\n\nWaitRadius\x12!.Nrmk.IndyFramework.WaitRadiusReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12M\n\tMoveJCond\x12 .Nrmk.IndyFramework.MoveJCondReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12I\n\nStopMotion\x12\x1b.Nrmk.IndyFramework.StopCat\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12K\n\x0bPauseMotion\x12\x1c.Nrmk.IndyFramework.PauseCat\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12N\n\x11SetDirectTeaching\x12\x19.Nrmk.IndyFramework.State\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12N\n\x11SetSimulationMode\x12\x19.Nrmk.IndyFramework.State\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12S\n\x14SetCustomControlMode\x12\x1b.Nrmk.IndyFramework.IntMode\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12P\n\x14GetCustomControlMode\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1b.Nrmk.IndyFramework.IntMode\"\x00\x12T\n\x17SetFrictionCompensation\x12\x19.Nrmk.IndyFramework.State\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12V\n\x1cGetFrictionCompensationState\x12\x19.Nrmk.IndyFramework.Empty\x1a\x19.Nrmk.IndyFramework.State\"\x00\x12\x44\n\x07Recover\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12N\n\x11SetManualRecovery\x12\x19.Nrmk.IndyFramework.State\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12O\n\x10MoveRecoverJoint\x12\x1b.Nrmk.IndyFramework.TargetJ\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12O\n\rSearchProgram\x12\x1b.Nrmk.IndyFramework.Program\x1a\x1f.Nrmk.IndyFramework.ProgramInfo\"\x00\x12J\n\x0bPlayProgram\x12\x1b.Nrmk.IndyFramework.Program\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12I\n\x0cPauseProgram\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12J\n\rResumeProgram\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12H\n\x0bStopProgram\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12\x45\n\tSendAlarm\x12\x1b.Nrmk.IndyFramework.Message\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12J\n\x0eSendAnnotation\x12\x1b.Nrmk.IndyFramework.Message\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12\x61\n\x11PlayTuningProgram\x12!.Nrmk.IndyFramework.TuningProgram\x1a\'.Nrmk.IndyFramework.CollisionThresholds\"\x00\x12`\n\x19SetModbusVariableNameList\x12&.Nrmk.IndyFramework.ModbusVariableList\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12O\n\x13SetVariableNameList\x12\x1b.Nrmk.IndyFramework.AllVars\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12O\n\x13GetVariableNameList\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1b.Nrmk.IndyFramework.AllVars\"\x00\x12J\n\x0eSetIntVariable\x12\x1b.Nrmk.IndyFramework.IntVars\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12J\n\x0eGetIntVariable\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1b.Nrmk.IndyFramework.IntVars\"\x00\x12P\n\x11SetModbusVariable\x12\x1e.Nrmk.IndyFramework.ModbusVars\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12P\n\x11GetModbusVariable\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1e.Nrmk.IndyFramework.ModbusVars\"\x00\x12L\n\x0fSetBoolVariable\x12\x1c.Nrmk.IndyFramework.BoolVars\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12L\n\x0fGetBoolVariable\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1c.Nrmk.IndyFramework.BoolVars\"\x00\x12N\n\x10SetFloatVariable\x12\x1d.Nrmk.IndyFramework.FloatVars\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12N\n\x10GetFloatVariable\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1d.Nrmk.IndyFramework.FloatVars\"\x00\x12L\n\x0fSetJPosVariable\x12\x1c.Nrmk.IndyFramework.JPosVars\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12L\n\x0fGetJPosVariable\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1c.Nrmk.IndyFramework.JPosVars\"\x00\x12L\n\x0fSetTPosVariable\x12\x1c.Nrmk.IndyFramework.TPosVars\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12L\n\x0fGetTPosVariable\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1c.Nrmk.IndyFramework.TPosVars\"\x00\x12i\n\x11InverseKinematics\x12(.Nrmk.IndyFramework.InverseKinematicsReq\x1a(.Nrmk.IndyFramework.InverseKinematicsRes\"\x00\x12~\n\x18\x43heckAproachRetractValid\x12/.Nrmk.IndyFramework.CheckAproachRetractValidReq\x1a/.Nrmk.IndyFramework.CheckAproachRetractValidRes\"\x00\x12l\n\x12GetPalletPointList\x12).Nrmk.IndyFramework.GetPalletPointListReq\x1a).Nrmk.IndyFramework.GetPalletPointListRes\"\x00\x12u\n\x15\x43\x61lculateRelativePose\x12,.Nrmk.IndyFramework.CalculateRelativePoseReq\x1a,.Nrmk.IndyFramework.CalculateRelativePoseRes\"\x00\x12{\n\x17\x43\x61lculateCurrentPoseRel\x12..Nrmk.IndyFramework.CalculateCurrentPoseRelReq\x1a..Nrmk.IndyFramework.CalculateCurrentPoseRelRes\"\x00\x12G\n\rPingFromConty\x12\x19.Nrmk.IndyFramework.Empty\x1a\x19.Nrmk.IndyFramework.Empty\"\x00\x12P\n\x0fGetTeleOpDevice\x12\x19.Nrmk.IndyFramework.Empty\x1a .Nrmk.IndyFramework.TeleOpDevice\"\x00\x12N\n\x0eGetTeleOpState\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1f.Nrmk.IndyFramework.TeleOpState\"\x00\x12W\n\x13\x43onnectTeleOpDevice\x12 .Nrmk.IndyFramework.TeleOpDevice\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12S\n\x16\x44isConnectTeleOpDevice\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12I\n\x0fReadTeleOpInput\x12\x19.Nrmk.IndyFramework.Empty\x1a\x19.Nrmk.IndyFramework.TeleP\"\x00\x12N\n\x0bStartTeleOp\x12\x1f.Nrmk.IndyFramework.TeleOpState\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12G\n\nStopTeleOp\x12\x19.Nrmk.IndyFramework.Empty\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12O\n\x0bSetPlayRate\x12 .Nrmk.IndyFramework.TelePlayRate\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12L\n\x0bGetPlayRate\x12\x19.Nrmk.IndyFramework.Empty\x1a .Nrmk.IndyFramework.TelePlayRate\"\x00\x12R\n\x0fGetTeleFileList\x12\x19.Nrmk.IndyFramework.Empty\x1a\".Nrmk.IndyFramework.TeleOpFileList\"\x00\x12Q\n\x0eSaveTeleMotion\x12\x1f.Nrmk.IndyFramework.TeleFileReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12Q\n\x0eLoadTeleMotion\x12\x1f.Nrmk.IndyFramework.TeleFileReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12S\n\x10\x44\x65leteTeleMotion\x12\x1f.Nrmk.IndyFramework.TeleFileReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12J\n\rEnableTeleKey\x12\x19.Nrmk.IndyFramework.State\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12M\n\tMoveTeleJ\x12 .Nrmk.IndyFramework.MoveTeleJReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12M\n\tMoveTeleL\x12 .Nrmk.IndyFramework.MoveTeleLReq\x1a\x1c.Nrmk.IndyFramework.Response\"\x00\x12H\n\x06MoveFL\x12\x1d.Nrmk.IndyFramework.MoveFLReq\x1a\x1d.Nrmk.IndyFramework.MoveFLRes\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'control_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CONTROL']._serialized_start=96
  _globals['_CONTROL']._serialized_end=5926
# @@protoc_insertion_point(module_scope)
