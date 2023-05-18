
from ipa.tasks import lane_detection_task
from ipa.configs import lane_detection as lanecfg
from official.core import input_reader
from ipa.dataloaders import lane_input 

import matplotlib.pyplot as plt
import dataclasses
from official.modeling import hyperparams
from official.core import config_definitions as cfg
import tensorflow as tf

from ipa.modeling.layers import detection_generator
from official.vision.beta.ops import box_ops as bops
from ipa.ops import box_ops as bops

from official.core import input_reader
from ipa.configs import lane_detection as lda
from ipa.utils.demos import utils
from ipa.data.create_bdd100k_tf_record import CATEGORIES, LANECATEGORIES
import matplotlib.pyplot as plt
import matplotlib

def test_lane_input_task():
  matplotlib.use('TkAgg')
  config = lanecfg.LaneDetectionTask(
        model=lanecfg.LaneDetector(
            min_level=3,
            norm_activation=lanecfg.common.NormActivation(activation='mish'),
            _boxes=['(12, 16)', '(40, 28)', '(76, 55)', '(142, 110)', '(192, 243)', '(459, 401)']))
  task = lane_detection_task.LaneDetectionTask(config)

  test_data = task.build_inputs(config.train_data)
  return test_data

def run_lane_data(dataset):
  dataset = dataset.take(10)
  drawer = utils.DrawBoxes(classes=12, labels=list(CATEGORIES.keys()))
  lane_drawer = utils.DrawLanes(classes=8, labels=list(LANECATEGORIES.keys()))
  shind = 0
  alpha = 0.8
  for i, (image, objects) in enumerate(dataset):
    fig, axe = plt.subplots(1, 5)
    # print(objects.keys())
    # image, boxes, lanes, masks = map_dict(objects)

    # # mask = masks['masks']
    # g = tf.convert_to_tensor([[[0.0, 1.0, 0.0]]])
    # b = tf.convert_to_tensor([[[0.0, 0.0, 1.0]]])
    # # image = tf.where(tf.logical_or(mask == g, mask == b), alpha * image + (1 - alpha) * mask, image)
    # mask = objects['masks']
    # image = tf.where(tf.logical_or(mask == g, mask == b), alpha * image + (1 - alpha) * mask, image)

    gt = objects['objects']['true_conf']
    obj3 = gt['3'][..., 0]
    # obj4 = gt['4'][..., 0]
    # obj5 = gt['5'][..., 0]

    i_ = drawer(image.numpy(), objects['objects'])
    i_ = lane_drawer(i_, objects['lanes'])

    # print(bops.yxyx_to_xcycwh(  objects['objects']['bbox']))

    _, lane_grid, _ = tf.split(objects['lanes']['grid']['2'], [2, 1, -1], axis = -1)

    axe[0].imshow(i_[shind])
    axe[1].imshow(image[shind])
    axe[2].imshow(obj3[shind, ..., 0:3].numpy())
    axe[3].imshow(obj3[shind, ..., 3:6].numpy())
    axe[4].imshow(lane_grid[shind, ..., 0].numpy())

    
    fig.set_size_inches(16.5, 5.5, forward=True)
    plt.tight_layout()
    plt.show()
    # image = lane_drawer(image, lanes)



if __name__ == '__main__':
  dataset = test_lane_input_task()
  run_lane_data(dataset)
