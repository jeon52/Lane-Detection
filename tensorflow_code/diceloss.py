#this is an example that tinghan has given me so I can make my own logcosh dice loss function
import tensorflow as tf

class DiceLoss(object):

  def __init__(self):

    self.smooth = 1e-6

  def __call__(self, ground_truth, predictions):

    intersection = tf.reduce_sum(ground_truth * predictions, axis = (1, 2)) #axis is width and height
    union = tf.reduce_sum(ground_truth + predictions, axis = (1, 2))
    dice = (2*intersection + self.smooth)/ (union + self.smooth) #self.smooth is required according to TingHan
    dice_loss = 1 - dice
    return dice_loss


