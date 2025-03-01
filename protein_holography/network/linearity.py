#
# Linearity class for use in holographic neural networks.
# 
# Layer takes inputs f_{i-1} of shape l x c(l,i-1) x m(l)
# and contracts it with weights W_{i} of shape c(l,i-1) x c(l,i).
# It returns the contracted product as output.
#
# In einstein notation, the equation for this layer is
#
#     g^i_{l,c(l,i),m(l)} = W^i_{c(l,i-1),c(l,i)} f^{i-1}_{l,c(l,i-1),m(l)}
#

import tensorflow as tf

class Linearity(tf.keras.layers.Layer):
    def __init__(self, l_dims, layer_id, L_MAX, reg_strength, scale=1.0, **kwargs):
        super().__init__(**kwargs)
        self.l_dims = l_dims # list of channel dimension for each order l
        self.L_MAX = L_MAX
        self.layer_id = layer_id # typically the number of the layer in the network
        self.scale = scale
        self.reg_strength = reg_strength

    # set up the weight matrices used in the linear combination
    def build(self, input_shape): # input takes shape l x c(l,i-1) x m(l)
        weights_initializer = tf.keras.initializers.GlorotUniform()

        # lists for the input and output dims with l indexing the list
        # input_dims := c(l,i-1)
        # output_dims := c(l,i) 
        input_dims = [input_shape[l][1] for l in range(self.L_MAX + 1)]
        output_dims = self.l_dims

        weights_real = {}
        weights_imag = {}
        weights_complex = {}
        for l in range(self.L_MAX + 1):
            weights_real[l] = self.add_weight(shape=[input_dims[l],
                                                     output_dims[l]],
                                              dtype=tf.dtypes.float32,
                                              initializer=weights_initializer,
                                              regularizer=tf.keras.regularizers.l1(self.reg_strength),
                                              trainable=True,
                                              name="W_real_" + str(self.layer_id) + "_" + str(l))


            weights_imag[l] = self.add_weight(shape=[input_dims[l],
                                                     output_dims[l]],
                                              dtype=tf.dtypes.float32,
                                              initializer=weights_initializer,
                                              regularizer=tf.keras.regularizers.l1(self.reg_strength),
                                              trainable=True,
                                              name="W_imag_" + str(self.layer_id) + "_" + str(l))

        self.weights_ = {}
        self.weights_real = {}
        self.weights_imag = {}
        for l in range(self.L_MAX + 1):
            self.weights_real[str(l)] = weights_real[l]
            self.weights_imag[str(l)] = weights_imag[l]
            


    # compute the layer via tensor contraction
    @tf.function
    def call(self, input,training=None): 
        output = {}
        for l in range(self.L_MAX + 1):
#            output[l] = tf.einsum("ij,bim->bjm",self.weights_[l],input[l])
            output[l] = tf.einsum("ij,bim->bjm",tf.complex(self.weights_real[str(l)],self.weights_imag[str(l)],
                                          name="W_complex" + str(self.layer_id) + "_" + str(l))
                                  ,input[l]/self.scale)
        return output
