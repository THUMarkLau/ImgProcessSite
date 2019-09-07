from ops import *
from utils import *
from glob import glob
import time
from tensorflow.contrib.data import prefetch_to_device, shuffle_and_repeat, map_and_batch
import numpy as np
import pdb

class my_UGATIT(object):
    def __init__(self, sess):
        self.sess = sess


    def test(self, img_data):
        tf.global_variables_initializer().run()
        self.saver = tf.train.Saver()
        #checkpoint_dir未知
        could_load, checkpoint_counter = self.load('checkpoint')
        sample_img = np.asarray(img_data)
        fake_img = self.sess.run(self.test_fake_B, feed_dict = {self.test_domain_A : sample_img})
        return fake_img


    def load(self, checkpoint_dir):
        print(" [*] Reading checkpoints...")

        #model_dir未知
        checkpoint_dir = os.path.join(checkpoint_dir, 'UGATIT_selfie2anime_lsgan_4resblock_6dis_1_1_10_10_1000_sn_smoothing')

        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        if ckpt and ckpt.model_checkpoint_path:
            ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
            self.saver.restore(self.sess, os.path.join(checkpoint_dir, ckpt_name))
            counter = int(ckpt_name.split('-')[-1])
            print(" [*] Success to read {}".format(ckpt_name))
            return True, counter
        else:
            print(" [*] Failed to find a checkpoint")
            return False, 0


    def build_model(self):
        self.test_domain_A = tf.placeholder(tf.float32, [1, self.img_size, self.img_size, self.img_ch], name='test_domain_A')
        self.test_domain_B = tf.placeholder(tf.float32, [1, self.img_size, self.img_size, self.img_ch], name='test_domain_B')


        self.test_fake_B, _ = self.generate_a2b(self.test_domain_A)
        self.test_fake_A, _ = self.generate_b2a(self.test_domain_B)



def generate_img(img_data):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
        gan = my_UGATIT(sess)
        gan.build_model()
        #result应为numpy数组
        result = gan.test(img_data)
        return result
