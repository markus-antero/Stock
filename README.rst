ARCGIS to SQL project
=====================
The existing scope of this project is to solve problems for: 

- Acquiring and redefining static and updating data.
- Utilizing python compatible analytics platform
- Authentication and access to SQL and ARCGIS 
- Importing and exporting data from the ARCGIS platform. 
- Visualization 

The relations are visualized in graph:

.. image:: images/domain.jpg

The solution is divided to scripts and additional source files divided to three modules:

- ./data/complex (Math module) see complex.ipynb
- ./data/finance (Data objects) see finance- and finance_main.ipymb
- ./data/geographic (Map) see geographic.ipymb


Python SQL to ARCGIS and Orange Canvas development
--------------------------------------------------

this project tests Python as a mediator technology between SQL data-store and an existing front-end UI called ARCGIS. 
As an UI platform, ARCGIS ( https://developers.arcgis.com/ ) is developer-friendly.

To discover the links between source and documentation, database and thin-client UI, and programming practices and available libraries.
The development platform used is Python 3.5.
Task specific packages include:

- geoalchemy2 
- geopandas   
- pandasql   
- sqlalchemy  

Python to UI:

- html5lib				
- esri arcgis

Python to analytics:

- Orange.canvas



Analytics
---------

AS a method for native Python based development Orange Canvas is used as the analytics platform for this project.
The Orange Canvas is a GUI tool embedded with it's own Python based libraries.
A session in the Orange Canvas is visualized in:

.. image:: images/orangeCanvas.jpg

As an analytics tool, the platform is usable as a visual staging area database.
It can also be used to plot information or to produce automated reports for documentation.

.. image:: images/goverment_debt_vs_gdp.png

S&P 500
-------
The map produced as the result is available at:

- https://nedlaw.maps.arcgis.com/apps/Embed/index.html?webmap=21dee994a8f64f2785fbcfeae01ad99a&extent=-180,-49.1324,180,82.6354&home=true&zoom=true&scale=true&search=true&searchextent=true&basemap_gallery=true&disable_scroll=true&theme=light

.. image:: images/Map.jpg

The map features countries and companies as separate features. 

Linked database design and queries
----------------------------------
The information used is collected through different REST services. Each service type is linked with table (table = service call).

- SandP500Index and CompanyStatistics tables share the [Symbol] as ID.
- SandP500_index_data tables contains the running record of company performance. 
- SandP500history table is the running benchmark
- GeographicNE and cities tables contain the geographic information needed to link location to company. 

.. image:: images/database_q2.jpg

SQL 

  SELECT [Date] ,[Volume] ,[Adj Close] ,[100ma] ,stati.[symbol],[Latitude] ,[Longitude], s.City
  
  FROM [finance].[dbo].[SandP500_index_data] as stati INNER JOIN 
       (SELECT top 10  [symbol], [Latitude] ,[Longitude], cities.City
        FROM [finance].[dbo].[SandP500Index] as comp left join [finance].[dbo].[cities] 
            on cities.City = comp.city and cities.iso3 = comp.iso3 
            inner join [finance].[dbo].[GeographicNE] as country on cities.iso3 = country.iso_a3
        where cities.iso3 is not null
        order by comp.symbol) 
  s on s.symbol = stati.symbol
  
  where DATEDIFF(day,[Date],getdate()) between 0 and 170 
  
  order by stati.symbol, [Date]

Query using SQL alchemy - parameter name notation - :gigs 
 
  SELECT c_index.[symbol], [security],[SEC], [GICS_Sector], [GICS_subIndustry],[CIK],[marketCapital]
                          ,[bookValue], [ebitda], [dividentShare], [DividentYield], [earningShare], [BookPrice]
                          ,[SalesPrice], [earningsGrowth], [earningsRatio]
                          ,substring(address, CHARINDEX(', ', address)+1, len(address)-(CHARINDEX(', ', address)-1)) as US_state
  FROM [finance].[dbo].[SandP500Index] as c_index
                inner join [finance].[dbo].[companyStatistics] as stat on c_index.symbol = stat.symbol
  where [GICS_Sector] like :gigs

Opinions about Python
=====================


As development platform Python has mixed identity - it can be used to: 

- supplement command prompt 
- scripting
- larger programming.
 
It is designed as modular tool with programmable objects at core.
E.g. In this project, the main access is done with using scripts, but the core is done using the objects. 

Additional sources:
-------------------

- https://github.com/markus-antero/Stock/blob/master/manual/8_METRICS.rst
- https://github.com/markus-antero/Stock/blob/master/manual/SourceRelated.rst
- https://github.com/markus-antero/Stock/blob/master/manual/financial_abbreviations.rst
- https://github.com/markus-antero/Stock/blob/master/manual/indicators.rst
- https://github.com/markus-antero/Stock/blob/master/manual/orange_canvas.rst
- https://github.com/markus-antero/Stock/blob/master/manual/pca._doc.rst
