# quack-api
A simple DuckDB and FastAPI app

[Introduction](#introduction)

[Installation](#installation)

[Usage](#usage)

## Introduction ##
DuckDB is a database management system that is completely embedded within the host process, effectively separating the data from the database. This means that you can use it to query data that is stored within various data formats. DuckDB has a Python API, meaning it can be embedded within a Python process.

FastAPI is a web framework for building APIs with Python. With it, you can create APIs that receive HTTP requests for functions and carry them out.

Piecing toghether what we know about DuckDB and FastAPI, it becomes clear that the two can be combined to create a DuckDB FastAPI app, QuackAPI. This repository contains all the code and data required to get a simple barebones version of QuackAPI running. The repo contains 4 files, two python files, generate.py and main.py, and two CSVs, trade and quote. The CSVs are provided for some starter data, although you can replace them with whatever data you will mount to DuckDB. These CSVs replicate a day's worth of trade and quote data, with around 1000000 and 1500000 rows respectively. The generate.py file will convert the CSVs in the repository firstly into datasets and then will write them down as Apache Arrow files. Apache Arrow files are not the only option, https://arrow.apache.org/docs/python/generated/pyarrow.dataset.write_dataset.html#:~:text=formatFileFormat%20or,keyword%20is%20required, this link outlines the options for the ds.write_dataset function, although bear in mind, out of these options, DuckDB can only mount Arrow or Parquet files.

The main.py provides the configuration for FastAPI. We start by setting the partitioning schema (note this is not necessary), and then read the trade and quote dataset in the desired format (we've used Arrow?) with the partitioning schema. We have then defined two functions. The first function allows the user to enter a raw DuckDB query, and it will return the result to the console. The second function parameterises the query and provides boxes for each of the following parameters: body of the select (if empty, *), table name, symbol(s), date(s), and column(s) to be grouped by.  With table name and body being required and the rest are optional.

## Installation ##
To make use of QuackAPI, the following need installed in your virtual python environment:

```python
pip install fastapi
pip install uvicorn
pip install typing
pip install tabulate
```
Once you have intalled the above, and have main.py defined then run the following line within your virtual environment:
```python
uvicorn --reload main:app
```
You can specify the host by -- host and the IP address, and the port will be assigned at 8000, if you want to change this add --port and insert chosen port number. The --reload flag allows the system to track any changes to the main.py script while it is running. The FastAPI website has an entire tutorial on how to get the API running, and how to develop it, https://fastapi.tiangolo.com/tutorial/.

## Usage ##
Provided within this repository is fake csv data that can be used. Within the generate.py script point to that data and then make an Apache Arrow file from it. However, if you want to extend this, and automate it, a suggestion would be to use crontab, and set up the crontab to at some point (probably end of day) run the generate.py script on your data to save down that day's data in Apache Arrow format. Anything that provides functionality to run scripts or carry out functions daily can be used, crontab was what we had available. 

This is the first query in use, enter a simple query into the description, and it'll be returned to the console below, as the image shows:

![image](https://github.com/DataIntellectTech/quack-api/assets/131150806/66f0e63a-5a4d-4a78-8228-6d177f366081)

The second query looks as follows:
![image](https://github.com/DataIntellectTech/quack-api/assets/131150806/cd006a7d-b7ce-48f1-a510-8a36cbfd6ec8)

which translates to "SELECT AVG(price) FROM trade WHERE sym in ('AAPL','GOOG')"



