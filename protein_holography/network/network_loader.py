import os

import tensorflow as tf

from  protein_holography.network import hnn
from protein_holography.network import clebsch


def load_network_from_weights(saved_network):
    # parameters of the network
    # parameters commented out were only necessary to load the data or for training
    # but are listed here for completeness

                 
    netL = int(saved_network.split('netL=')[1].split('_')[0])
    l = int(saved_network.split('l=')[1].split('_')[0])
    k = range(21)
    projection = 'zgram'
    e = 10000
    eVal = 128
    nlayers = int(saved_network.split('nlayers=')[1].split('_')[0])
    hdim = int(saved_network.split('hdim=')[1].split('_')[0])
    learnrate = float(saved_network.split('learnrate=')[1].split('_')[0])
    bsize = int(saved_network.split('bsize=')[1].split('_')[0])
    rmax = 10.
    scale = 1.
    dropout = float(saved_network.split('dropout_rate=')[1].split('_')[0])
    reg = float(saved_network.split('reg_strength=')[1].split('_')[0])
    n_dense = int(saved_network.split('n_dense=')[1].split('_')[0])
    ch = 'casp12'
    d = 10.
    
    nclasses=20

    datadir = '/gscratch/spe/mpun/protein_holography/data'
    cg_file = os.path.join(datadir, "CG_matrix_l=13.npy")
    tf_cg_matrices = clebsch.load_clebsch(cg_file, netL)
    
    hidden_l_dims = [[hdim] * (netL + 1)] * nlayers

    network = hnn.hnn(netL,hidden_l_dims,nlayers,
                      nclasses,tf_cg_matrices,n_dense,
                      reg,dropout,scale,
                      connection='full'
    )
    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=1e-2,
        decay_steps=10000,
        decay_rate=0.9
    )
    optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
    #tf.function
    def loss_fn(truth, pred):
        return tf.nn.softmax_cross_entropy_with_logits(
            labels = truth,
            logits = pred)
    
    network.compile(optimizer=optimizer,
                    loss=loss_fn,
                    metrics =['categorical_accuracy'])
    return network
