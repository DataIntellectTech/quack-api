import pyarrow as pa
import pyarrow.dataset as ds
import duckdb
import os
from pyarrow import csv
from datetime import date

home=os.environ['HOME']
quote_schema = pa.schema([
    pa.field('time', pa.timestamp('ns')),
    pa.field('src', pa.string()),
    pa.field('sym', pa.string()),
    pa.field('bid', pa.float64()),
    pa.field('bsize', pa.int64()),
    pa.field('ask', pa.float64()),
    pa.field('asize', pa.int64())])

trade_schema = pa.schema([
    pa.field('sym', pa.string()),
    pa.field('time', pa.timestamp('ns')),
    pa.field('src', pa.string()),
    pa.field('price', pa.float64()),
    pa.field('size', pa.int64())])

today=date.today()
trade = ds.dataset(home+"/quack-api/trade.csv", format = "csv", schema=trade_schema)
quote = ds.dataset(home+"/quack-api/quote.csv", format = "csv", schema=quote_schema)

ds.write_dataset(trade, home+"/quack-api/arrowdb/trade", format="arrow", schema=trade_schema)
ds.write_dataset(quote, home+"/quack-api/arrowdb/quote", format="arrow", schema=quote_schema)

