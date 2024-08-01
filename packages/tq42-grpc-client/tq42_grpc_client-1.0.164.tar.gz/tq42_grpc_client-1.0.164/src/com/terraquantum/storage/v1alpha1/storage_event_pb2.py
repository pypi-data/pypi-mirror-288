# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/storage/v1alpha1/storage_event.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.storage.v1alpha1 import storage_pb2 as com_dot_terraquantum_dot_storage_dot_v1alpha1_dot_storage__pb2
from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5com/terraquantum/storage/v1alpha1/storage_event.proto\x12!com.terraquantum.storage.v1alpha1\x1a/com/terraquantum/storage/v1alpha1/storage.proto\x1a\x1b\x62uf/validate/validate.proto\"\x81\x01\n\x1dStorageTransferRequestedProto\x12\x18\n\x02id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\x02id\x12\x1d\n\x03url\x18\x02 \x01(\tB\x0b\xbaH\x08r\x03\x18\x80\x01\xc8\x01\x01R\x03url\x12\'\n\nproject_id\x18\x03 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tprojectId\"X\n\x13StorageCreatedProto\x12\x18\n\x02id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\x02id\x12\'\n\nproject_id\x18\x02 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tprojectId\"\x8e\x01\n\x19StorageStatusChangedProto\x12\x18\n\x02id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\x02id\x12W\n\x06status\x18\x02 \x01(\x0e\x32\x35.com.terraquantum.storage.v1alpha1.StorageStatusProtoB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x06status\"b\n\x1dStorageDeletionRequestedProto\x12\x18\n\x02id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\x02id\x12\'\n\nproject_id\x18\x02 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tprojectId\"8\n\x15\x41\x63tiveStorageIdsProto\x12\x1f\n\x03ids\x18\x01 \x03(\tB\r\xbaH\n\x92\x01\x07\"\x05r\x03\xb0\x01\x01R\x03ids\"\x85\x02\n\x15UploadUrlCreatedProto\x12\'\n\nstorage_id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tstorageId\x12%\n\nsigned_url\x18\x02 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\tsignedUrl\x12!\n\x08hash_md5\x18\x03 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x07hashMd5\x12\'\n\nproject_id\x18\x04 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tprojectId\x12\'\n\ncreated_by\x18\x05 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tcreatedBy\x12\'\n\nrequest_id\x18\x06 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\trequestId\"\xe4\x01\n\x17UploadUrlRequestedProto\x12%\n\x08hash_md5\x18\x01 \x01(\tB\n\xbaH\x07r\x05\x10\x02\x18\x80\x01R\x07hashMd5\x12\'\n\tfile_name\x18\x02 \x01(\tB\n\xbaH\x07r\x05\x10\x02\x18\x80\x01R\x08\x66ileName\x12\'\n\nproject_id\x18\x03 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tprojectId\x12\'\n\ncreated_by\x18\x04 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tcreatedBy\x12\'\n\nrequest_id\x18\x05 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\trequestIdB\xb8\x02\n%com.com.terraquantum.storage.v1alpha1B\x11StorageEventProtoP\x01ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/storage/v1alpha1;storagev1alpha1\xa2\x02\x03\x43TS\xaa\x02!Com.Terraquantum.Storage.V1alpha1\xca\x02!Com\\Terraquantum\\Storage\\V1alpha1\xe2\x02-Com\\Terraquantum\\Storage\\V1alpha1\\GPBMetadata\xea\x02$Com::Terraquantum::Storage::V1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.storage.v1alpha1.storage_event_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.com.terraquantum.storage.v1alpha1B\021StorageEventProtoP\001ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/storage/v1alpha1;storagev1alpha1\242\002\003CTS\252\002!Com.Terraquantum.Storage.V1alpha1\312\002!Com\\Terraquantum\\Storage\\V1alpha1\342\002-Com\\Terraquantum\\Storage\\V1alpha1\\GPBMetadata\352\002$Com::Terraquantum::Storage::V1alpha1'
  _globals['_STORAGETRANSFERREQUESTEDPROTO'].fields_by_name['id']._options = None
  _globals['_STORAGETRANSFERREQUESTEDPROTO'].fields_by_name['id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGETRANSFERREQUESTEDPROTO'].fields_by_name['url']._options = None
  _globals['_STORAGETRANSFERREQUESTEDPROTO'].fields_by_name['url']._serialized_options = b'\272H\010r\003\030\200\001\310\001\001'
  _globals['_STORAGETRANSFERREQUESTEDPROTO'].fields_by_name['project_id']._options = None
  _globals['_STORAGETRANSFERREQUESTEDPROTO'].fields_by_name['project_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGECREATEDPROTO'].fields_by_name['id']._options = None
  _globals['_STORAGECREATEDPROTO'].fields_by_name['id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGECREATEDPROTO'].fields_by_name['project_id']._options = None
  _globals['_STORAGECREATEDPROTO'].fields_by_name['project_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGESTATUSCHANGEDPROTO'].fields_by_name['id']._options = None
  _globals['_STORAGESTATUSCHANGEDPROTO'].fields_by_name['id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGESTATUSCHANGEDPROTO'].fields_by_name['status']._options = None
  _globals['_STORAGESTATUSCHANGEDPROTO'].fields_by_name['status']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_STORAGEDELETIONREQUESTEDPROTO'].fields_by_name['id']._options = None
  _globals['_STORAGEDELETIONREQUESTEDPROTO'].fields_by_name['id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGEDELETIONREQUESTEDPROTO'].fields_by_name['project_id']._options = None
  _globals['_STORAGEDELETIONREQUESTEDPROTO'].fields_by_name['project_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_ACTIVESTORAGEIDSPROTO'].fields_by_name['ids']._options = None
  _globals['_ACTIVESTORAGEIDSPROTO'].fields_by_name['ids']._serialized_options = b'\272H\n\222\001\007\"\005r\003\260\001\001'
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['storage_id']._options = None
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['storage_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['signed_url']._options = None
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['signed_url']._serialized_options = b'\272H\003\310\001\001'
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['hash_md5']._options = None
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['hash_md5']._serialized_options = b'\272H\003\310\001\001'
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['project_id']._options = None
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['project_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['created_by']._options = None
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['created_by']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['request_id']._options = None
  _globals['_UPLOADURLCREATEDPROTO'].fields_by_name['request_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['hash_md5']._options = None
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['hash_md5']._serialized_options = b'\272H\007r\005\020\002\030\200\001'
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['file_name']._options = None
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['file_name']._serialized_options = b'\272H\007r\005\020\002\030\200\001'
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['project_id']._options = None
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['project_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['created_by']._options = None
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['created_by']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['request_id']._options = None
  _globals['_UPLOADURLREQUESTEDPROTO'].fields_by_name['request_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGETRANSFERREQUESTEDPROTO']._serialized_start=171
  _globals['_STORAGETRANSFERREQUESTEDPROTO']._serialized_end=300
  _globals['_STORAGECREATEDPROTO']._serialized_start=302
  _globals['_STORAGECREATEDPROTO']._serialized_end=390
  _globals['_STORAGESTATUSCHANGEDPROTO']._serialized_start=393
  _globals['_STORAGESTATUSCHANGEDPROTO']._serialized_end=535
  _globals['_STORAGEDELETIONREQUESTEDPROTO']._serialized_start=537
  _globals['_STORAGEDELETIONREQUESTEDPROTO']._serialized_end=635
  _globals['_ACTIVESTORAGEIDSPROTO']._serialized_start=637
  _globals['_ACTIVESTORAGEIDSPROTO']._serialized_end=693
  _globals['_UPLOADURLCREATEDPROTO']._serialized_start=696
  _globals['_UPLOADURLCREATEDPROTO']._serialized_end=957
  _globals['_UPLOADURLREQUESTEDPROTO']._serialized_start=960
  _globals['_UPLOADURLREQUESTEDPROTO']._serialized_end=1188
# @@protoc_insertion_point(module_scope)
