# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/experiment/v1/experimentrun/algorithm/toy.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n@com/terraquantum/experiment/v1/experimentrun/algorithm/toy.proto\x12\x36\x63om.terraquantum.experiment.v1.experimentrun.algorithm\x1a\x1b\x62uf/validate/validate.proto\"K\n\x12ToyParametersProto\x12\x15\n\x01n\x18\x01 \x01(\x05\x42\x07\xbaH\x04\x1a\x02 \x00R\x01n\x12\x0c\n\x01r\x18\x02 \x01(\x02R\x01r\x12\x10\n\x03msg\x18\x03 \x01(\tR\x03msg\"\x10\n\x0eToyInputsProto\"\xf7\x01\n\x10ToyMetadataProto\x12r\n\nparameters\x18\x04 \x01(\x0b\x32J.com.terraquantum.experiment.v1.experimentrun.algorithm.ToyParametersProtoB\x06\xbaH\x03\xc8\x01\x01R\nparameters\x12^\n\x06inputs\x18\x05 \x01(\x0b\x32\x46.com.terraquantum.experiment.v1.experimentrun.algorithm.ToyInputsProtoR\x06inputsJ\x04\x08\x01\x10\x04R\x01nR\x01rR\x03msg\"J\n\x0eToyResultProto\x12\x0c\n\x01y\x18\x01 \x03(\x05R\x01y\x12\x10\n\x03msg\x18\x02 \x01(\tR\x03msg\x12\x18\n\x07version\x18\x03 \x01(\tR\x07version\"\x11\n\x0fToyOutputsProto\"\xdc\x01\n\x0fToyOutcomeProto\x12\x66\n\x06result\x18\x01 \x01(\x0b\x32\x46.com.terraquantum.experiment.v1.experimentrun.algorithm.ToyResultProtoB\x06\xbaH\x03\xc8\x01\x01R\x06result\x12\x61\n\x07outputs\x18\x02 \x01(\x0b\x32G.com.terraquantum.experiment.v1.experimentrun.algorithm.ToyOutputsProtoR\x07outputsB\xa2\x03\n:com.com.terraquantum.experiment.v1.experimentrun.algorithmB\x08ToyProtoP\x01ZZterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm\xa2\x02\x06\x43TEVEA\xaa\x02\x36\x43om.Terraquantum.Experiment.V1.Experimentrun.Algorithm\xca\x02\x36\x43om\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\xe2\x02\x42\x43om\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\GPBMetadata\xea\x02;Com::Terraquantum::Experiment::V1::Experimentrun::Algorithmb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.experiment.v1.experimentrun.algorithm.toy_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n:com.com.terraquantum.experiment.v1.experimentrun.algorithmB\010ToyProtoP\001ZZterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm\242\002\006CTEVEA\252\0026Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm\312\0026Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\342\002BCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\GPBMetadata\352\002;Com::Terraquantum::Experiment::V1::Experimentrun::Algorithm'
  _globals['_TOYPARAMETERSPROTO'].fields_by_name['n']._options = None
  _globals['_TOYPARAMETERSPROTO'].fields_by_name['n']._serialized_options = b'\272H\004\032\002 \000'
  _globals['_TOYMETADATAPROTO'].fields_by_name['parameters']._options = None
  _globals['_TOYMETADATAPROTO'].fields_by_name['parameters']._serialized_options = b'\272H\003\310\001\001'
  _globals['_TOYOUTCOMEPROTO'].fields_by_name['result']._options = None
  _globals['_TOYOUTCOMEPROTO'].fields_by_name['result']._serialized_options = b'\272H\003\310\001\001'
  _globals['_TOYPARAMETERSPROTO']._serialized_start=153
  _globals['_TOYPARAMETERSPROTO']._serialized_end=228
  _globals['_TOYINPUTSPROTO']._serialized_start=230
  _globals['_TOYINPUTSPROTO']._serialized_end=246
  _globals['_TOYMETADATAPROTO']._serialized_start=249
  _globals['_TOYMETADATAPROTO']._serialized_end=496
  _globals['_TOYRESULTPROTO']._serialized_start=498
  _globals['_TOYRESULTPROTO']._serialized_end=572
  _globals['_TOYOUTPUTSPROTO']._serialized_start=574
  _globals['_TOYOUTPUTSPROTO']._serialized_end=591
  _globals['_TOYOUTCOMEPROTO']._serialized_start=594
  _globals['_TOYOUTCOMEPROTO']._serialized_end=814
# @@protoc_insertion_point(module_scope)
