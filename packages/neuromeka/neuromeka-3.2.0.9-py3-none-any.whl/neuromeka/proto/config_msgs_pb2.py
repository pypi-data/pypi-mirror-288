# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: config_msgs.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_msgs_pb2 as common__msgs__pb2
import device_msgs_pb2 as device__msgs__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63onfig_msgs.proto\x12\x12Nrmk.IndyFramework\x1a\x11\x63ommon_msgs.proto\x1a\x11\x64\x65vice_msgs.proto\"\x15\n\x05\x46rame\x12\x0c\n\x04\x66pos\x18\x01 \x03(\x02\"6\n\rFTsensorFrame\x12\x13\n\x0btranslation\x18\x01 \x01(\x02\x12\x10\n\x08rotation\x18\x02 \x01(\x02\"\x18\n\x08JointPos\x12\x0c\n\x04jpos\x18\x01 \x03(\x02\":\n\x0bPlanarFrame\x12\r\n\x05\x66pos0\x18\x01 \x03(\x02\x12\r\n\x05\x66pos1\x18\x02 \x03(\x02\x12\r\n\x05\x66pos2\x18\x03 \x03(\x02\"K\n\x0b\x46rameResult\x12\x0c\n\x04\x66pos\x18\x01 \x03(\x02\x12.\n\x08response\x18\x02 \x01(\x0b\x32\x1c.Nrmk.IndyFramework.Response\"\x16\n\x05Ratio\x12\r\n\x05ratio\x18\x01 \x01(\r\"2\n\x12\x41utoServoOffConfig\x12\x0e\n\x06\x65nable\x18\x01 \x01(\x08\x12\x0c\n\x04time\x18\x02 \x01(\x02\"\xc4\x02\n\x10\x43ollTuningConfig\x12G\n\tprecision\x18\x01 \x01(\x0e\x32\x34.Nrmk.IndyFramework.CollTuningConfig.TuningPrecision\x12\x46\n\x0ctuning_space\x18\x02 \x01(\x0e\x32\x30.Nrmk.IndyFramework.CollTuningConfig.TuningSpace\x12\x15\n\rvel_level_max\x18\x03 \x01(\x05\"?\n\x0fTuningPrecision\x12\x0c\n\x08LOW_TUNE\x10\x00\x12\x0f\n\x0bMIDDLE_TUNE\x10\x01\x12\r\n\tHIGH_TUNE\x10\x02\"G\n\x0bTuningSpace\x12\x0b\n\x07NO_TUNE\x10\x00\x12\x0e\n\nJOINT_TUNE\x10\x01\x12\r\n\tTASK_TUNE\x10\x02\x12\x0c\n\x08\x41LL_TUNE\x10\x03\"3\n\x0cJointGainSet\x12\n\n\x02kp\x18\x01 \x03(\x02\x12\n\n\x02kv\x18\x02 \x03(\x02\x12\x0b\n\x03kl2\x18\x03 \x03(\x02\"2\n\x0bTaskGainSet\x12\n\n\x02kp\x18\x01 \x03(\x02\x12\n\n\x02kv\x18\x02 \x03(\x02\x12\x0b\n\x03kl2\x18\x03 \x03(\x02\"Q\n\x10ImpedanceGainSet\x12\x0c\n\x04mass\x18\x01 \x03(\x02\x12\x0f\n\x07\x64\x61mping\x18\x02 \x03(\x02\x12\x11\n\tstiffness\x18\x03 \x03(\x02\x12\x0b\n\x03kl2\x18\x04 \x03(\x02\"\x7f\n\x0c\x46orceGainSet\x12\n\n\x02kp\x18\x01 \x03(\x02\x12\n\n\x02kv\x18\x02 \x03(\x02\x12\x0b\n\x03kl2\x18\x03 \x03(\x02\x12\x0c\n\x04mass\x18\x04 \x03(\x02\x12\x0f\n\x07\x64\x61mping\x18\x05 \x03(\x02\x12\x11\n\tstiffness\x18\x06 \x03(\x02\x12\x0b\n\x03kpf\x18\x07 \x03(\x02\x12\x0b\n\x03kif\x18\x08 \x03(\x02\"i\n\x0bTestGainSet\x12\r\n\x05kpctc\x18\x01 \x03(\x02\x12\r\n\x05kvctc\x18\x02 \x03(\x02\x12\r\n\x05kictc\x18\x03 \x03(\x02\x12\r\n\x05knric\x18\x04 \x03(\x02\x12\x0e\n\x06kpnric\x18\x05 \x03(\x02\x12\x0e\n\x06kinric\x18\x06 \x03(\x02\"\xa5\x01\n\rCustomGainSet\x12\r\n\x05gain0\x18\x01 \x03(\x02\x12\r\n\x05gain1\x18\x02 \x03(\x02\x12\r\n\x05gain2\x18\x03 \x03(\x02\x12\r\n\x05gain3\x18\x04 \x03(\x02\x12\r\n\x05gain4\x18\x05 \x03(\x02\x12\r\n\x05gain5\x18\x06 \x03(\x02\x12\r\n\x05gain6\x18\x07 \x03(\x02\x12\r\n\x05gain7\x18\x08 \x03(\x02\x12\r\n\x05gain8\x18\t \x03(\x02\x12\r\n\x05gain9\x18\n \x03(\x02\":\n\x16NewControllerTestState\x12\x0f\n\x07Jenable\x18\x01 \x01(\x08\x12\x0f\n\x07Tenable\x18\x02 \x01(\x08\"\x87\x01\n\x0f\x46rictionCompSet\x12\x1b\n\x13\x63ontrol_comp_enable\x18\x01 \x01(\x08\x12\x1b\n\x13\x63ontrol_comp_levels\x18\x02 \x03(\x05\x12\x1c\n\x14teaching_comp_enable\x18\x03 \x01(\x08\x12\x1c\n\x14teaching_comp_levels\x18\x04 \x03(\x05\"(\n\x0eMountingAngles\x12\n\n\x02ry\x18\x01 \x01(\x02\x12\n\n\x02rz\x18\x02 \x01(\x02\"G\n\x0eToolProperties\x12\x0c\n\x04mass\x18\x01 \x01(\x02\x12\x16\n\x0e\x63\x65nter_of_mass\x18\x02 \x03(\x02\x12\x0f\n\x07inertia\x18\x03 \x03(\x02\"#\n\x12\x43ollisionSensLevel\x12\r\n\x05level\x18\x01 \x01(\r\"\xb2\x02\n\x13\x43ollisionThresholds\x12\x16\n\x0ej_torque_bases\x18\x01 \x03(\x02\x12\x19\n\x11j_torque_tangents\x18\x02 \x03(\x02\x12\x16\n\x0et_torque_bases\x18\x03 \x03(\x02\x12\x19\n\x11t_torque_tangents\x18\x04 \x03(\x02\x12\x13\n\x0b\x65rror_bases\x18\x05 \x03(\x02\x12\x16\n\x0e\x65rror_tangents\x18\x06 \x03(\x02\x12\x1f\n\x17t_constvel_torque_bases\x18\x07 \x03(\x02\x12\"\n\x1at_constvel_torque_tangents\x18\x08 \x03(\x02\x12\x1f\n\x17t_conveyor_torque_bases\x18\t \x03(\x02\x12\"\n\x1at_conveyor_torque_tangents\x18\n \x03(\x02\"t\n\x0f\x43ollisionPolicy\x12\x37\n\x06policy\x18\x01 \x01(\x0e\x32\'.Nrmk.IndyFramework.CollisionPolicyType\x12\x12\n\nsleep_time\x18\x02 \x01(\x02\x12\x14\n\x0cgravity_time\x18\x03 \x01(\x02\"\xc4\x01\n\x0cSafetyLimits\x12\x13\n\x0bpower_limit\x18\x01 \x01(\x02\x12\x19\n\x11power_limit_ratio\x18\x02 \x01(\x02\x12\x17\n\x0ftcp_force_limit\x18\x03 \x01(\x02\x12\x1d\n\x15tcp_force_limit_ratio\x18\x04 \x01(\x02\x12\x17\n\x0ftcp_speed_limit\x18\x05 \x01(\x02\x12\x1d\n\x15tcp_speed_limit_ratio\x18\x06 \x01(\x02\x12\x14\n\x0cjoint_limits\x18\x07 \x03(\x02\"\xb0\x03\n\x10SafetyStopConfig\x12G\n\x1djoint_position_limit_stop_cat\x18\x01 \x01(\x0e\x32 .Nrmk.IndyFramework.StopCategory\x12\x44\n\x1ajoint_speed_limit_stop_cat\x18\x02 \x01(\x0e\x32 .Nrmk.IndyFramework.StopCategory\x12\x45\n\x1bjoint_torque_limit_stop_cat\x18\x03 \x01(\x0e\x32 .Nrmk.IndyFramework.StopCategory\x12\x42\n\x18tcp_speed_limit_stop_cat\x18\x04 \x01(\x0e\x32 .Nrmk.IndyFramework.StopCategory\x12\x42\n\x18tcp_force_limit_stop_cat\x18\x05 \x01(\x0e\x32 .Nrmk.IndyFramework.StopCategory\x12>\n\x14power_limit_stop_cat\x18\x06 \x01(\x0e\x32 .Nrmk.IndyFramework.StopCategory\"\xe9\x01\n\x08\x44IConfig\x12\x15\n\rfunction_code\x18\x01 \x01(\x05\x12\x15\n\rfunction_name\x18\x02 \x01(\t\x12\x39\n\x0etriggerSignals\x18\x03 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x39\n\x0esuccessSignals\x18\x04 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x39\n\x0e\x66\x61ilureSignals\x18\x05 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\"@\n\x0c\x44IConfigList\x12\x30\n\ndi_configs\x18\x01 \x03(\x0b\x32\x1c.Nrmk.IndyFramework.DIConfig\"\x9f\x01\n\x08\x44OConfig\x12\x12\n\nstate_code\x18\x01 \x01(\x05\x12\x12\n\nstate_name\x18\x02 \x01(\t\x12\x34\n\tonSignals\x18\x03 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\x12\x35\n\noffSignals\x18\x04 \x03(\x0b\x32!.Nrmk.IndyFramework.DigitalSignal\"@\n\x0c\x44OConfigList\x12\x30\n\ndo_configs\x18\x01 \x03(\x0b\x32\x1c.Nrmk.IndyFramework.DOConfigb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'config_msgs_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FRAME']._serialized_start=79
  _globals['_FRAME']._serialized_end=100
  _globals['_FTSENSORFRAME']._serialized_start=102
  _globals['_FTSENSORFRAME']._serialized_end=156
  _globals['_JOINTPOS']._serialized_start=158
  _globals['_JOINTPOS']._serialized_end=182
  _globals['_PLANARFRAME']._serialized_start=184
  _globals['_PLANARFRAME']._serialized_end=242
  _globals['_FRAMERESULT']._serialized_start=244
  _globals['_FRAMERESULT']._serialized_end=319
  _globals['_RATIO']._serialized_start=321
  _globals['_RATIO']._serialized_end=343
  _globals['_AUTOSERVOOFFCONFIG']._serialized_start=345
  _globals['_AUTOSERVOOFFCONFIG']._serialized_end=395
  _globals['_COLLTUNINGCONFIG']._serialized_start=398
  _globals['_COLLTUNINGCONFIG']._serialized_end=722
  _globals['_COLLTUNINGCONFIG_TUNINGPRECISION']._serialized_start=586
  _globals['_COLLTUNINGCONFIG_TUNINGPRECISION']._serialized_end=649
  _globals['_COLLTUNINGCONFIG_TUNINGSPACE']._serialized_start=651
  _globals['_COLLTUNINGCONFIG_TUNINGSPACE']._serialized_end=722
  _globals['_JOINTGAINSET']._serialized_start=724
  _globals['_JOINTGAINSET']._serialized_end=775
  _globals['_TASKGAINSET']._serialized_start=777
  _globals['_TASKGAINSET']._serialized_end=827
  _globals['_IMPEDANCEGAINSET']._serialized_start=829
  _globals['_IMPEDANCEGAINSET']._serialized_end=910
  _globals['_FORCEGAINSET']._serialized_start=912
  _globals['_FORCEGAINSET']._serialized_end=1039
  _globals['_TESTGAINSET']._serialized_start=1041
  _globals['_TESTGAINSET']._serialized_end=1146
  _globals['_CUSTOMGAINSET']._serialized_start=1149
  _globals['_CUSTOMGAINSET']._serialized_end=1314
  _globals['_NEWCONTROLLERTESTSTATE']._serialized_start=1316
  _globals['_NEWCONTROLLERTESTSTATE']._serialized_end=1374
  _globals['_FRICTIONCOMPSET']._serialized_start=1377
  _globals['_FRICTIONCOMPSET']._serialized_end=1512
  _globals['_MOUNTINGANGLES']._serialized_start=1514
  _globals['_MOUNTINGANGLES']._serialized_end=1554
  _globals['_TOOLPROPERTIES']._serialized_start=1556
  _globals['_TOOLPROPERTIES']._serialized_end=1627
  _globals['_COLLISIONSENSLEVEL']._serialized_start=1629
  _globals['_COLLISIONSENSLEVEL']._serialized_end=1664
  _globals['_COLLISIONTHRESHOLDS']._serialized_start=1667
  _globals['_COLLISIONTHRESHOLDS']._serialized_end=1973
  _globals['_COLLISIONPOLICY']._serialized_start=1975
  _globals['_COLLISIONPOLICY']._serialized_end=2091
  _globals['_SAFETYLIMITS']._serialized_start=2094
  _globals['_SAFETYLIMITS']._serialized_end=2290
  _globals['_SAFETYSTOPCONFIG']._serialized_start=2293
  _globals['_SAFETYSTOPCONFIG']._serialized_end=2725
  _globals['_DICONFIG']._serialized_start=2728
  _globals['_DICONFIG']._serialized_end=2961
  _globals['_DICONFIGLIST']._serialized_start=2963
  _globals['_DICONFIGLIST']._serialized_end=3027
  _globals['_DOCONFIG']._serialized_start=3030
  _globals['_DOCONFIG']._serialized_end=3189
  _globals['_DOCONFIGLIST']._serialized_start=3191
  _globals['_DOCONFIGLIST']._serialized_end=3255
# @@protoc_insertion_point(module_scope)
