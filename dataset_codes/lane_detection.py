import tensorflow as tf
from typing import ClassVar, Dict, List, Optional, Tuple, Union
import dataclasses
import os

from official.core import exp_factory
from official.modeling import hyperparams
from official.modeling import optimization
from official.modeling.hyperparams import config_definitions as cfg
from official.vision.beta.configs import common

from ipa.configs import backbones
from ipa.configs import yolo
import numpy as np

class ModelConfig(yolo.ModelConfig):
  @property
  def input_size(self):
    if self._input_size is None:
      return [None, None, 3]
    else:
      return self._input_size

  @input_size.setter
  def input_size(self, input_size):
    self._input_size = input_size


# dataset parsers
@dataclasses.dataclass
class Mosaic(hyperparams.Config):
  output_size: List[int] = dataclasses.field(default_factory=lambda: [640, 640])
  mosaic_frequency: float = 0.0
  crop_area: List[int] = dataclasses.field(default_factory=lambda: [0.25, 1.0])
  crop_area_mosaic: List[int] = dataclasses.field(
      default_factory=lambda: [0.25, 0.75])
  random_crop: bool = True
  random_crop_mosaic: bool = False

@dataclasses.dataclass
class Parser(hyperparams.Config):
  image_w: int = 512
  image_h: int = 512
  fixed_size: bool = True
  max_num_instances: int = 200
  min_process_size: int = 512
  letter_box: bool = False
  random_flip: bool = True
  pct_rand: float = 0.0
  jitter_im: float = 0.6
  aug_scale_aspect: float = 0.3
  aug_rand_translate: float = 0.00
  aug_rand_saturation: float = 0.75  #1.5
  aug_rand_brightness: float = 0.5  #1.5
  aug_rand_hue: float = 0.1  #0.015
  aug_scale_min: float = 0.3
  aug_scale_max: float = 2.0
  aug_rand_angle: float = 10.0
  use_tie_breaker: bool = True
  use_scale_xy: bool = False
  anchor_thresh: float = 0.213
  mosaic: Mosaic = Mosaic()

#bdd100k dataset path
@dataclasses.dataclass
class TfBDD100kDecoder(hyperparams.Config):
  regenerate_source_id: bool = False
  input_path: str = '/Users/bradjeon/dataset/Dataset/bdd100k-val*'

@dataclasses.dataclass
class TFDSCOCODecder(hyperparams.Config):
  regenerate_source_id: bool = False
  tfds_name: str = 'coco/panoptic'
  tfds_split: str = 'train'

@dataclasses.dataclass
class DataDecoder(hyperparams.OneOfConfig):
  type: Optional[str] = 'bdd100k'
  bdd100k: TfBDD100kDecoder = TfBDD100kDecoder()
  coco_tfds: TFDSCOCODecder = TFDSCOCODecder()

@dataclasses.dataclass
class DataConfig(cfg.DataConfig):
  """Input config for training."""
  decoder: DataDecoder = DataDecoder(type = "bdd100k") # the data set being used
  input_path: str = '/Users/bradjeon/dataset/Dataset/bdd100k-val*'
  global_batch_size: int = 32
  is_training: bool = True
  dtype: str = 'float32'
  tfds_data_dir: str = ''
  tfds_download: bool = True
  shuffle_buffer_size: int = 100
  parser: Parser = Parser()

def _build_dict(min_level, max_level, value):
  return lambda: {str(key): value for key in range(min_level, max_level + 1)}

def _build_path_scales(min_level, max_level):
  return lambda: {str(key): 2**key for key in range(min_level, max_level + 1)}

@dataclasses.dataclass
class LaneLossLayer(hyperparams.Config):
  min_level: int = 2
  max_level: int = 2
  ignore_thresh: Dict = dataclasses.field(
      default_factory=_build_dict(min_level, max_level, 0.13))
  det_thresh: float = 0.25
  point_normalizer: Dict = dataclasses.field(
      default_factory=_build_dict(min_level, max_level, 0.75))
  cls_normalizer: Dict = dataclasses.field(
      default_factory=_build_dict(min_level, max_level, 1.0))
  det_normalizer: Dict = dataclasses.field(
      default_factory=_build_dict(min_level, max_level, 1.0))
  max_delta: Dict = dataclasses.field(
      default_factory=_build_dict(min_level, max_level, np.inf))
  scale_xy: Dict = dataclasses.field(
      default_factory=_build_dict(min_level, max_level, 2.5))
  path_scales: Dict = dataclasses.field(
      default_factory=_build_path_scales(min_level, max_level))
  objectness_smooth: Dict = dataclasses.field(
      default_factory=_build_dict(min_level, max_level, 0.75))
  nms_thresh: float = 0.6
  max_points: int = 200

