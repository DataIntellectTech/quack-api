import pyarrow as pa
import pyarrow.dataset as ds
import duckdb
import os
import sys

home=os.environ['HOME'] #setting environment variable

quote_schema = pa.schema([                       # defining schema for quote dataset, this should include all the columns from the csv that you are generating from
    pa.field('time', pa.timestamp('ns')),        # assigning column types 
    pa.field('src', pa.string()),
    pa.field('sym', pa.string()),
    pa.field('bid', pa.float64()),
    pa.field('bsize', pa.int64()),
    pa.field('ask', pa.float64()),
    pa.field('asize', pa.int64())])

trade_schema = pa.schema([                       # defining schema for trade dataset
    pa.field('sym', pa.string()),                # assigning column types
    pa.field('time', pa.timestamp('ns')),
    pa.field('src', pa.string()),
    pa.field('price', pa.float64()),
    pa.field('size', pa.int64())])

#If using other data that isn't trade or quote data, the schema will look different, and should include the column of that data, with their desired types

trade = ds.dataset(home+"/quack-api/"+str(sys.argv[1])+"/trade.csv", format = "csv", schema=trade_schema) #assigning tables to arrow datasets generated from the csvs, using the schemas
quote = ds.dataset(home+"/quack-api/"+str(sys.argv[1])+"/quote.csv", format = "csv", schema=quote_schema)

ds.write_dataset(trade, home+"/quack-api/arrowdb/trade/"+str(sys.argv[1]), format="arrow", schema=trade_schema) # writing the datasets to appropriate directories 
ds.write_dataset(quote, home+"/quack-api/arrowdb/quote/"+str(sys.argv[1]), format="arrow", schema=quote_schema)
