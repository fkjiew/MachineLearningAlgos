import numpy as np

class RidgeClassifier: # TODO adapt to n class
    def __init__(self,lambd=1):
        self.lambd  = lambd
        self.beta = 0

    def fit(self,X,y):
        self.labels = np.unique(y)
        assert len(self.labels) == 2, "Only 2 class can be given to this classifier"

        # Renamed labels as 1 and -1
        y[y == self.labels[0]] = 1
        y[y == self.labels[1]] = -1

        X = np.concatenate((np.ones((X.shape[0],1)),X),axis=1) # add column of 1 for the bias
        self.beta = np.linalg.inv(self.lambd*np.identity(X.shape[1]) + X.T @ X) @ X.T @ y

    def predict(self,X):    
        X = np.concatenate((np.ones((X.shape[0],1)),X),axis=1) # add column of 1 for the bias
        y_hat  = np.where((X @ self.beta) >0,self.labels[0],self.labels[1])
        return y_hat

    def score(self,X,y):
        y_hat  = self.predict(X)
        acc  = np.count_nonzero(np.array(y_hat)==np.array(y)) /len(y)
        return acc