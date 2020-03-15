from game import Game
import numpy as np
import tensorflow as tf

game = Game()
input_size = game.side*game.side
output_size = 3
x = tf.placeholder(tf.float32, [None, input_size])
W = tf.Variable(tf.random_normal([input_size, output_size]))
b = tf.Variable(tf.random_normal([output_size])+0.1)
Wx_b = tf.add(tf.matmul(x, W), b)
y_ = tf.placeholder(tf.int64, [None])
loss = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=Wx_b)
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss)
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
for _ in range(1000):
    sess.run(train_step, feed_dict={x: np.load("board.npy"), y_: np.load("action.npy")})
correct_prediction = tf.equal(tf.argmax(Wx_b, 1), y_)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: np.load("board_test.npy"), y_: np.load("action_test.npy")}))


