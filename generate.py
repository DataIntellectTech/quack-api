import pyarrow as pa
import pyarrow.dataset as ds
import duckdb
import os
from pyarrow import csv

home=os.environ['HOME'] #setting environment variable

quote_schema = pa.schema([                       # defining schema for quote dataset
    pa.field('time', pa.timestamp('ns')),        # assigning time column timestamp type
    pa.field('src', pa.string()),                # assigning src column string type
    pa.field('sym', pa.string()),                # assigning sym column string type
    pa.field('bid', pa.float64()),               # assigning bid column float type
    pa.field('bsize', pa.int64()),               # assigning bsize column int type
    pa.field('ask', pa.float64()),               # assigning ask column float type
    pa.field('asize', pa.int64())])              # assigning asize column int type

trade_schema = pa.schema([                       # defining schema for trade dataset
    pa.field('sym', pa.string()),                # assigning sym column string type
    pa.field('time', pa.timestamp('ns')),        # assigning time column timestamp type 
    pa.field('src', pa.string()),                # assigning src column string type
    pa.field('price', pa.float64()),             # assigning price column float type
    pa.field('size', pa.int64())])               # assigning size column int typoe

trade = ds.dataset(home+"/quack-api/trade.csv", format = "csv", schema=trade_schema) #assigning trade to the arrow dataset generated from the trade csv
quote = ds.dataset(home+"/quack-api/quote.csv", format = "csv", schema=quote_schema) #assigning quote to the arrow dataset generated from the quote csv

ds.write_dataset(trade, home+"/quack-api/arrowdb/trade", format="arrow", schema=trade_schema) # writing the trade dataset to disk, saving it in quack-api/arrowdb/trade/ directory 
ds.write_dataset(quote, home+"/quack-api/arrowdb/quote", format="arrow", schema=quote_schema) # writing the quote dataset to disk, saving it in quack-api/arrowdb/quote/ directory 

