import tensorflow as tf

class Log_cosh_diceLoss(object): #creating a new class
    def __init__(self):

        self.smooth = 1e-6 #self allows initialization/declaration of values in tf

    def __call__(self, ground_truth, predictions):

        intersection = tf.reduce_sum(ground_truth * predictions, axis = (1, 2)) #axis is width and height
        union = tf.reduce_sum(ground_truth + predictions, axis = (1, 2)) #tf.reduce_sum is required to do for whole image not one pixel
        dice = (2 * intersection + self.smooth)/ (union + self.smooth) #self.smooth is required according to TingHan
        dice_loss = 1 - dice

        coshdiceloss = tf.cosh(dice_loss) #using math operations of tf
        logcoshdiceloss = tf.log(dice_loss)

        return logcoshdiceloss

        #need to change the ground truth and predictions to different type - type cast to float...


