# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: control_msgs.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import device_msgs_pb2 as device__msgs__pb2
import common_msgs_pb2 as common__msgs__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x63ontrol_msgs.proto\x12\x12Nrmk.IndyFramework\x1a\x11\x64\x65vice_msgs.proto\x1a\x11\x63ommon_msgs.proto\"k\n\x0b\x43ontrolInfo\x12\x17\n\x0f\x63ontrol_version\x18\x01 \x01(\t\x12\x13\n\x0brobot_model\x18\x02 \x01(\t\x12.\n\x08response\x18\x64 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\":\n\x0eSDKLicenseInfo\x12\x13\n\x0blicense_key\x18\x01 \x01(\t\x12\x13\n\x0b\x65xpire_date\x18\x02 \x01(\t\"S\n\x0eSDKLicenseResp\x12\x11\n\tactivated\x18\x01 \x01(\x08\x12.\n\x08response\x18\x64 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\"\xc1\x02\n\x11VariableCondition\x12/\n\x06i_vars\x18\x01 \x03(\x0b\x32\x1f.Nrmk.IndyFramework.IntVariable\x12\x31\n\x06\x66_vars\x18\x02 \x03(\x0b\x32!.Nrmk.IndyFramework.FloatVariable\x12\x30\n\x06\x62_vars\x18\x03 \x03(\x0b\x32 .Nrmk.IndyFramework.BoolVariable\x12\x32\n\x06m_vars\x18\x04 \x03(\x0b\x32\".Nrmk.IndyFramework.ModbusVariable\x12\x30\n\x06j_vars\x18\x05 \x03(\x0b\x32 .Nrmk.IndyFramework.JPosVariable\x12\x30\n\x06t_vars\x18\x06 \x03(\x0b\x32 .Nrmk.IndyFramework.TPosVariable\"o\n\x0bIOCondition\x12-\n\x02\x64i\x18\x01 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x31\n\x06\x65nd_di\x18\x02 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\"\x96\x03\n\x0fMotionCondition\x12\x44\n\ttype_cond\x18\x01 \x01(\x0e\x32\x31.Nrmk.IndyFramework.MotionCondition.ConditionType\x12\x44\n\ntype_react\x18\x02 \x01(\x0e\x32\x30.Nrmk.IndyFramework.MotionCondition.ReactionType\x12\x12\n\nconst_cond\x18\x03 \x01(\x08\x12\x30\n\x07io_cond\x18\x04 \x01(\x0b\x32\x1f.Nrmk.IndyFramework.IOCondition\x12\x37\n\x08var_cond\x18\x05 \x01(\x0b\x32%.Nrmk.IndyFramework.VariableCondition\":\n\rConditionType\x12\x0e\n\nCONST_COND\x10\x00\x12\x0b\n\x07IO_COND\x10\x01\x12\x0c\n\x08VAR_COND\x10\x02\"<\n\x0cReactionType\x12\r\n\tNONE_COND\x10\x00\x12\r\n\tSTOP_COND\x10\x01\x12\x0e\n\nPAUSE_COND\x10\x02\"\x8b\x01\n\x0c\x42lendingType\x12\x33\n\x04type\x18\x01 \x01(\x0e\x32%.Nrmk.IndyFramework.BlendingType.Type\x12\x17\n\x0f\x62lending_radius\x18\x02 \x01(\x02\"-\n\x04Type\x12\x08\n\x04NONE\x10\x00\x12\x0c\n\x08OVERRIDE\x10\x01\x12\r\n\tDUPLICATE\x10\x02\"b\n\x07TargetJ\x12\x0f\n\x07j_start\x18\x01 \x03(\x02\x12\x10\n\x08j_target\x18\x02 \x03(\x02\x12\x34\n\tbase_type\x18\x03 \x01(\x0e\x32!.Nrmk.IndyFramework.JointBaseType\"\xe5\x01\n\x08MoveJReq\x12+\n\x06target\x18\x01 \x01(\x0b\x32\x1b.Nrmk.IndyFramework.TargetJ\x12\x32\n\x08\x62lending\x18\x02 \x01(\x0b\x32 .Nrmk.IndyFramework.BlendingType\x12\x11\n\tvel_ratio\x18\x03 \x01(\x02\x12\x11\n\tacc_ratio\x18\x04 \x01(\x02\x12;\n\x0epost_condition\x18\x14 \x01(\x0b\x32#.Nrmk.IndyFramework.MotionCondition\x12\x15\n\rteaching_mode\x18\x1e \x01(\x08\"\xe9\x01\n\x0cMoveJCondReq\x12+\n\x06target\x18\x01 \x01(\x0b\x32\x1b.Nrmk.IndyFramework.TargetJ\x12\x32\n\x08\x62lending\x18\x02 \x01(\x0b\x32 .Nrmk.IndyFramework.BlendingType\x12\x11\n\tvel_ratio\x18\x03 \x01(\x02\x12\x11\n\tacc_ratio\x18\x04 \x01(\x02\x12;\n\x0epost_condition\x18\x14 \x01(\x0b\x32#.Nrmk.IndyFramework.MotionCondition\x12\x15\n\rteaching_mode\x18\x1e \x01(\x08\"\xb7\x01\n\tMoveJTReq\x12+\n\x06target\x18\x01 \x01(\x0b\x32\x1b.Nrmk.IndyFramework.TargetJ\x12\x32\n\x08\x62lending\x18\x02 \x01(\x0b\x32 .Nrmk.IndyFramework.BlendingType\x12\x0c\n\x04time\x18\x03 \x01(\x02\x12;\n\x0epost_condition\x18\x14 \x01(\x0b\x32#.Nrmk.IndyFramework.MotionCondition\"a\n\x07TargetP\x12\x0f\n\x07t_start\x18\x01 \x03(\x02\x12\x10\n\x08t_target\x18\x02 \x03(\x02\x12\x33\n\tbase_type\x18\x03 \x01(\x0e\x32 .Nrmk.IndyFramework.TaskBaseType\"o\n\x07TargetC\x12\x0f\n\x07t_start\x18\x01 \x03(\x02\x12\x0e\n\x06t_pos0\x18\x02 \x03(\x02\x12\x0e\n\x06t_pos1\x18\x03 \x03(\x02\x12\x33\n\tbase_type\x18\x04 \x01(\x0e\x32 .Nrmk.IndyFramework.TaskBaseType\"\x9d\x02\n\x08MoveLReq\x12+\n\x06target\x18\x01 \x01(\x0b\x32\x1b.Nrmk.IndyFramework.TargetP\x12\x32\n\x08\x62lending\x18\x02 \x01(\x0b\x32 .Nrmk.IndyFramework.BlendingType\x12\x11\n\tvel_ratio\x18\x03 \x01(\x02\x12\x11\n\tacc_ratio\x18\x04 \x01(\x02\x12\x36\n\x08vel_type\x18\x05 \x01(\x0e\x32$.Nrmk.IndyFramework.VelocityModeType\x12;\n\x0epost_condition\x18\x14 \x01(\x0b\x32#.Nrmk.IndyFramework.MotionCondition\x12\x15\n\rteaching_mode\x18\x1e \x01(\x08\"\xb7\x01\n\tMoveLTReq\x12+\n\x06target\x18\x01 \x01(\x0b\x32\x1b.Nrmk.IndyFramework.TargetP\x12\x32\n\x08\x62lending\x18\x02 \x01(\x0b\x32 .Nrmk.IndyFramework.BlendingType\x12\x0c\n\x04time\x18\x03 \x01(\x02\x12;\n\x0epost_condition\x18\x14 \x01(\x0b\x32#.Nrmk.IndyFramework.MotionCondition\"\xa6\x03\n\x08MoveCReq\x12+\n\x06target\x18\x01 \x01(\x0b\x32\x1b.Nrmk.IndyFramework.TargetC\x12\x32\n\x08\x62lending\x18\x02 \x01(\x0b\x32 .Nrmk.IndyFramework.BlendingType\x12\r\n\x05\x61ngle\x18\x03 \x01(\x02\x12=\n\x0csetting_type\x18\n \x01(\x0e\x32\'.Nrmk.IndyFramework.CircularSettingType\x12\x39\n\tmove_type\x18\x0b \x01(\x0e\x32&.Nrmk.IndyFramework.CircularMovingType\x12\x11\n\tvel_ratio\x18\x14 \x01(\x02\x12\x11\n\tacc_ratio\x18\x15 \x01(\x02\x12\x36\n\x08vel_type\x18\x16 \x01(\x0e\x32$.Nrmk.IndyFramework.VelocityModeType\x12;\n\x0epost_condition\x18\x19 \x01(\x0b\x32#.Nrmk.IndyFramework.MotionCondition\x12\x15\n\rteaching_mode\x18\x1e \x01(\x08\"\xc0\x02\n\tMoveCTReq\x12+\n\x06target\x18\x01 \x01(\x0b\x32\x1b.Nrmk.IndyFramework.TargetC\x12\x32\n\x08\x62lending\x18\x02 \x01(\x0b\x32 .Nrmk.IndyFramework.BlendingType\x12\r\n\x05\x61ngle\x18\x03 \x01(\x02\x12=\n\x0csetting_type\x18\n \x01(\x0e\x32\'.Nrmk.IndyFramework.CircularSettingType\x12\x39\n\tmove_type\x18\x0b \x01(\x0e\x32&.Nrmk.IndyFramework.CircularMovingType\x12\x0c\n\x04time\x18\x14 \x01(\x02\x12;\n\x0epost_condition\x18\x19 \x01(\x0b\x32#.Nrmk.IndyFramework.MotionCondition\"\xde\x03\n\tWaitIOReq\x12\x32\n\x07\x64i_list\x18\x01 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x32\n\x07\x64o_list\x18\x02 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x36\n\x0b\x65nd_di_list\x18\x03 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x36\n\x0b\x65nd_do_list\x18\x04 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x13\n\x0b\x63onjunction\x18\x05 \x01(\x05\x12\x36\n\x0bset_do_list\x18\x06 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12:\n\x0fset_end_do_list\x18\x07 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x35\n\x0bset_ao_list\x18\x08 \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\x12\x39\n\x0fset_end_ao_list\x18\t \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\"\x81\x02\n\x0bWaitTimeReq\x12\x0c\n\x04time\x18\x01 \x01(\x02\x12\x36\n\x0bset_do_list\x18\x02 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12:\n\x0fset_end_do_list\x18\x03 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x35\n\x0bset_ao_list\x18\x04 \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\x12\x39\n\x0fset_end_ao_list\x18\x05 \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\"\x89\x02\n\x0fWaitProgressReq\x12\x10\n\x08progress\x18\x01 \x01(\x05\x12\x36\n\x0bset_do_list\x18\x02 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12:\n\x0fset_end_do_list\x18\x03 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x35\n\x0bset_ao_list\x18\x04 \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\x12\x39\n\x0fset_end_ao_list\x18\x05 \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\"\xae\x02\n\x0bWaitTrajReq\x12\x39\n\x0etraj_condition\x18\x01 \x01(\x0e\x32!.Nrmk.IndyFramework.TrajCondition\x12\x36\n\x0bset_do_list\x18\x02 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12:\n\x0fset_end_do_list\x18\x03 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x35\n\x0bset_ao_list\x18\x04 \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\x12\x39\n\x0fset_end_ao_list\x18\x05 \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\"\x85\x02\n\rWaitRadiusReq\x12\x0e\n\x06radius\x18\x01 \x01(\x05\x12\x36\n\x0bset_do_list\x18\x02 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12:\n\x0fset_end_do_list\x18\x03 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x35\n\x0bset_ao_list\x18\x04 \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\x12\x39\n\x0fset_end_ao_list\x18\x05 \x03(\x0b\x32 .Nrmk.IndyFramework.AnalogSignal\".\n\x07Program\x12\x11\n\tprog_name\x18\x01 \x01(\t\x12\x10\n\x08prog_idx\x18\x02 \x01(\x05\"\xc3\x01\n\rTuningProgram\x12,\n\x07program\x18\x01 \x01(\x0b\x32\x1b.Nrmk.IndyFramework.Program\x12\x35\n\x0ctuning_space\x18\x02 \x01(\x0e\x32\x1f.Nrmk.IndyFramework.TuningSpace\x12\x36\n\tprecision\x18\x03 \x01(\x0e\x32#.Nrmk.IndyFramework.TuningPrecision\x12\x15\n\rvel_level_max\x18\x04 \x01(\r\"<\n\x0bProgramInfo\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x04\x12\x11\n\ttimestamp\x18\x03 \x01(\t\"I\n\x08Variable\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x61\x64\x64r\x18\x02 \x01(\x05\x12\x0c\n\x04type\x18\x03 \x01(\t\x12\x13\n\x0bin_watching\x18\x04 \x01(\x08\"*\n\x0bIntVariable\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x03\"\xcf\x01\n\x0eModbusVariable\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x61\x64\x64r\x18\x02 \x01(\x05\x12\r\n\x05value\x18\x03 \x01(\x05\x12\x42\n\x0bsignal_type\x18\x04 \x01(\x0e\x32-.Nrmk.IndyFramework.ModbusVariable.SignalType\"N\n\nSignalType\x12\x0c\n\x08ReadCoil\x10\x00\x12\r\n\tWriteCoil\x10\x01\x12\x10\n\x0cReadRegister\x10\x02\x12\x11\n\rWriteRegister\x10\x03\"+\n\x0c\x42oolVariable\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x08\",\n\rFloatVariable\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x02\"*\n\x0cJPosVariable\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x01(\x05\x12\x0c\n\x04jpos\x18\x02 \x03(\x02\"*\n\x0cTPosVariable\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x01(\x05\x12\x0c\n\x04tpos\x18\x02 \x03(\x02\"x\n\x0cModbusServer\x12\x13\n\x0bserver_name\x18\x01 \x01(\t\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\x12\x39\n\rvariable_list\x18\x04 \x03(\x0b\x32\".Nrmk.IndyFramework.ModbusVariable\"P\n\x12ModbusVariableList\x12:\n\x10modbus_variables\x18\x01 \x03(\x0b\x32 .Nrmk.IndyFramework.ModbusServer\":\n\x07\x41llVars\x12/\n\tvariables\x18\x01 \x03(\x0b\x32\x1c.Nrmk.IndyFramework.Variable\"=\n\x07IntVars\x12\x32\n\tvariables\x18\x01 \x03(\x0b\x32\x1f.Nrmk.IndyFramework.IntVariable\"C\n\nModbusVars\x12\x35\n\tvariables\x18\x01 \x03(\x0b\x32\".Nrmk.IndyFramework.ModbusVariable\"?\n\x08\x42oolVars\x12\x33\n\tvariables\x18\x01 \x03(\x0b\x32 .Nrmk.IndyFramework.BoolVariable\"A\n\tFloatVars\x12\x34\n\tvariables\x18\x01 \x03(\x0b\x32!.Nrmk.IndyFramework.FloatVariable\"?\n\x08JPosVars\x12\x33\n\tvariables\x18\x01 \x03(\x0b\x32 .Nrmk.IndyFramework.JPosVariable\"?\n\x08TPosVars\x12\x33\n\tvariables\x18\x01 \x03(\x0b\x32 .Nrmk.IndyFramework.TPosVariable\"7\n\x14InverseKinematicsReq\x12\x0c\n\x04tpos\x18\x01 \x03(\x02\x12\x11\n\tinit_jpos\x18\x02 \x03(\x02\"T\n\x14InverseKinematicsRes\x12\x0c\n\x04jpos\x18\x01 \x03(\x02\x12.\n\x08response\x18\x64 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\"c\n\x1b\x43heckAproachRetractValidReq\x12\x0c\n\x04tpos\x18\x01 \x03(\x02\x12\x11\n\tinit_jpos\x18\x02 \x03(\x02\x12\x10\n\x08pre_tpos\x18\x03 \x03(\x02\x12\x11\n\tpost_tpos\x18\x04 \x03(\x02\"\x9b\x01\n\x1b\x43heckAproachRetractValidRes\x12\x10\n\x08is_valid\x18\x01 \x01(\x08\x12\x0f\n\x07tar_pos\x18\x02 \x03(\x02\x12\x14\n\x0c\x61pproach_pos\x18\x03 \x03(\x02\x12\x13\n\x0bretract_pos\x18\x04 \x03(\x02\x12.\n\x08response\x18\x64 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\"\x8f\x01\n\x15GetPalletPointListReq\x12\x0c\n\x04tpos\x18\x01 \x03(\x02\x12\x0c\n\x04jpos\x18\x02 \x03(\x02\x12\x10\n\x08pre_tpos\x18\x03 \x03(\x02\x12\x11\n\tpost_tpos\x18\x04 \x03(\x02\x12\x16\n\x0epallet_pattern\x18\x05 \x01(\x05\x12\r\n\x05width\x18\x06 \x01(\x05\x12\x0e\n\x06height\x18\x07 \x01(\x05\"[\n\x0bPalletPoint\x12\x0f\n\x07tar_pos\x18\x01 \x03(\x02\x12\x14\n\x0c\x61pproach_pos\x18\x02 \x03(\x02\x12\x13\n\x0bretract_pos\x18\x03 \x03(\x02\x12\x10\n\x08tar_jpos\x18\x04 \x03(\x02\"\x7f\n\x15GetPalletPointListRes\x12\x36\n\rpallet_points\x18\x01 \x03(\x0b\x32\x1f.Nrmk.IndyFramework.PalletPoint\x12.\n\x08response\x18\x64 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\"s\n\x18\x43\x61lculateRelativePoseReq\x12\x11\n\tstart_pos\x18\x01 \x03(\x02\x12\x0f\n\x07\x65nd_pos\x18\x02 \x03(\x02\x12\x33\n\tbase_type\x18\x03 \x01(\x0e\x32 .Nrmk.IndyFramework.TaskBaseType\"`\n\x18\x43\x61lculateRelativePoseRes\x12\x14\n\x0crelative_pos\x18\x01 \x03(\x02\x12.\n\x08response\x18\x64 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\"|\n\x1a\x43\x61lculateCurrentPoseRelReq\x12\x13\n\x0b\x63urrent_pos\x18\x01 \x03(\x02\x12\x14\n\x0crelative_pos\x18\x02 \x03(\x02\x12\x33\n\tbase_type\x18\x03 \x01(\x0e\x32 .Nrmk.IndyFramework.TaskBaseType\"d\n\x1a\x43\x61lculateCurrentPoseRelRes\x12\x16\n\x0e\x63\x61lculated_pos\x18\x01 \x03(\x02\x12.\n\x08response\x18\x64 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\"\xb2\x01\n\x0cTeleOpDevice\x12\x0c\n\x04name\x18\x01 \x01(\t\x12?\n\x04type\x18\x02 \x01(\x0e\x32\x31.Nrmk.IndyFramework.TeleOpDevice.TeleOpDeviceType\x12\n\n\x02ip\x18\x03 \x01(\t\x12\x0c\n\x04port\x18\x04 \x01(\r\x12\x11\n\tconnected\x18\x05 \x01(\x08\"&\n\x10TeleOpDeviceType\x12\x08\n\x04NONE\x10\x00\x12\x08\n\x04VIVE\x10\x01\"i\n\x0bTeleOpState\x12*\n\x04mode\x18\x01 \x01(\x0e\x32\x1c.Nrmk.IndyFramework.TeleMode\x12.\n\x06method\x18\x02 \x01(\x0e\x32\x1e.Nrmk.IndyFramework.TeleMethod\"E\n\x05TeleP\x12\x0c\n\x04tpos\x18\x01 \x03(\x02\x12.\n\x08response\x18\x64 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\"O\n\x0eTeleOpFileList\x12\r\n\x05\x66iles\x18\x01 \x03(\t\x12.\n\x08response\x18\x64 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\"\x1b\n\x0bTeleFileReq\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1c\n\x0cTelePlayRate\x12\x0c\n\x04rate\x18\x01 \x01(\x02\"r\n\x0cMoveTeleJReq\x12\x0c\n\x04jpos\x18\x01 \x03(\x02\x12\x11\n\tvel_ratio\x18\x02 \x01(\x02\x12\x11\n\tacc_ratio\x18\x03 \x01(\x02\x12.\n\x06method\x18\n \x01(\x0e\x32\x1e.Nrmk.IndyFramework.TeleMethod\"r\n\x0cMoveTeleLReq\x12\x0c\n\x04tpos\x18\x01 \x03(\x02\x12\x11\n\tvel_ratio\x18\x02 \x01(\x02\x12\x11\n\tacc_ratio\x18\x03 \x01(\x02\x12.\n\x06method\x18\n \x01(\x0e\x32\x1e.Nrmk.IndyFramework.TeleMethod\"\xcd\x02\n\tMoveFLReq\x12+\n\x06target\x18\x01 \x01(\x0b\x32\x1b.Nrmk.IndyFramework.TargetP\x12\x32\n\x08\x62lending\x18\x02 \x01(\x0b\x32 .Nrmk.IndyFramework.BlendingType\x12\x11\n\tvel_ratio\x18\x03 \x01(\x02\x12\x11\n\tacc_ratio\x18\x04 \x01(\x02\x12\x36\n\x08vel_type\x18\x05 \x01(\x0e\x32$.Nrmk.IndyFramework.VelocityModeType\x12\x11\n\tdes_force\x18\x06 \x01(\x02\x12\x1a\n\x12\x65nableForceControl\x18\x07 \x01(\x08\x12;\n\x0epost_condition\x18\x14 \x01(\x0b\x32#.Nrmk.IndyFramework.MotionCondition\x12\x15\n\rteaching_mode\x18\x1e \x01(\x08\"\x18\n\tMoveFLRes\x12\x0b\n\x03msg\x18\x64 \x01(\t*7\n\rJointBaseType\x12\x12\n\x0e\x41\x42SOLUTE_JOINT\x10\x00\x12\x12\n\x0eRELATIVE_JOINT\x10\x01*B\n\x0cTaskBaseType\x12\x11\n\rABSOLUTE_TASK\x10\x00\x12\x11\n\rRELATIVE_TASK\x10\x01\x12\x0c\n\x08TCP_TASK\x10\x02*J\n\x10VelocityModeType\x12\x11\n\rTIME_ORIENTED\x10\x00\x12\x11\n\rDISP_ORIENTED\x10\x01\x12\x10\n\x0cROT_ORIENTED\x10\x02*5\n\x13\x43ircularSettingType\x12\r\n\tPOINT_SET\x10\x00\x12\x0f\n\x0b\x43\x45NTER_AXIS\x10\x01*:\n\x12\x43ircularMovingType\x12\x0c\n\x08\x43ONSTANT\x10\x00\x12\n\n\x06RADIAL\x10\x01\x12\n\n\x06SMOOTH\x10\x02*j\n\x08TeleMode\x12\x11\n\rTELE_INACTIVE\x10\x00\x12\x0e\n\nTELE_CALIB\x10\x01\x12\x0f\n\x0bTELE_RECORD\x10\x02\x12\r\n\tTELE_PLAY\x10\x03\x12\x0c\n\x08TELE_RAW\x10\n\x12\r\n\tTELE_MOVE\x10\x14*\x9b\x01\n\nTeleMethod\x12\x16\n\x12TELE_TASK_ABSOLUTE\x10\x00\x12\x16\n\x12TELE_TASK_RELATIVE\x10\x01\x12\x11\n\rTELE_TASK_TCP\x10\x02\x12\x17\n\x13TELE_JOINT_ABSOLUTE\x10\n\x12\x17\n\x13TELE_JOINT_RELATIVE\x10\x0b\x12\x18\n\x14TELE_RECORD_ABSOLUTE\x10\x14\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'control_msgs_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_JOINTBASETYPE']._serialized_start=8868
  _globals['_JOINTBASETYPE']._serialized_end=8923
  _globals['_TASKBASETYPE']._serialized_start=8925
  _globals['_TASKBASETYPE']._serialized_end=8991
  _globals['_VELOCITYMODETYPE']._serialized_start=8993
  _globals['_VELOCITYMODETYPE']._serialized_end=9067
  _globals['_CIRCULARSETTINGTYPE']._serialized_start=9069
  _globals['_CIRCULARSETTINGTYPE']._serialized_end=9122
  _globals['_CIRCULARMOVINGTYPE']._serialized_start=9124
  _globals['_CIRCULARMOVINGTYPE']._serialized_end=9182
  _globals['_TELEMODE']._serialized_start=9184
  _globals['_TELEMODE']._serialized_end=9290
  _globals['_TELEMETHOD']._serialized_start=9293
  _globals['_TELEMETHOD']._serialized_end=9448
  _globals['_CONTROLINFO']._serialized_start=80
  _globals['_CONTROLINFO']._serialized_end=187
  _globals['_SDKLICENSEINFO']._serialized_start=189
  _globals['_SDKLICENSEINFO']._serialized_end=247
  _globals['_SDKLICENSERESP']._serialized_start=249
  _globals['_SDKLICENSERESP']._serialized_end=332
  _globals['_VARIABLECONDITION']._serialized_start=335
  _globals['_VARIABLECONDITION']._serialized_end=656
  _globals['_IOCONDITION']._serialized_start=658
  _globals['_IOCONDITION']._serialized_end=769
  _globals['_MOTIONCONDITION']._serialized_start=772
  _globals['_MOTIONCONDITION']._serialized_end=1178
  _globals['_MOTIONCONDITION_CONDITIONTYPE']._serialized_start=1058
  _globals['_MOTIONCONDITION_CONDITIONTYPE']._serialized_end=1116
  _globals['_MOTIONCONDITION_REACTIONTYPE']._serialized_start=1118
  _globals['_MOTIONCONDITION_REACTIONTYPE']._serialized_end=1178
  _globals['_BLENDINGTYPE']._serialized_start=1181
  _globals['_BLENDINGTYPE']._serialized_end=1320
  _globals['_BLENDINGTYPE_TYPE']._serialized_start=1275
  _globals['_BLENDINGTYPE_TYPE']._serialized_end=1320
  _globals['_TARGETJ']._serialized_start=1322
  _globals['_TARGETJ']._serialized_end=1420
  _globals['_MOVEJREQ']._serialized_start=1423
  _globals['_MOVEJREQ']._serialized_end=1652
  _globals['_MOVEJCONDREQ']._serialized_start=1655
  _globals['_MOVEJCONDREQ']._serialized_end=1888
  _globals['_MOVEJTREQ']._serialized_start=1891
  _globals['_MOVEJTREQ']._serialized_end=2074
  _globals['_TARGETP']._serialized_start=2076
  _globals['_TARGETP']._serialized_end=2173
  _globals['_TARGETC']._serialized_start=2175
  _globals['_TARGETC']._serialized_end=2286
  _globals['_MOVELREQ']._serialized_start=2289
  _globals['_MOVELREQ']._serialized_end=2574
  _globals['_MOVELTREQ']._serialized_start=2577
  _globals['_MOVELTREQ']._serialized_end=2760
  _globals['_MOVECREQ']._serialized_start=2763
  _globals['_MOVECREQ']._serialized_end=3185
  _globals['_MOVECTREQ']._serialized_start=3188
  _globals['_MOVECTREQ']._serialized_end=3508
  _globals['_WAITIOREQ']._serialized_start=3511
  _globals['_WAITIOREQ']._serialized_end=3989
  _globals['_WAITTIMEREQ']._serialized_start=3992
  _globals['_WAITTIMEREQ']._serialized_end=4249
  _globals['_WAITPROGRESSREQ']._serialized_start=4252
  _globals['_WAITPROGRESSREQ']._serialized_end=4517
  _globals['_WAITTRAJREQ']._serialized_start=4520
  _globals['_WAITTRAJREQ']._serialized_end=4822
  _globals['_WAITRADIUSREQ']._serialized_start=4825
  _globals['_WAITRADIUSREQ']._serialized_end=5086
  _globals['_PROGRAM']._serialized_start=5088
  _globals['_PROGRAM']._serialized_end=5134
  _globals['_TUNINGPROGRAM']._serialized_start=5137
  _globals['_TUNINGPROGRAM']._serialized_end=5332
  _globals['_PROGRAMINFO']._serialized_start=5334
  _globals['_PROGRAMINFO']._serialized_end=5394
  _globals['_VARIABLE']._serialized_start=5396
  _globals['_VARIABLE']._serialized_end=5469
  _globals['_INTVARIABLE']._serialized_start=5471
  _globals['_INTVARIABLE']._serialized_end=5513
  _globals['_MODBUSVARIABLE']._serialized_start=5516
  _globals['_MODBUSVARIABLE']._serialized_end=5723
  _globals['_MODBUSVARIABLE_SIGNALTYPE']._serialized_start=5645
  _globals['_MODBUSVARIABLE_SIGNALTYPE']._serialized_end=5723
  _globals['_BOOLVARIABLE']._serialized_start=5725
  _globals['_BOOLVARIABLE']._serialized_end=5768
  _globals['_FLOATVARIABLE']._serialized_start=5770
  _globals['_FLOATVARIABLE']._serialized_end=5814
  _globals['_JPOSVARIABLE']._serialized_start=5816
  _globals['_JPOSVARIABLE']._serialized_end=5858
  _globals['_TPOSVARIABLE']._serialized_start=5860
  _globals['_TPOSVARIABLE']._serialized_end=5902
  _globals['_MODBUSSERVER']._serialized_start=5904
  _globals['_MODBUSSERVER']._serialized_end=6024
  _globals['_MODBUSVARIABLELIST']._serialized_start=6026
  _globals['_MODBUSVARIABLELIST']._serialized_end=6106
  _globals['_ALLVARS']._serialized_start=6108
  _globals['_ALLVARS']._serialized_end=6166
  _globals['_INTVARS']._serialized_start=6168
  _globals['_INTVARS']._serialized_end=6229
  _globals['_MODBUSVARS']._serialized_start=6231
  _globals['_MODBUSVARS']._serialized_end=6298
  _globals['_BOOLVARS']._serialized_start=6300
  _globals['_BOOLVARS']._serialized_end=6363
  _globals['_FLOATVARS']._serialized_start=6365
  _globals['_FLOATVARS']._serialized_end=6430
  _globals['_JPOSVARS']._serialized_start=6432
  _globals['_JPOSVARS']._serialized_end=6495
  _globals['_TPOSVARS']._serialized_start=6497
  _globals['_TPOSVARS']._serialized_end=6560
  _globals['_INVERSEKINEMATICSREQ']._serialized_start=6562
  _globals['_INVERSEKINEMATICSREQ']._serialized_end=6617
  _globals['_INVERSEKINEMATICSRES']._serialized_start=6619
  _globals['_INVERSEKINEMATICSRES']._serialized_end=6703
  _globals['_CHECKAPROACHRETRACTVALIDREQ']._serialized_start=6705
  _globals['_CHECKAPROACHRETRACTVALIDREQ']._serialized_end=6804
  _globals['_CHECKAPROACHRETRACTVALIDRES']._serialized_start=6807
  _globals['_CHECKAPROACHRETRACTVALIDRES']._serialized_end=6962
  _globals['_GETPALLETPOINTLISTREQ']._serialized_start=6965
  _globals['_GETPALLETPOINTLISTREQ']._serialized_end=7108
  _globals['_PALLETPOINT']._serialized_start=7110
  _globals['_PALLETPOINT']._serialized_end=7201
  _globals['_GETPALLETPOINTLISTRES']._serialized_start=7203
  _globals['_GETPALLETPOINTLISTRES']._serialized_end=7330
  _globals['_CALCULATERELATIVEPOSEREQ']._serialized_start=7332
  _globals['_CALCULATERELATIVEPOSEREQ']._serialized_end=7447
  _globals['_CALCULATERELATIVEPOSERES']._serialized_start=7449
  _globals['_CALCULATERELATIVEPOSERES']._serialized_end=7545
  _globals['_CALCULATECURRENTPOSERELREQ']._serialized_start=7547
  _globals['_CALCULATECURRENTPOSERELREQ']._serialized_end=7671
  _globals['_CALCULATECURRENTPOSERELRES']._serialized_start=7673
  _globals['_CALCULATECURRENTPOSERELRES']._serialized_end=7773
  _globals['_TELEOPDEVICE']._serialized_start=7776
  _globals['_TELEOPDEVICE']._serialized_end=7954
  _globals['_TELEOPDEVICE_TELEOPDEVICETYPE']._serialized_start=7916
  _globals['_TELEOPDEVICE_TELEOPDEVICETYPE']._serialized_end=7954
  _globals['_TELEOPSTATE']._serialized_start=7956
  _globals['_TELEOPSTATE']._serialized_end=8061
  _globals['_TELEP']._serialized_start=8063
  _globals['_TELEP']._serialized_end=8132
  _globals['_TELEOPFILELIST']._serialized_start=8134
  _globals['_TELEOPFILELIST']._serialized_end=8213
  _globals['_TELEFILEREQ']._serialized_start=8215
  _globals['_TELEFILEREQ']._serialized_end=8242
  _globals['_TELEPLAYRATE']._serialized_start=8244
  _globals['_TELEPLAYRATE']._serialized_end=8272
  _globals['_MOVETELEJREQ']._serialized_start=8274
  _globals['_MOVETELEJREQ']._serialized_end=8388
  _globals['_MOVETELELREQ']._serialized_start=8390
  _globals['_MOVETELELREQ']._serialized_end=8504
  _globals['_MOVEFLREQ']._serialized_start=8507
  _globals['_MOVEFLREQ']._serialized_end=8840
  _globals['_MOVEFLRES']._serialized_start=8842
  _globals['_MOVEFLRES']._serialized_end=8866
# @@protoc_insertion_point(module_scope)
