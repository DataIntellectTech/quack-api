# quack-api
A simple DuckDB and FastAPI app

[Introduction](#introduction)

[Installation](#installation)

[Usage](#usage)

## Introduction ##
The first thing you are probably asking is what is QuackAPI? It is a simple application you can use to take any set of Arrow or Parquet files (we're expecting trade and quote finance files) and will provide a simple yet fast database for them, that can be queried from within the browser. In order to achieve this we make use of two softwares, DuckDB and FastAPI.  

DuckDB is a database management system that is completely embedded within the host process, effectively separating the data from the database. This means that you can use it to query data that is stored within various data formats. DuckDB has a Python API, therefore it can be embedded within a Python process.

FastAPI is a web framework for building APIs with Python. With it, you can create APIs that receive HTTP requests for functions and carry them out.

This repository contains all the code and data required to get a simple barebones version of QuackAPI running. The repo contains two Python files, generate.py, and main.py, four arrow files, which are within a partitioned structure, partitioned on a date, with each date having a trade and quote file, and 6 CSVs, trade and quote, 2 for each date. The arrow files are provided so that the main.py script will work straight out of the box, and the CSVs are provided to first show where the arrow files have come from and then to allow for use of the generate.py script if adding another date is required. Each day of data, either CSVs or arrow files contains 1000000 and 1500000 rows, for trade and quote data respectively.  The generate.py file will convert the CSVs in the repository firstly into datasets and then will write them down as Apache Arrow files. Apache Arrow files are not the only option, https://arrow.apache.org/docs/python/generated/pyarrow.dataset.write_dataset.html#:~:text=formatFileFormat%20or,keyword%20is%20required, this link outlines the options for the ds.write_dataset function, although bear in mind, out of these options, DuckDB can only mount Arrow or Parquet files. 

The main.py provides the configuration for FastAPI. We start by setting the partitioning schema (note this is not necessary), and then read the trade and quote dataset in the desired format (we've used Arrow?) with the partitioning schema. If the data you have is set up like the example and you have a partitioned structure to your files, adding the partitoning schema will ensure that the partition is read in when querying, and therefore allows the partition to be queried directly. If the data is not partioned, then no partitioned schema is required. We have then defined two functions. The first function allows the user to enter a raw DuckDB query, and it will return the result to the console. The second function parameterises the query and provides boxes for each of the following parameters: the body of the select (if empty, *), table name, symbol(s), date(s), and column(s) to be grouped by.  The table name and body are required and the rest are optional.

## Installation ##
To make use of QuackAPI, the following need to be installed in your virtual Python environment:

```python
pip install fastapi
pip install uvicorn
pip install typing
pip install tabulate
```
Once you have installed the above, and have main.py defined then run the following line within your virtual environment:
```python
uvicorn --reload main:app
```
You can specify the host by -- host and the IP address, and the port will be assigned at 8000, if you want to change this add --port and insert chosen port number. The --reload flag allows the system to track any changes to the main.py script while it is running. The FastAPI website has an entire tutorial on how to get the API running, and how to develop it, https://fastapi.tiangolo.com/tutorial/.

## Usage ##
Provided within this repository is fake CSV data that can be used. To make use of the generate.py file run the following command within a Python virtual environement:
```python
python generate.py date
```
The date after generate.py allows you to specify what CSV you want to be generated into an arrow file, and is necessary for the script to run. A date is required due to the structure of the direcotry containing the trade and quote CSVs.

However, if you want to extend this, and automate it, a suggestion would be to use crontab, and set up the crontab to at some time daily (probably end of day) to run the generate.py script on your data to save down that day's data in Apache Arrow format. Anything that provides functionality to run scripts or carry out functions daily can be used, crontab was simply what we had available. 

This is the first query in use, enter a simple query into the description, and it'll be returned to the console below, as the image shows:

![image](https://github.com/DataIntellectTech/quack-api/assets/131150806/66f0e63a-5a4d-4a78-8228-6d177f366081)

The second query looks as follows:
![image](https://github.com/DataIntellectTech/quack-api/assets/131150806/cd006a7d-b7ce-48f1-a510-8a36cbfd6ec8)

which translates to "SELECT AVG(price) FROM trade WHERE sym in ('AAPL','GOOG')"



