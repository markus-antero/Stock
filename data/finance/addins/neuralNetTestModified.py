'''
Created on 24.2.2017

@author: Markus.Walden
'''

import quandl
import numpy as np
import numpy.linalg as lng
import time
import matplotlib.pyplot as plt
from scipy import optimize
from mpl_toolkits.mplot3d import Axes3D

quandl.ApiConfig.api_key = "2suZ1gv-896LK2WvuzaD"

class NeuralNetForward(object):
    '''
    classdocs
    * Normalize - apples to apples
    * notation (x*w = z)
        x = input 
        w - weight
        z - output quess
        y - actual output
        
    z2     $$z^{(2)}$$     Layer 2 activation     (numExamples, hiddenLayerSize)
    a2     $$a^{(2)}$$     Layer 2 activity     (numExamples, hiddenLayerSize)
    z3     $$z^{(3)}$$     Layer 3 activation     (numExamples, outputLayerSize)
    J     $$J$$     Cost     (1, outputLayerSize)
    '''
    x = np.array(([3,5],[5,1],[10,2],[7,3]), dtype=float) # hours sleeping, hours studying
    y = np.array(([75],[82],[93],[87]), dtype=float) # score
    
    testX = np.array(([4, 5.5], [4.5,1], [9,2.5], [6, 2]), dtype=float)
    testY = np.array(([70], [89], [85], [75]), dtype=float)
    
    def __init__(self, x, y, inputLayerSize = 2, outputLayerSize = 1, hiddenLayerSize = 3 ):
        '''
        Constructor - set values to input, output and hidden layer
        Randomly generate weights to synapsis based on the standard normal distribution.
            w1_inputToHidden = np.random.randn(self.inputLayer, self.hiddenLayer)
            w2_hiddentoOutput = np.random.randn(self.hiddenLayer, self.outputLayer)
        '''
        self.x = x
        self.y = y
        
        self.inputLayerSize = inputLayerSize
        self.outputLayerSize = outputLayerSize
        self.hiddenLayerSize = hiddenLayerSize
        
        self.w1_inputToHidden = np.random.randn(self.inputLayerSize, self.hiddenLayerSize)
        self.w2_hiddentoOutput = np.random.randn(self.hiddenLayerSize, self.outputLayerSize)
        
        print ("NeuralNetForward initialized with \ninput {0} \noutput{1}".format(self.x, self.y))

    def toDict(self):
        return {
            "inputVector": self.x,
            "outputVector": self.y,
            "inputLayerSize" : self.inputLayerSize,
            "outputLayerSize" : self.outputLayerSize,
            "hiddenLayerSize" : self.hiddenLayerSize,
            "w1_inputToHiddenSynapse,": self.w1_inputToHidden,
            "w2_hiddentoOutput": self.w2_hiddentoOutput,
            "quess": self.yHat,
            "derivative_w1": self.dJdW1,
            "derivative_w2": self.dJdW2,
            }

    def forward (self):
        #produce dot product(s) and run sigmoid to generate an estimate yHat 
        self.z2 = np.dot(self.x, self.w1_inputToHidden)
        self.a2 = self.sigmoid(self.z2)
        self.z3 = np.dot(self.a2, self.w2_hiddentoOutput)
        yHat = self.sigmoid(self.z3)
        
        print ("for input: {0} \noutput: {1}".format(self.x, yHat))
        return yHat
        
    def sigmoid (self, z):
        #sigmoid activation function to scalar or vector
        output = 1 / (1+np.exp(-z))
        print ("sigmoid activation for z: {0} \nWith output {1}".format(z, output))
        return output  
    
    def sigmoidPrime(self, z):
        #Derivative of sigmoid function
        output = np.exp(-z)/((1+np.exp(-z))**2)
        print ("sigmoid derivative for z: {0} \nWith output {1}".format(z, output))
        return output
    
    def costFunction(self):
        #Compute cost for given X,y, use weights already stored in class.
        self.yHat = self.forward()
        J = 0.5*sum((self.y-self.yHat)**2)
        return J
    
    def costFunctionPrime(self):
        '''
        Compute derivative with respect to W and W2 for a given X and y:
        populates: dJdW1, dJdW2 (self)
        returns Back propagating error for hidden LayerSize (delta2) and outputLayerSize (delta3)) 
        '''
        self.yHat = self.forward()
        
        delta3 = np.multiply(-(self.y-self.yHat), self.sigmoidPrime(self.z3))
        self.dJdW2 = np.dot(self.a2.T, delta3)
        
        delta2 = np.dot(delta3, self.w2_hiddentoOutput.T)*self.sigmoidPrime(self.z2)
        self.dJdW1 = np.dot(self.x.T, delta2)  
        
        return delta3, delta2    
    
    #Helper Functions for interacting with other classes:
    def getParams(self):
        #Get W1 and W2 unrolled into vector:
        params = np.concatenate((self.w1_inputToHidden.ravel(), self.w2_hiddentoOutput.ravel()))
        return params
    
    def setParams(self, params):
        #Set W1 and W2 using single paramater vector.
        W1_start = 0
        W1_end = self.hiddenLayerSize * self.inputLayerSize
        self.w1_inputToHidden = np.reshape(params[W1_start:W1_end], (self.inputLayerSize , self.hiddenLayerSize))
        W2_end = W1_end + self.hiddenLayerSize*self.outputLayerSize
        self.w2_hiddentoOutput = np.reshape(params[W1_end:W2_end], (self.hiddenLayerSize, self.outputLayerSize))
        
    def computeGradients(self):
        delta3, delta2 = self.costFunctionPrime()
        print ("Delta:t", delta3, delta2)
        return np.concatenate((self.dJdW1.ravel(), self.dJdW2.ravel()))

    def __repr__(self):
        '''
        String with 
            "inputLayer" : self.inputLayer                     - user defined
            "outputLayer" : self.outputLayer,                  - user defined
            "hiddenLayer" : self.hiddenLayer,                  - user defined
            "w1_inputToHiddenSynapse,": self.w1_inputToHidden, - (inputLayerSize, hiddenLayerSize)
            "w2_hiddentoOutput": self.w2_hiddentoOutput,       - (hiddenLayerSize, outputLayerSize)
            "quess": self.yHat,                                - Network output
            "derivative_w1": self.dJdW1,                       - Partial derivative of cost with respect to w1
            "derivative_w2": self.dJdW2,                       - Partial derivative of cost with respect to w2
        '''
        return str(self.toDict())

    '''
    static methods
    '''        
    @staticmethod
    def computeNumericalGradient(nn):
        #Get the synapsis  w1_inputToHidden and w2_HiddenToOutput unrolled into vector (using ravel())):
        paramsInitial = nn.getParams()
        
        numgrad = np.zeros(paramsInitial.shape)
        perturb = np.zeros(paramsInitial.shape)
        e = 1e-4

        for p in range(len(paramsInitial)):
            #Set perturbation vector
            perturb[p] = e
            nn.setParams(paramsInitial + perturb)
            loss2 = nn.costFunction()
            
            nn.setParams(paramsInitial - perturb)
            loss1 = nn.costFunction()

            #Compute Numerical Gradient
            numgrad[p] = (loss2 - loss1) / (2*e)

            #Return the value we changed to zero:
            perturb[p] = 0
            
        #Return Params to original value:
        nn.setParams(paramsInitial)
        return numgrad

    @staticmethod
    def bruteforceCost(nn, iteration = 1000, weightsToTry = np.linspace(-5,5,1000)):   
        costs = np.zeros(1000)
        startTime = time.clock()
        for i in range(1000):
            nn.w1_inputToHidden[0,0] = weightsToTry[i]
            yHat = nn.forward(nn.x)
            costs[i] = 0.5*sum((nn.y-yHat)**2)
        
        endTime = time.clock()
        timeElapsed = endTime-startTime
        return costs, timeElapsed


