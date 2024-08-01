# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/efq.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers import shared_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ml__layers_dot_shared__pb2
from com.terraquantum import default_value_pb2 as com_dot_terraquantum_dot_default__value__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nJcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/efq.proto\x12@com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers\x1a\x1b\x62uf/validate/validate.proto\x1aMcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/shared.proto\x1a$com/terraquantum/default_value.proto\"\xad\x05\n\x08\x45\x46QLayer\x12/\n\nnum_qubits\x18\x02 \x01(\x05\x42\x10\xbaH\x06\x1a\x04\x18\x19(\x01\x82\xa6\x1d\x03\x1a\x01\x04R\tnumQubits\x12&\n\x05\x64\x65pth\x18\x03 \x01(\x05\x42\x10\xbaH\x06\x1a\x04\x18\x08(\x01\x82\xa6\x1d\x03\x1a\x01\x04R\x05\x64\x65pth\x12\x92\x01\n\x10measurement_mode\x18\x04 \x01(\x0e\x32V.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.MeasurementModeProtoB\x0f\xbaH\x05\x82\x01\x02\x10\x01\x82\xa6\x1d\x03z\x01\x03R\x0fmeasurementMode\x12{\n\x08rotation\x18\x05 \x01(\x0e\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.MeasureProtoB\x0f\xbaH\x05\x82\x01\x02\x10\x01\x82\xa6\x1d\x03z\x01\x03R\x08rotation\x12\x82\x01\n\nentangling\x18\x06 \x01(\x0e\x32Q.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.EntanglingProtoB\x0f\xbaH\x05\x82\x01\x02\x10\x01\x82\xa6\x1d\x03z\x01\x02R\nentangling\x12y\n\x07measure\x18\x07 \x01(\x0e\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.MeasureProtoB\x0f\xbaH\x05\x82\x01\x02\x10\x01\x82\xa6\x1d\x03z\x01\x02R\x07measureJ\x04\x08\x01\x10\x02J\x04\x08\x08\x10\tJ\x04\x08\t\x10\nR\x0bin_featuresR\x0b\x64iff_methodR\nqubit_typeB\xdc\x03\nDcom.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layersB\x08\x45\x66qProtoP\x01Zdterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers\xa2\x02\x07\x43TEVEAM\xaa\x02?Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm.MlLayers\xca\x02?Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\xe2\x02KCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\\GPBMetadata\xea\x02\x45\x43om::Terraquantum::Experiment::V1::Experimentrun::Algorithm::MlLayersb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.efq_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\nDcom.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layersB\010EfqProtoP\001Zdterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers\242\002\007CTEVEAM\252\002?Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm.MlLayers\312\002?Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\342\002KCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\\GPBMetadata\352\002ECom::Terraquantum::Experiment::V1::Experimentrun::Algorithm::MlLayers'
  _globals['_EFQLAYER'].fields_by_name['num_qubits']._options = None
  _globals['_EFQLAYER'].fields_by_name['num_qubits']._serialized_options = b'\272H\006\032\004\030\031(\001\202\246\035\003\032\001\004'
  _globals['_EFQLAYER'].fields_by_name['depth']._options = None
  _globals['_EFQLAYER'].fields_by_name['depth']._serialized_options = b'\272H\006\032\004\030\010(\001\202\246\035\003\032\001\004'
  _globals['_EFQLAYER'].fields_by_name['measurement_mode']._options = None
  _globals['_EFQLAYER'].fields_by_name['measurement_mode']._serialized_options = b'\272H\005\202\001\002\020\001\202\246\035\003z\001\003'
  _globals['_EFQLAYER'].fields_by_name['rotation']._options = None
  _globals['_EFQLAYER'].fields_by_name['rotation']._serialized_options = b'\272H\005\202\001\002\020\001\202\246\035\003z\001\003'
  _globals['_EFQLAYER'].fields_by_name['entangling']._options = None
  _globals['_EFQLAYER'].fields_by_name['entangling']._serialized_options = b'\272H\005\202\001\002\020\001\202\246\035\003z\001\002'
  _globals['_EFQLAYER'].fields_by_name['measure']._options = None
  _globals['_EFQLAYER'].fields_by_name['measure']._serialized_options = b'\272H\005\202\001\002\020\001\202\246\035\003z\001\002'
  _globals['_EFQLAYER']._serialized_start=291
  _globals['_EFQLAYER']._serialized_end=976
# @@protoc_insertion_point(module_scope)
