
PCA and PCAD
============

Standardize the data.
Obtain the Eigenvectors and Eigenvalues from the covariance matrix or correlation matrix, or perform Singular Vector Decomposition.
Sort eigenvalues in descending order and choose the k
eigenvectors that correspond to the k largest eigenvalues where k is the number of dimensions of the new feature subspace (k≤d)/.
Construct the projection matrix W from the selected k eigenvectors.
Transform the original dataset X via W to obtain a k-dimensional feature subspace Y.


    Σμ = λμ 
        Σ - n x n matrix
        μ - n x 1 vector
        λ – scalar
        
    Σμ =λμ
    Σμ −λμ = 0
    (Σ−λΙ)μ = 0
    det (Σ−λΙ) = 0

The classic approach to PCA is to perform the eigendecomposition on the covariance matrix Σ, which is a d×d
matrix where each element represents the covariance between two features. The covariance between two features is calculated as follows:

    σjk=1n−1∑Ni=1(xij−x¯j)(xik−x¯k).

Method
------
1. newton_krylov
2. generate test case using Anomany detection dataset,
3. Calculate notebook
4. produce and draw eigenvectors and corresponding samples 
5. Understand standard deviation, expand to normal distribution to differential 
6. After plotting sample data / use real data / 
    i. Convert dataframe object to numpy array - http://stackoverflow.com/questions/13187778/convert-pandas-dataframe-to-numpy-array-preserving-index
        run 

Links
-----

PCA

i. https://docs.scipy.org/doc/scipy/reference/optimize.nonlin.html
i. http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
i. https://plot.ly/ipython-notebooks/principal-component-analysis/
i. http://occamstypewriter.org/boboh/2012/01/17/pca_and_pcoa_explained/
i. https://github.com/jakevdp/sklearn_pycon2015/blob/master/notebooks/04.1-Dimensionality-PCA.ipynb

Solver  

i. https://github.com/rasbt
i. http://www.kdnuggets.com/2015/11/seven-steps-machine-learning-python.html/2
i. https://www.coursera.org/learn/machine-learning
i. http://www.holehouse.org/mlclass/
i. http://www.cs.cmu.edu/~ninamf/courses/601sp15/lectures.shtml
i. http://deeplearning.net/software/theano/

    
