Additional sources, Content, errors, and sphinx
===============================================

Global indicators
-----------------
UN - sustainable development goals - top 5 - the noble goals

1. No poverty 
2. zero hunger 
3. good health and well-being 
4. quality education
5. gender equality

- http://www.un.org/sustainabledevelopment/sustainable-development-goals/

Food production
--------------- 
definition for sustainable food production: 

- http://www.sustainabletable.org/254/local-regional-food-systems

Energy 
------
1. energies in Europe (and globally) - http://ec.europa.eu/eurostat/statistics-explained/index.php/Energy_from_renewable_sources
2. Global energy consumption ( http://www.iea.org/ ) - https://www.iea.org/publications/freepublications/publication/KeyWorld2016.pdf

Key issues:

- World energy consumption continues to rise
- Steady increase in overall consumption (8)

World population 
----------------
rapid increase in regional density and volume

Estimated to reach 9.5 billion by the year 2050 
(This means that within my (projected) lifetime, the world population is going to double in size from 4.78 billion to 9.5)  

Global population is driven regionally 

- http://worldpopulationhistory.org/map/1953/mercator/1/0/25/ Environment 
-----------
- http://www.worldometers.info/
- http://www.poodwaddle.com/worldclock/env/
- http://www.globalwaterforum.org/resources/data/

Summary
-------
Deficit of existing resources will continue to grow annually (fuelled by population growth in specific regions)

- https://www.foe.co.uk/sites/default/files/downloads/overconsumption.pdf

the UN is disenfranchised from reality
Local bubbles - misalignment in opinions.

add additional content
----------------------
.. toctree::
   :maxdepth: 2

   ./manual/sphinx

Source Handling
===============
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
