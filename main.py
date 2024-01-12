import duckdb
from fastapi import FastAPI, Query
import pyarrow.dataset as ds
import os
from fastapi.responses import PlainTextResponse
from tabulate import tabulate
from typing import Annotated

home=os.environ['HOME']                                                                         # setting environment variable

part = ds.partitioning(pa.schema([("date", pa.date64())]))                                      # defining the partition schema to partition on date

trade = ds.dataset(home+"/quack-api/arrowdb/trade", format = "arrow", partitioning=part)        # assigning trade to the arrow trade dataset 
quote = ds.dataset(home+"/quack-api/arrowdb/quote", format = "arrow", partitioning=part)        # assigning trade to the arrow quote dataset


app = FastAPI()                                                                                 # 
app.title="DuckDB"                                                                              # assigning title of app to be "DuckDB"
con = duckdb.connect()                                                                          # connecting to duckdb and setting con to be the variable

@app.get("/query", response_class=PlainTextResponse)                                            # defining endpoint for the exec_query function
def exec_query(query: str):                                                                     # defining the exec_query function
    result = con.execute(query)                                                                 # executing the query
    rows=result.fetchall()                                                                      # fetching the query the result and assign to variable rows
    con.execute("CREATE OR REPLACE TEMP TABLE tab AS " + query)                                 # creating temporary table of the data
    columns=con.execute("SELECT DISTINCT(name) FROM pragma_table_info('tab')").fetchall()       # fetching the column names from the temporary table
    columns= [i[0] for i in columns]                                                            # iterate through the column names
    table=tabulate(rows, headers=columns, tablefmt="simple")                                    # placing the data and the column names into a table
    return table                                                                                # return the table

@app.get("/parameterised", response_class=PlainTextResponse)                                    # defining endpoint for the parameterisedquery function
def parameterisedquery(body: str,table: str,                                                    # defining the parameterisedquery function
        symbol: Annotated[str | None, Query(alias="symbol",title="Symbol",description="Symbol(s) to be searched for, in the form ('sym','sym'...)")]=None, # adds text to the app to instruct user of the format required for entering symbols
        date: Annotated[str | None, Query(alias="Date",title="Date",description="Date(s) to be searched for, in the form ('yyyy-mm-dd','yyyy-mm-dd'...)")]=None,  # adds text to the app to instruct user of the format required for entering dates
        group: str = None):
    conditions = []                                                                             # assigning conditions as an empty list

    if symbol is not None:                                                                          
        conditions.append("sym in " + symbol)                                                   # if symbol is a parameter, append "sym in symbol" to conditions

    if date is not None:
        conditions.append("date in " + date)                                                    # if symbol is a parameter, append "date in date" to conditions

    where_clause = "WHERE " + (" AND ".join(conditions)) if conditions else ""                  # build a WHERE clause if conditions is non-empty

    groups=""
    if group is not None:
        groups = "GROUP BY " + group                                                            # if group ius a parameter, build a group by clause

    query = f"SELECT {body} FROM {table} {where_clause} {groups}"                               # create the query with all relevant parts
    result = con.execute(query)                                                                 # execute the query
    rows = result.fetchall()                                                                    # fetch the result and assign to variable rows
    con.execute("CREATE OR REPLACE TEMP TABLE tab AS " + query)                                 # create temporary table of the data
    columns=con.execute("SELECT DISTINCT(name) FROM pragma_table_info('tab')").fetchall()       # fetching the column names from the temporary table
    columns= [i[0] for i in columns]                                                            # iterate through the column names
    table=tabulate(rows, headers=columns, tablefmt="fancy_grid")                                # placing the data and the column names into a table
    return table                                                                                # return the table
