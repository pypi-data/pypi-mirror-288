# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/group/v1/group/group.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.role.v1.role import role_id_pb2 as com_dot_terraquantum_dot_role_dot_v1_dot_role_dot_role__id__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+com/terraquantum/group/v1/group/group.proto\x12\x1f\x63om.terraquantum.group.v1.group\x1a+com/terraquantum/role/v1/role/role_id.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xbd\x02\n\nGroupProto\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\'\n\x0forganization_id\x18\x02 \x01(\tR\x0eorganizationId\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x04 \x01(\tR\x0b\x64\x65scription\x12\x39\n\ncreated_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x1d\n\nmember_ids\x18\x06 \x03(\tR\tmemberIds\x12\x45\n\x08role_ids\x18\x07 \x03(\x0b\x32*.com.terraquantum.role.v1.role.RoleIdProtoR\x07roleIds\x12\x1f\n\x0bproject_ids\x18\x08 \x03(\tR\nprojectIdsB\x98\x02\n#com.com.terraquantum.group.v1.groupB\nGroupProtoP\x01ZCterraquantum.swiss/tq42_grpc_client/com/terraquantum/group/v1/group\xa2\x02\x05\x43TGVG\xaa\x02\x1f\x43om.Terraquantum.Group.V1.Group\xca\x02\x1f\x43om\\Terraquantum\\Group\\V1\\Group\xe2\x02+Com\\Terraquantum\\Group\\V1\\Group\\GPBMetadata\xea\x02#Com::Terraquantum::Group::V1::Groupb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.group.v1.group.group_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n#com.com.terraquantum.group.v1.groupB\nGroupProtoP\001ZCterraquantum.swiss/tq42_grpc_client/com/terraquantum/group/v1/group\242\002\005CTGVG\252\002\037Com.Terraquantum.Group.V1.Group\312\002\037Com\\Terraquantum\\Group\\V1\\Group\342\002+Com\\Terraquantum\\Group\\V1\\Group\\GPBMetadata\352\002#Com::Terraquantum::Group::V1::Group'
  _globals['_GROUPPROTO']._serialized_start=159
  _globals['_GROUPPROTO']._serialized_end=476
# @@protoc_insertion_point(module_scope)
