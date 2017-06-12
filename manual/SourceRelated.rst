Additional sources, errors, and sphinx
===============================================

add additional content
----------------------
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
sphinx-quickstart - sphinx-quickstart [options] [projectdir]

sphinx-apidoc -	sphinx-apidoc [options] -o outputdir packagedir [pathnames]
	
make html

make clean

to use as a template for python package (https://pythonhosted.org/an_example_pypi_project/sphinx.html)

Creating source

1. build source codes in modules with __init__.py for each folder
2. use sphinx-apidoc to autogenerate source codes to rst files (sphinx-apidoc -o . ./[source])
