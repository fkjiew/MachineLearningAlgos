import numpy as np
from .base_layer import BaseLayer

class Loss(BaseLayer):
    def __init__(self,weights=1):
        self.input_unit = None
        self.output_unit = None
        self.weights = weights

        self.loss = 0
        self.loss_d = 0

    def plug(self,intputlayer):
        assert len(intputlayer.output_shape) == 1, "Input of Loss layer must be a vector"
        self.input_shape = intputlayer.output_shape[0]
        self.output_shape = self.input_shape

        self.input_unit = intputlayer
        intputlayer.output_unit = self

        self.zin = 0
    
    def forward(self,X,y):
        self.zin = self.input_unit.forward(X)
        self.loss = self.loss_function(self.zin,y)
        return self.loss

    def backprop(self,y):
        self.loss_d = self.deriv(self.zin,y.reshape(self.zin.shape))
        return self.loss_d

    def loss_function(self,y_pred,y_true):
        raise NotImplementedError("Function not supposed to call, class is only a base")
    
    def deriv(self,y_pred,y_true):
        raise NotImplementedError("Function not supposed to call, class is only a base")

class MSE(Loss):
    def loss_function(self,y_pred,y_true):
        return np.mean(self.weights*(y_pred- y_true)**2)
    
    def deriv(self,y_pred,y_true):
        return 2*(y_pred - y_true) *self.weights

class MAE(Loss):
    def loss_function(self,y_pred,y_true):
        return np.mean(np.abs(y_pred-y_true)*self.weights)

    def deriv(self,y_pred,y_true):
        return np.sign((y_pred-y_true)*self.weights)

class BinaryCrossEntropy(Loss):
    def loss_function(self,y_pred,y_true):
        return np.mean((-y_true * np.log(y_pred) - (1 - y_true) * np.log(1 - y_pred))*self.weights)
    
    def deriv(self,y_pred,y_true):
        return (y_pred - y_true) * self.weights