class NNtrainer(NeuralNetForward):
    def __init__(self, x, y, testX, testY, Lambda=0):
        #Make Local reference to network:
        super().__init__(x = x, y = y)
        self.testX = testX
        self.testY = testY
        self.Lambda = Lambda
        print ("testing enabled")

        
    def costFunction(self, x, y):
        #Compute cost for given X,y, use weights already stored in class.
        self.yHat = self.forward(x)
        #We don't want cost to increase with the number of examples, so normalize by dividing the error term by number of examples(X.shape[0])
        J = 0.5*sum((y-self.yHat)**2)/x.shape[0] + (self.Lambda/2)*(sum(self.w1_inputToHidden**2)+sum(self.w2_hiddentoOutput**2))
        return J

    def costFunctionPrime(self, x, y):
        #Compute derivative with respect to W and W2 for a given X and y:
        self.yHat = self.forward(x)
    
        delta3 = np.multiply(-(y-self.yHat), self.sigmoidPrime(self.z3))
        #Add gradient of regularization term:
        self.dJdW2 = np.dot(self.a2.T, delta3)/x.shape[0] + self.Lambda*self.w2_hiddentoOutput
    
        delta2 = np.dot(delta3, self.w2_hiddentoOutput.T)*self.sigmoidPrime(self.z2)
        #Add gradient of regularization term:
        self.dJdW1 = np.dot(x.T, delta2)/x.shape[0] + self.Lambda*self.w1_inputToHidden
    
        return delta3, delta2

    def forward (self, x):
        #produce dot product(s) and run sigmoid to generate an estimate yHat 
        self.z2 = np.dot(x, self.w1_inputToHidden)
        self.a2 = self.sigmoid(self.z2)
        self.z3 = np.dot(self.a2, self.w2_hiddentoOutput)
        yHat = self.sigmoid(self.z3)
        
        print ("for input: {0} \noutput: {1}".format(self.x, yHat))
        return yHat

    
    def computeGradients(self, x, y):
        _, _ = self.costFunctionPrime(x, y)
        return np.concatenate((self.dJdW1.ravel(), self.dJdW2.ravel()))
        
    def callbackF(self, params, x, y):
        print ("with imput: {0} \noutput: {1}\n".format(x,y))
        
        self.setParams(params)
        self.J.append(self.costFunction(self.x, self.y)) 
        self.testJ.append(self.costFunction(self.testX, self.testY))   
        
    def costFunctionWrapper(self, params, x, y):
        print ("with imput: {0} \noutput: {1}\n".format(x,y))
        
        self.setParams(params)
        cost = self.costFunction(self.x, self.y)
        grad = self.computeGradients(self.x, self.y)
        
        return cost, grad
        
    def train(self):
        #Make an internal variable for the callback function:
        #Make empty list to store costs:
        self.J = []
        self.testJ = []
        
        params0 = self.getParams()

        options = {'maxiter': 200, 'disp' : True}
        _res = optimize.minimize(self.costFunctionWrapper, params0, jac=True, method='BFGS', \
                                 args=(self.x, self.y), options=options, callback=self.callbackF) #

        self.setParams(_res.x)
        self.optimizationResults = _res