@dataclasses.dataclass
class LaneDetector(ModelConfig):
  _input_size: Optional[List[int]] = dataclasses.field(default_factory=lambda:[512, 512, 3])
  object_classes: int = 12 # if 0 then ignore boxes in the pipeline
  lane_classes: int = 8 # if 0 then ignore lanes in pipeline
  lane_instance_classes: int = 3 # if 0 ignore lane segmentations
  
  backbone: backbones.Backbone = backbones.Backbone(
      type='darknet', darknet=backbones.DarkNet(model_id='cspdarknet53', dilate=False))

  subdivisions: int = 1
  boxes_per_scale: int = 6
  lanes_per_scale: int = 1
  pan_filters: int = 512
  pan_route_len: int = 6
  pan_csp: bool = True
  pan_insert_spp: bool = False
  mta_filters: int = 256 
  mta_route_len: int = 5
  mta_csp: bool = False
  mta_insert_spp: bool = True
  
  lane_loss_scale: float = 0.5
  object_loss_scale: float = 0.5

  min_level: int = 2
  max_level: int = 5
  dilate: bool = True
  object_filter: yolo.YoloLossLayer = yolo.YoloLossLayer(min_level= 3,
                                                         max_level= 3)
  lane_filter: yolo.YoloLossLayer = LaneLossLayer(min_level=2,
                                                  max_level=2)

  norm_activation: common.NormActivation = common.NormActivation(
      activation='mish',
      use_sync_bn=True,
      norm_momentum=0.99,
      norm_epsilon=0.001)

  darknet_weights_file: str = 'yolov4.weights'
  darknet_weights_cfg: str = 'yolov4.cfg'
  decoder_activation: str = 'leaky'
  _boxes: Optional[List[str]] = dataclasses.field(default_factory=lambda: [
      '(12, 16)', '(40, 28)', '(76, 55)', '(142, 110)', '(192, 243)', '(459, 401)'])

@dataclasses.dataclass
class LaneDetectionTask(cfg.TaskConfig):
  model: LaneDetector = LaneDetector()
  train_data: DataConfig = DataConfig(is_training=True)
  validation_data: DataConfig = DataConfig(is_training=False)
  weight_decay: float = 5e-4
  
  gradient_clip_norm: float = 0.0
  per_category_metrics: bool = False

  load_darknet_weights: bool = True
  darknet_load_decoder: bool = False
  init_checkpoint_modules: str = 'backbone'
  annotation_file: Optional[str] = None

@exp_factory.register_config_factory('lane_custom')
def lane_custom() -> cfg.ExperimentConfig:
  train_batch_size = 2
  validation_batch_size = 2
  num_batches = 180000
  validation_size = 10000
  default_batch_size = 64

  config = cfg.ExperimentConfig(
      runtime=cfg.RuntimeConfig(
          mixed_precision_dtype='float16',
          loss_scale='dynamic',
          num_gpus=1),
      task=LaneDetectionTask(
          model=LaneDetector(),
          train_data=DataConfig(  
              input_path='/media/vbanna/DATA_SHARE/Lane_detection_raw/bdd-lane/bdd100k/records/records_points*', 
              is_training=True,
              global_batch_size=train_batch_size, 
              parser=Parser(),
              drop_remainder=True, 
              shuffle_buffer_size=2),
          validation_data=DataConfig(
              input_path='/media/vbanna/DATA_SHARE/Lane_detection_raw/bdd-lane/bdd100k/records/records_points*', 
              is_training=False,
              global_batch_size=validation_batch_size,
              parser=Parser(),
              drop_remainder=True, 
              shuffle_buffer_size=2)),
      trainer=cfg.TrainerConfig(
          steps_per_loop=2000,
          summary_interval=2000,
          checkpoint_interval=10000,
          train_steps=int(num_batches * default_batch_size / train_batch_size),
          validation_steps=validation_size//validation_batch_size,
          validation_interval=2000,
          optimizer_config=optimization.OptimizationConfig({
              'optimizer': {
                  'type': 'sgd',
                  'sgd': {
                      'momentum': 0.9
                  }
              },
              'learning_rate': {
                  'type': 'stepwise',
                  'stepwise': {
                      'boundaries': [
                          int(num_batches * 0.8 * default_batch_size / train_batch_size),
                          int(num_batches * 0.9 * default_batch_size / train_batch_size)
                      ],
                      'values': [
                          0.00261 * train_batch_size / default_batch_size,
                          0.000261 * train_batch_size / default_batch_size,
                          0.0000261 * train_batch_size / default_batch_size
                      ]
                  }
              },
              'warmup': {
                  'type': 'polynomial',
                  'polynomial': {
                      'warmup_steps': int(1000 * default_batch_size / train_batch_size),
                      'power': 4
                  }
              }
          })),
      restrictions=[
          'task.train_data.is_training != None',
          'task.validation_data.is_training != None'
      ])

  return config
