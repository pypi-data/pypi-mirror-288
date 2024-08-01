# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/user/v1/waiting_user/waiting_user.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.javalibs.logging.v1 import logging_extensions_pb2 as com_dot_terraquantum_dot_javalibs_dot_logging_dot_v1_dot_logging__extensions__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8com/terraquantum/user/v1/waiting_user/waiting_user.proto\x12%com.terraquantum.user.v1.waiting_user\x1a=com/terraquantum/javalibs/logging/v1/logging_extensions.proto\"\xcd\x03\n\x10WaitingUserProto\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x34\n\nfirst_name\x18\x02 \x01(\tB\x15\x88\xb5\x18\x01\x90\xb5\x18\x01\x98\xb5\x18\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01R\tfirstName\x12\x32\n\tlast_name\x18\x03 \x01(\tB\x15\x88\xb5\x18\x01\x90\xb5\x18\x01\x98\xb5\x18\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01R\x08lastName\x12\x32\n\x05\x65mail\x18\x04 \x01(\tB\x1c\x88\xb5\x18\x01\xa2\xb5\x18\x14^[^@]{3}(.*)(\\.\\w+)$R\x05\x65mail\x12\x18\n\x07\x63ompany\x18\x05 \x01(\tR\x07\x63ompany\x12H\n\x04role\x18\x06 \x01(\x0e\x32\x34.com.terraquantum.user.v1.waiting_user.UserRoleProtoR\x04role\x12s\n\x18primary_area_of_interest\x18\x07 \x01(\x0e\x32:.com.terraquantum.user.v1.waiting_user.AreaOfInterestProtoR\x15primaryAreaOfInterest\x12,\n\x12newsletter_sign_up\x18\t \x01(\x08R\x10newsletterSignUpJ\x04\x08\x08\x10\t*\xb2\x02\n\rUserRoleProto\x12\x19\n\x15USER_ROLE_UNSPECIFIED\x10\x00\x12\x0f\n\x0b\x43_LEVEL_CVP\x10\x01\x12\x0f\n\x0bVP_DIRECTOR\x10\x02\x12\x0b\n\x07MANAGER\x10\x03\x12\x1a\n\x16INDIVIDUAL_CONTRIBUTOR\x10\x04\x12\x12\n\x0eSTUDENT_INTERN\x10\x05\x12\t\n\x05OTHER\x10\x06\x12\x0e\n\nJOB_SEEKER\x10\x07\x12\x0e\n\nFREELANCER\x10\x08\x12\x13\n\x0f\x41\x43\x43OUNT_MANAGER\x10\t\x12\x10\n\x0c\x41GENCY_OWNER\x10\n\x12\r\n\tSALES_REP\x10\x0b\x12\x11\n\rSALES_MANAGER\x10\x0c\x12\x16\n\x12\x43ONTENT_STRATEGIST\x10\r\x12\x0c\n\x08\x44\x45SIGNER\x10\x0e\x12\r\n\tPROFESSOR\x10\x0f*V\n\x13\x41reaOfInterestProto\x12 \n\x1c\x41REA_OF_INTEREST_UNSPECIFIED\x10\x00\x12\r\n\tTECHNICAL\x10\x01\x12\x0e\n\nMANAGEMENT\x10\x02\x42\xbe\x02\n)com.com.terraquantum.user.v1.waiting_userB\x10WaitingUserProtoP\x01ZIterraquantum.swiss/tq42_grpc_client/com/terraquantum/user/v1/waiting_user\xa2\x02\x05\x43TUVW\xaa\x02$Com.Terraquantum.User.V1.WaitingUser\xca\x02$Com\\Terraquantum\\User\\V1\\WaitingUser\xe2\x02\x30\x43om\\Terraquantum\\User\\V1\\WaitingUser\\GPBMetadata\xea\x02(Com::Terraquantum::User::V1::WaitingUserb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.user.v1.waiting_user.waiting_user_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n)com.com.terraquantum.user.v1.waiting_userB\020WaitingUserProtoP\001ZIterraquantum.swiss/tq42_grpc_client/com/terraquantum/user/v1/waiting_user\242\002\005CTUVW\252\002$Com.Terraquantum.User.V1.WaitingUser\312\002$Com\\Terraquantum\\User\\V1\\WaitingUser\342\0020Com\\Terraquantum\\User\\V1\\WaitingUser\\GPBMetadata\352\002(Com::Terraquantum::User::V1::WaitingUser'
  _globals['_WAITINGUSERPROTO'].fields_by_name['first_name']._options = None
  _globals['_WAITINGUSERPROTO'].fields_by_name['first_name']._serialized_options = b'\210\265\030\001\220\265\030\001\230\265\030\377\377\377\377\377\377\377\377\377\001'
  _globals['_WAITINGUSERPROTO'].fields_by_name['last_name']._options = None
  _globals['_WAITINGUSERPROTO'].fields_by_name['last_name']._serialized_options = b'\210\265\030\001\220\265\030\001\230\265\030\377\377\377\377\377\377\377\377\377\001'
  _globals['_WAITINGUSERPROTO'].fields_by_name['email']._options = None
  _globals['_WAITINGUSERPROTO'].fields_by_name['email']._serialized_options = b'\210\265\030\001\242\265\030\024^[^@]{3}(.*)(\\.\\w+)$'
  _globals['_USERROLEPROTO']._serialized_start=627
  _globals['_USERROLEPROTO']._serialized_end=933
  _globals['_AREAOFINTERESTPROTO']._serialized_start=935
  _globals['_AREAOFINTERESTPROTO']._serialized_end=1021
  _globals['_WAITINGUSERPROTO']._serialized_start=163
  _globals['_WAITINGUSERPROTO']._serialized_end=624
# @@protoc_insertion_point(module_scope)
