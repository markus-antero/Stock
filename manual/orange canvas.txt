Orange Canvas
=============

To run 
------
- python -m Orange.canvas

Blog posts & documentation
--------------------------
Containing recent changes to Orange canvas explaining conflicts with some of the tutorials available

- https://blog.biolab.si/2017/04/07/model-replaces-classify-and-regression/
- https://blog.biolab.si/2017/06/05/nomogram/
- https://blog.biolab.si/tag/gsoc/
- https://blog.biolab.si/2016/03/12/overfitting-and-regularization/
- https://blog.biolab.si/2016/11/30/data-mining-for-political-scientists/
- http://blog.biolab.si/2015/08/14/classifying-instances-with-orange-in-python/
- https://blog.biolab.si/2015/10/16/learners-in-python/ 

Python script widget to access external python libraries 
--------------------------------------------------------
Main python script support for 

- https://docs.orange.biolab.si/3/data-mining-library/#tutorial

For Python Script

- https://docs.orange.biolab.si/3/visual-programming/widgets/data/pythonscript.html

Example 1:

One can, for example, do batch filtering by attributes. We used zoo.tab for the example and we filtered out all the attributes that have more than 5 discrete values. This in our case removed only ‘leg’ attribute, but imagine an example where one would have many such attributes.

	from Orange.data import Domain, Table

	domain = Domain([attr for attr in in_data.domain.attributes
					 if attr.is_continuous or len(attr.values) <= 5],
					in_data.domain.class_vars)
	out_data = Table(domain, in_data)

Example 2:

The second example shows how to round all the values in a few lines of code. This time we used wine.tab and rounded all the values to whole numbers.

	import numpy as np

	out_data = in_data.copy()			#copy, otherwise input data will be overwritten
	np.round(out_data.X, 0, out_data.X)

Example 3:

The third example introduces some gaussian noise to the data. Again we make a copy of the input data, then walk through all the values with a double for loop and add random noise.

	import random
	from Orange.data import Domain, Table

	new_data = in_data.copy()
	for inst in new_data:
	  for f in inst.domain.attributes:
		inst[f] += random.gauss(0, 0.02)
	out_data = new_data

Example 4: 

The final example uses Orange3-Text add-on. Python Script is very useful for custom preprocessing in text mining, extracting new features from strings, or utilizing advanced nltk or gensim functions. Below, we simply tokenized our input data from deerwester.tab by splitting them by whitespace.

	print('Running Preprocessing ...')
	tokens = [doc.split(' ') for doc in in_data.documents]
	print('Tokens:', tokens)
	out_object = in_data
	out_object.store_tokens(tokens)

github
------
- https://github.com/biolab/orange3-example-addon

Network Module
--------------
- http://orange3-network.readthedocs.io/en/latest/widgets/networkfile.html

    1. Graph File. Loads network file and (optionally) constructs a data table from the graph. A dropdown menu provides access to documentation data sets with Browse documentation networks.... The folder icon provides access to local data files. If Build graph data table automatically is checked, the widget will not output an inferred data table (no Items output will be available).
    
	2. Vertices Data File. Information on the network nodes. Reads standard Orange data files. he folder icon provides access to local data files.
    
	3. Information on the constructed network. Reports on the type of graph, number of nodes and edges and the provided vertices data file

Educational 
-----------
- https://blog.biolab.si/tag/gsoc/

Contains:

- K-Means
- Polynomial Regression
- Gradient Descent
- Polynomial Classification	
	
conda environment 
-----------------

The system cannot find the path specified.

(C:\python\New folder) C:\python\New folder\etc\conda\activate.d>set "GDAL_DRIVER_PATH="

- https://conda.io/docs/using/envs.html

C:\python\New folder) C:\Users\Markus.Walden>conda env --help
usage: conda-env-script.py [-h]
                           {attach,create,export,list,remove,upload,update}
                           ...

positional arguments:
  {attach,create,export,list,remove,upload,update}
    attach              Embeds information describing your conda environment
                        into the notebook metadata
    create              Create an environment based on an environment file
    export              Export a given environment
    list                List the Conda environments
    remove              Remove an environment
    upload              Upload an environment to anaconda.org
    update              Update the current environment based on environment
                        file

optional arguments:
  -h, --help            Show this help message and exit.
