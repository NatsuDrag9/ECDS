import numpy as np
import pickle
import gzip
import random
from tempfile import TemporaryFile
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
    def getVariables(self):
        return (self.weights,self.biases)
def vectorized_result(j):
    e=np.zeros((7,1))
    e[j]=1.0
    return e
def create_data():
    lst_string=[]
    lst_out=[]
    lst_numpy_arrays=[]
    lst_tst_string=[]
    lst_tst_out=[]
    test_data=[]
    training_data=[]
    with open("dataset.txt","r") as f:
        for line in f:
            process_lst=line.split(",")
            if(process_lst[2]=="Training\n" or process_lst[2]=="PublicTest\n" or process_lst[2]=="PrivateTest\n"):
                lst_string.append(process_lst[1])
                lst_out.append(process_lst[0])
            if(process_lst[2]=="PublicTest\n" or process_lst[2]=="PrivateTest\n"):
                lst_tst_string.append(process_lst[1])
                lst_tst_out.append(process_lst[0])
    lst_output=[int(x) for x in lst_out]
    lst_tst_output=[int(x) for x in lst_tst_out]
    index_c=0
    for x in lst_string:
        lst_temps=x.split(" ")
        lst_temp=[int(x)/255 for x in lst_temps]
        np_temp=np.array(lst_temp).reshape(2304,1)
        training_data.append((np_temp,vectorized_result(int(lst_output[index_c]))))
        index_c=index_c+1
    index_c=0
    for x in lst_tst_string:
        lst_temps=x.split(" ")
        lst_temp=[int(x)/255 for x in lst_temps]
        np_temp=np.array(lst_temp).reshape(2304,1)
        test_data.append((np_temp,lst_tst_output[index_c]))
        
        index_c=index_c+1
    return (training_data,test_data)
n_n=Neural_network([2304,50,7])
training_data,test_data=create_data()
n_n.stochastic_grad_descent(training_data,50,10,0.1,test_data=test_data)
wghts,bias=n_n.getVariables()
