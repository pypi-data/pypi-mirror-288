# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/experiment/v1/experimentrun/algorithm/circuit_run.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.experiment.v1.experimentrun.algorithm import shared_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_shared__pb2
from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nHcom/terraquantum/experiment/v1/experimentrun/algorithm/circuit_run.proto\x12\x36\x63om.terraquantum.experiment.v1.experimentrun.algorithm\x1a\x43\x63om/terraquantum/experiment/v1/experimentrun/algorithm/shared.proto\x1a\x1b\x62uf/validate/validate.proto\"\xb4\x01\n\x19\x43ircuitRunParametersProto\x12\x1d\n\x05shots\x18\x01 \x01(\x05\x42\x07\xbaH\x04\x1a\x02 \x00R\x05shots\x12x\n\x07\x62\x61\x63kend\x18\x02 \x01(\x0e\x32Q.com.terraquantum.experiment.v1.experimentrun.algorithm.CircuitRunnerBackendProtoB\x0b\xbaH\x08\x82\x01\x02\x10\x01\xc8\x01\x01R\x07\x62\x61\x63kend\"\x80\x01\n\x15\x43ircuitRunInputsProto\x12g\n\x07\x63ircuit\x18\x01 \x01(\x0b\x32M.com.terraquantum.experiment.v1.experimentrun.algorithm.ModelStorageInfoProtoR\x07\x63ircuit\"\x9f\x02\n\x17\x43ircuitRunMetadataProto\x12y\n\nparameters\x18\x03 \x01(\x0b\x32Q.com.terraquantum.experiment.v1.experimentrun.algorithm.CircuitRunParametersProtoB\x06\xbaH\x03\xc8\x01\x01R\nparameters\x12m\n\x06inputs\x18\x04 \x01(\x0b\x32M.com.terraquantum.experiment.v1.experimentrun.algorithm.CircuitRunInputsProtoB\x06\xbaH\x03\xc8\x01\x01R\x06inputsJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03R\x05shotsR\x07\x62\x61\x63kend\"}\n\x16\x43ircuitRunOutputsProto\x12\x63\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.DatasetStorageInfoProtoR\x04\x64\x61ta\"\xa2\x01\n\x16\x43ircuitRunOutcomeProto\x12\x1e\n\x06result\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x06result\x12h\n\x07outputs\x18\x02 \x01(\x0b\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.CircuitRunOutputsProtoR\x07outputs*}\n\x19\x43ircuitRunnerBackendProto\x12&\n\"CIRCUIT_RUNNER_BACKEND_UNSPECIFIED\x10\x00\x12\x07\n\x03IBM\x10\x01\x12\x08\n\x04IONQ\x10\x02\x12\x12\n\x0e\x43IRQ_SIMULATOR\x10\x03\x12\x11\n\rIBM_SIMULATOR\x10\x04\x42\xa9\x03\n:com.com.terraquantum.experiment.v1.experimentrun.algorithmB\x0f\x43ircuitRunProtoP\x01ZZterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm\xa2\x02\x06\x43TEVEA\xaa\x02\x36\x43om.Terraquantum.Experiment.V1.Experimentrun.Algorithm\xca\x02\x36\x43om\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\xe2\x02\x42\x43om\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\GPBMetadata\xea\x02;Com::Terraquantum::Experiment::V1::Experimentrun::Algorithmb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.experiment.v1.experimentrun.algorithm.circuit_run_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n:com.com.terraquantum.experiment.v1.experimentrun.algorithmB\017CircuitRunProtoP\001ZZterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm\242\002\006CTEVEA\252\0026Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm\312\0026Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\342\002BCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\GPBMetadata\352\002;Com::Terraquantum::Experiment::V1::Experimentrun::Algorithm'
  _globals['_CIRCUITRUNPARAMETERSPROTO'].fields_by_name['shots']._options = None
  _globals['_CIRCUITRUNPARAMETERSPROTO'].fields_by_name['shots']._serialized_options = b'\272H\004\032\002 \000'
  _globals['_CIRCUITRUNPARAMETERSPROTO'].fields_by_name['backend']._options = None
  _globals['_CIRCUITRUNPARAMETERSPROTO'].fields_by_name['backend']._serialized_options = b'\272H\010\202\001\002\020\001\310\001\001'
  _globals['_CIRCUITRUNMETADATAPROTO'].fields_by_name['parameters']._options = None
  _globals['_CIRCUITRUNMETADATAPROTO'].fields_by_name['parameters']._serialized_options = b'\272H\003\310\001\001'
  _globals['_CIRCUITRUNMETADATAPROTO'].fields_by_name['inputs']._options = None
  _globals['_CIRCUITRUNMETADATAPROTO'].fields_by_name['inputs']._serialized_options = b'\272H\003\310\001\001'
  _globals['_CIRCUITRUNOUTCOMEPROTO'].fields_by_name['result']._options = None
  _globals['_CIRCUITRUNOUTCOMEPROTO'].fields_by_name['result']._serialized_options = b'\272H\003\310\001\001'
  _globals['_CIRCUITRUNNERBACKENDPROTO']._serialized_start=1126
  _globals['_CIRCUITRUNNERBACKENDPROTO']._serialized_end=1251
  _globals['_CIRCUITRUNPARAMETERSPROTO']._serialized_start=231
  _globals['_CIRCUITRUNPARAMETERSPROTO']._serialized_end=411
  _globals['_CIRCUITRUNINPUTSPROTO']._serialized_start=414
  _globals['_CIRCUITRUNINPUTSPROTO']._serialized_end=542
  _globals['_CIRCUITRUNMETADATAPROTO']._serialized_start=545
  _globals['_CIRCUITRUNMETADATAPROTO']._serialized_end=832
  _globals['_CIRCUITRUNOUTPUTSPROTO']._serialized_start=834
  _globals['_CIRCUITRUNOUTPUTSPROTO']._serialized_end=959
  _globals['_CIRCUITRUNOUTCOMEPROTO']._serialized_start=962
  _globals['_CIRCUITRUNOUTCOMEPROTO']._serialized_end=1124
# @@protoc_insertion_point(module_scope)
