import numpy as np
import pickle
import gzip
import random
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))
def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))
class Neural_network(object):
    def __init__(self,lyrs):
        self.no_of_layers=len(lyrs)
        self.lyr_info=lyrs
        self.biases=[np.random.randn(y,1)
                    for y in lyrs[1:]]
        self.weights=[np.random.randn(x,y)
                    for x,y in zip(lyrs[1:],lyrs[:-1])]
    def feedfrwrd(self,a):
        for biase,weight in zip(self.biases,self.weights):
            a=sigmoid(np.dot(weight,a)+biase)
        return a
    def stochastic_grad_descent(self,training_data,epochs,mini_batch_len,lrng_r,test_data=None):
        if test_data: n_test=len(test_data)
        n=len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches=[training_data[k:k+mini_batch_len]
                          for k in range(0,n,mini_batch_len)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch,lrng_r)
            if test_data:
                print("Epoch{0}:{1}/{2}".format(j,self.evaluate(test_data),n_test))
            else:
                print("Epoch {0} complete".format(j))
    def update_mini_batch(self,mini_batch,eta):
        nabla_b=[np.zeros(b.shape) for b in self.biases]
        nabla_w=[np.zeros(w.shape) for w in self.weights]
        for x,y in mini_batch:
            delta_nabla_b,delta_nabla_w=self.backprop(x,y)
            nabla_b=[nb+dnb for nb,dnb in zip(nabla_b,delta_nabla_b)]
            nabla_w=[nw+dnw for nw,dnw in zip(nabla_w,delta_nabla_w)]
        self.weights=[w-(eta/len(mini_batch)*nw)
                      for w,nw in zip(self.weights,nabla_w)]
        self.biases=[b-(eta/len(mini_batch)*nb)
                     for b,nb in zip(self.biases,nabla_b)]
    def backprop(self,x,y):
        nabla_b=[np.zeros(b.shape) for b in self.biases]
        nabla_w=[np.zeros(w.shape) for w in self.weights]
        activation=x
        activations=[x]
        zs=[]
        for b,w in zip(self.biases,self.weights):
            z=np.dot(w,activation)+b
            zs.append(z)
            activation=sigmoid(z)
            activations.append(activation)
        delta=self.cost_derivative(activations[-1],y)*sigmoid_prime(zs[-1])
        nabla_b[-1]=delta
        nabla_w[-1]=np.dot(delta,activations[-2].transpose())
        for l in range(2,self.no_of_layers):
            z=zs[-l]
            sp=sigmoid_prime(z)
            delta=np.dot(self.weights[-l+1].transpose(),delta)*sp
            nabla_b[-l]=delta
            nabla_w[-l]=np.dot(delta,activations[-1-l].transpose())
        return (nabla_b,nabla_w)
    def evaluate(self,test_data):
        test_results=[(np.argmax(self.feedfrwrd(x)),y)
                      for (x,y) in test_data]
        return sum(int(x==y) for (x,y) in test_results)
    def cost_derivative(self,output_activations,y):
        return (output_activations-y)
def load_data():
    f=gzip.open('mnist.pkl.gz','rb')
    training_data,validation_data,test_data=pickle.load(f,encoding="latin1")
    f.close()
    return(training_data,validation_data,test_data)
def load_data_wrapper():
    tr_d, va_d, te_d = load_data()
    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [y for y in tr_d[1]]
    training_data = [(x,y) for x,y in zip(training_inputs, training_results)]
    print(len(training_data))
    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = [(x,y) for x,y in zip(validation_inputs, va_d[1])]
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = [(x,y) for x,y in zip(test_inputs, te_d[1])]
    return (training_data, validation_data, test_data)
def vectorized_result(j):
    e=np.zeros((10,1))
    e[j]=1.0
    return e
n_n=Neural_network([784,100,10])
training_data,validation_data,test_data=load_data_wrapper()
n_n.stochastic_grad_descent(training_data,35,10,3.0,test_data=test_data)

