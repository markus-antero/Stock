sphinx
======
http://www.sphinx-doc.org/en/stable/invocation.html

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
2. use sphinx-apidoc to autogenerate source codes to rst files (sphinx-apidoc -o . ./finance)

Source Codes
------------
1. Make.bat

@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build
set SPHINXPROJ=Finance

if "%1" == "" goto help

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%

:end
popd

