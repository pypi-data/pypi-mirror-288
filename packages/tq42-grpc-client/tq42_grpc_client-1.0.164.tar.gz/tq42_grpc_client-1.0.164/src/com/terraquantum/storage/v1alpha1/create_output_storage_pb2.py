# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/storage/v1alpha1/create_output_storage.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.storage.v1alpha1 import storage_pb2 as com_dot_terraquantum_dot_storage_dot_v1alpha1_dot_storage__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=com/terraquantum/storage/v1alpha1/create_output_storage.proto\x12!com.terraquantum.storage.v1alpha1\x1a/com/terraquantum/storage/v1alpha1/storage.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1b\x62uf/validate/validate.proto\"\xd6\x02\n\x1a\x43reateOutputStorageRequest\x12\'\n\nstorage_id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tstorageId\x12\x34\n\x11\x65xperiment_run_id\x18\x02 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\x0f\x65xperimentRunId\x12\'\n\nproject_id\x18\x03 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tprojectId\x12L\n\x04type\x18\x04 \x01(\x0e\x32..com.terraquantum.storage.v1alpha1.StorageTypeB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x04type\x12\'\n\ncreated_by\x18\x05 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tcreatedBy\x12\x39\n\ncreated_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAtB\xbf\x02\n%com.com.terraquantum.storage.v1alpha1B\x18\x43reateOutputStorageProtoP\x01ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/storage/v1alpha1;storagev1alpha1\xa2\x02\x03\x43TS\xaa\x02!Com.Terraquantum.Storage.V1alpha1\xca\x02!Com\\Terraquantum\\Storage\\V1alpha1\xe2\x02-Com\\Terraquantum\\Storage\\V1alpha1\\GPBMetadata\xea\x02$Com::Terraquantum::Storage::V1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.storage.v1alpha1.create_output_storage_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.com.terraquantum.storage.v1alpha1B\030CreateOutputStorageProtoP\001ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/storage/v1alpha1;storagev1alpha1\242\002\003CTS\252\002!Com.Terraquantum.Storage.V1alpha1\312\002!Com\\Terraquantum\\Storage\\V1alpha1\342\002-Com\\Terraquantum\\Storage\\V1alpha1\\GPBMetadata\352\002$Com::Terraquantum::Storage::V1alpha1'
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['storage_id']._options = None
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['storage_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['experiment_run_id']._options = None
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['experiment_run_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['project_id']._options = None
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['project_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['type']._options = None
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['type']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['created_by']._options = None
  _globals['_CREATEOUTPUTSTORAGEREQUEST'].fields_by_name['created_by']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_CREATEOUTPUTSTORAGEREQUEST']._serialized_start=212
  _globals['_CREATEOUTPUTSTORAGEREQUEST']._serialized_end=554
# @@protoc_insertion_point(module_scope)