def main ():
    '''
    generate data 
    add secondary testing data
    Initialize and test network
    create instances to train and test  
    generate trained network
    print untrained, trained details
    '''
    x = NeuralNetForward.x/np.amax(NeuralNetForward.x, axis = 0)
    y = NeuralNetForward.y/100
    testX = NeuralNetForward.testX/np.amax(NeuralNetForward.testX, axis = 0)
    testY = NeuralNetForward.testY/100   
    plotSleepStudy(x, y)
    plotSleepStudy(testX, testY)
    
    allInputs, hoursSleep, hoursStudy = generateSampleData (sampleSize = 100, max = 10, min = 0)
    nn = NeuralNetForward(x = x, y = y)
    
    numgrad = NeuralNetForward.computeNumericalGradient(nn)
    grad = nn.computeGradients()
    if lng.norm(grad-numgrad)/lng.norm(grad+numgrad) < 1e-7:
        print (nn.costFunctionPrime())
        print (nn.forward())
        print (lng.norm(grad-numgrad)/lng.norm(grad+numgrad))    
        plotTest(nn)

    t = NNtrainer(x = x, y = y, testX=testX, testY=testY, Lambda=0.1) 

#    t.train()   
#    plotTraining(t)
    
#    t.x = allInputs
#    allOutputs = t.forward()
#    t.y = allOutputs
    
    yy = np.dot(hoursStudy.reshape(100,1), np.ones((1,100)))
    xx = np.dot(hoursSleep.reshape(100,1), np.ones((1,100))).T
#    plotContour(t, allOutputs, xx, yy)
#    plotModel3D(allOutputs, xx, yy)
    
    print ("Object n: ", nn)
#    print ("object t: ", t)
    
def plotSleepStudy(x, y):
    fig = plt.figure(0,(8,3))
    
    plt.subplot(1,2,1)
    plt.scatter(x[:,0], y)
    plt.grid(1)
    plt.xlabel('Hours Sleeping')
    plt.ylabel('Test Score')
    
    plt.subplot(1,2,2)
    plt.scatter(x[:,1], y)
    plt.grid(1)
    plt.xlabel('Hours Studying')
    plt.ylabel('Test Score')
    plt.show()
    
def plotModel3D(output, xx, yy):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    surf = ax.plot_surface(xx, yy, 100*output.reshape(100, 100), cmap=plt.cm.get_cmap('rainbow'))
    
    ax.set_xlabel('Hours Sleep')
    ax.set_ylabel('Hours Study')
    ax.set_zlabel('Test Score')
    plt.show()
    
def plotContour(t, output, xx, yy):     
    CS = plt.contour(xx,yy,100*output.reshape(100, 100))
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('Hours Sleep')
    plt.ylabel('Hours Study')
    plt.show()
    
def plotTraining(t):
    
    plt.plot(t.J)
    plt.plot(t.testJ)
    plt.grid(1)
    plt.xlabel('Iterations')
    plt.ylabel('Cost')
    plt.show()
    
def plotTest(nn):
    testValues = np.arange(-5,5,0.01)
    plt.plot(testValues, nn.sigmoid(testValues), linewidth=2)
    plt.plot(testValues, nn.sigmoidPrime(testValues), linewidth=2)
    plt.grid(1)
    plt.legend(['sigmoid', 'sigmoidPrime'])
    plt.show()
    
def generateSampleData (sampleSize = 100, max = 10, min = 0):
    #Test network for various combinations of sleep/study:
    hoursSleep = np.linspace(min, max, sampleSize)
    hoursStudy = np.linspace(min, max/2, sampleSize)
    
    #Normalize data (same way training data way normalized)
    hoursSleepNorm = hoursSleep/10.
    hoursStudyNorm = hoursStudy/5.
    
    #Create 2-d versions of input for plotting
    a, b  = np.meshgrid(hoursSleepNorm, hoursStudyNorm)
    
    #Join into a single input matrix:
    allInputs = np.zeros((a.size, 2))
    allInputs[:, 0] = a.ravel()
    allInputs[:, 1] = b.ravel()
    
    return allInputs, hoursSleep, hoursStudy
    
if __name__ == '__main__':
    main()     
    

