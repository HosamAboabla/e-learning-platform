from tensorflow.python.keras.backend import set_session
import tensorflow as tf

tf_config = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=2)
sess = tf.compat.v1.Session(config=tf_config)
graph = tf.compat.v1.get_default_graph()

set_session(sess)