Python SQL to ARCGIS development
================================

In this project I wanted to build, learn, and test Python as a mediator technology between SQL data-store and an existing front-end UI called ARCGIS. 
As an UI platform I liked ARCGIS ( https://developers.arcgis.com/ ) due to its developer friendly appearance.

To discover the links between source and documentation, database and thin-client UI, and programming practices and available libraries.
The development platform used is Python 3.5.
Task specific packages include:

SQL to Python

- geoalchemy2 
- geopandas   
- pandasql   
- sqlalchemy  

Python to UI:

- html5lib				
- esri arcgis			

problems to solve
-----------------
- Acquiring and redefining static and updating data.
- Authentication and access to SQL and ARCGIS 
- Importing and exporting data from the ARCGIS platform. 
- Visualization 

Python as a Puzzle
------------------
As development platform Python has mixed identity - it can be used to: 

- supplement command prompt 
- scripting
- larger programming.
 
It is designed as modular tool with programmable objects at core.
E.g. In this project, the main access is done with using scripts, but the core is done using the objects. 


add additional content
------------------
.. toctree::
   :maxdepth: 2

   ./manual/sphinx

error handling
--------------
try:
    # catch exc if index out of range
    print 'Looks like a bad index'

except:
    # catch something we didn't anticipate
    print 'Exception type:', sys.exc_info()[0]
    print 'Exception value:', sys.exc_info()[1]
    traceback.print_exc()    
finally:
    print ('executes always')
    
sphinx 
------
(http://www.sphinx-doc.org/en/stable/invocation.html)
sphinx-quickstart
	sphinx-quickstart [options] [projectdir]

sphinx-apidoc
	sphinx-apidoc [options] -o outputdir packagedir [pathnames]
	
make html
make clean

https://www.youtube.com/watch?v=qrcj7sVuvUA	

to use as a template for python package

	https://pythonhosted.org/an_example_pypi_project/sphinx.html

Creating source
---------------
1. build source codes in modules with __init__.py for each folder
2. use sphinx-apidoc to autogenerate source codes to rst files (sphinx-apidoc -o . ./[source])
