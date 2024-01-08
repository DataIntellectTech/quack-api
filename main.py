import duckdb
from fastapi import FastAPI, Query
import pyarrow as pa
import pyarrow.dataset as ds
from pyarrow import csv
from fastapi.responses import PlainTextResponse
from tabulate import tabulate
from typing import List, Annotated

part=ds.partitioning(pa.schema([("date", pa.date64())]))

trade = ds.dataset("quack-api/arrowdb/trade", format = "arrow", partitioning=part)
quote = ds.dataset("quack-api/arrowdb/quote", format = "arrow", partitioning=part) 


app = FastAPI()
app.title="DuckDB"
con = duckdb.connect()

@app.get("/query", response_class=PlainTextResponse)
def exec_query(query: str):
    result = con.execute(query)
    rows=result.fetchall()
    con.execute("CREATE OR REPLACE TEMP TABLE tab AS " + query)
    columns=con.execute("SELECT DISTINCT(name) FROM pragma_table_info('tab')").fetchall()
    columns= [i[0] for i in columns]
    table=tabulate(rows, headers=columns, tablefmt="simple")
    return table

@app.get("/parameterised", response_class=PlainTextResponse)
def parameterisedquery(body: str,table: str, symbol: Annotated[str | None, Query(alias="symbol",title="Symbol",description="Symbol(s) to be searched for, in the form ('sym','sym'...)")]=None, date: Annotated[str | None, Query(alias="Date",title="Date",description="Date(s) to be searched for, in the form ('yyyy-mm-dd','yyyy-mm-dd'...)")]=None, group: str = None):
    conditions = []

    if symbol is not None:
        conditions.append("sym in " + "("+symbol+")")

    if date is not None:
        conditions.append("date in " + date)

    where_clause = "WHERE " + (" AND ".join(conditions)) if conditions else ""

    groups=""
    if group is not None:
        groups = "GROUP BY " + group   

    query = f"SELECT {body} FROM {table} {where_clause} {groups}"
    result = con.execute(query)
    rows = result.fetchall()
    con.execute("CREATE OR REPLACE TEMP TABLE tab AS " + query)
    columns=con.execute("SELECT DISTINCT(name) FROM pragma_table_info('tab')").fetchall()
    columns= [i[0] for i in columns]
    table=tabulate(rows, headers=columns, tablefmt="fancy_grid")
    return table
