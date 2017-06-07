'''
Created on 19.4.2017

@author: Markus.Walden
'''

from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# use seaborn plotting style defaults
import seaborn as sns; sns.set()

# premade pca SKLEARN
from sklearn.decomposition import PCA, KernelPCA
from sklearn.datasets import make_circles, load_digits
    
def main ():
    linearPCA()
    nonLinearPCA()
    
def nonLinearPCA():
    
    X, y = generateData(method = 'nonLinear')
    
    kpca = KernelPCA(kernel="rbf", fit_inverse_transform=True, gamma=10)
    X_kpca = kpca.fit_transform(X)
    X_back = kpca.inverse_transform(X_kpca)
    pca = PCA()                             # pca = PCA(2) project from 64 to 2 dimensions
    X_pca = pca.fit_transform(X)
    
    X1, X2 = np.meshgrid(np.linspace(-1.5, 1.5, 50), np.linspace(-1.5, 1.5, 50))
    X_grid = np.array([np.ravel(X1), np.ravel(X2)]).T
    # projection on the first principal component (in the phi space)
    Z_grid = kpca.transform(X_grid)[:, 0].reshape(X1.shape)
    plt.contour(X1, X2, Z_grid, colors='grey', linewidths=1, origin='lower')
    
    reds = y == 0
    blues = y == 1
    
    visualizePCA(X1, X2, Z_grid, X_pca, reds, blues, X_kpca, X_back)
    
def linearPCA():    
    '''
    generate data
    '''    
    x = generateData()
    
    pca = PCA(n_components=2)
    pca.fit(x)
    print(pca.explained_variance_)
    print(pca.components_)
    
    plt.plot(x[:, 0], x[:, 1], 'o', alpha=0.5)
    for length, vector in zip(pca.explained_variance_, pca.components_):
        v = vector * 3 * np.sqrt(length)
        plt.plot([0, v[0]], [0, v[1]], '-k', lw=3)
    plt.axis('equal');
    plt.show()
    
    clf = PCA(0.95) # keep 95% of variance
    X_trans = clf.fit_transform(x)
    print(x.shape)
    print(X_trans.shape)
    
    X_new = clf.inverse_transform(X_trans)
    plt.plot(x[:, 0], x[:, 1], 'o', alpha=0.2)
    plt.plot(X_new[:, 0], X_new[:, 1], 'ob', alpha=0.8)
    plt.axis('equal')
    plt.show()

def generateData (rendomSeed = 1, method = 'linear'):
    '''
    '''    
    if method == 'linear':
        np.random.seed(1)
        X = np.dot(np.random.random(size=(2, 2)), np.random.normal(size=(2, 200))).T
        plt.plot(X[:, 0], X[:, 1], 'o')
        plt.axis('equal');
        plt.show()
        return X

    elif method == 'nonLinear':
        X, y = make_circles(n_samples=400, factor=.3, noise=.05)

        plt.figure()
        plt.subplot(2, 2, 1, aspect='equal')
        plt.title("Original space")
        reds = y == 0
        blues = y == 1
        
        plt.plot(X[reds, 0], X[reds, 1], "ro")
        plt.plot(X[blues, 0], X[blues, 1], "bo")
        plt.xlabel("$x_1$")
        plt.ylabel("$x_2$")
        
        return X,y 

def visualizePCA(X1, X2, Z_grid, X_pca, reds, blues, X_kpca, X_back):
    plt.contour(X1, X2, Z_grid, colors='grey', linewidths=1, origin='lower')

    plt.subplot(2, 2, 2, aspect='equal')
    plt.plot(X_pca[reds, 0], X_pca[reds, 1], "ro")
    plt.plot(X_pca[blues, 0], X_pca[blues, 1], "bo")
    plt.title("Projection by PCA")
    plt.xlabel("1st principal component")
    plt.ylabel("2nd component")
    
    plt.subplot(2, 2, 3, aspect='equal')
    plt.plot(X_kpca[reds, 0], X_kpca[reds, 1], "ro")
    plt.plot(X_kpca[blues, 0], X_kpca[blues, 1], "bo")
    plt.title("Projection by KPCA")
    plt.xlabel("1st principal component in space induced by $\phi$")
    plt.ylabel("2nd component")
    
    plt.subplot(2, 2, 4, aspect='equal')
    plt.plot(X_back[reds, 0], X_back[reds, 1], "ro")
    plt.plot(X_back[blues, 0], X_back[blues, 1], "bo")
    plt.title("Original space after inverse transform")
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")
    
    plt.subplots_adjust(0.02, 0.10, 0.98, 0.94, 0.04, 0.35)
    
    plt.show()
    
if __name__ == '__main__':
    main() 