import pyarrow as pa
import pyarrow.dataset as ds
import duckdb
import os
import argparse

home=os.environ['HOME'] #setting environment variable

parser=argparse.ArgumentParser(description='Generate csvs to arrow files', epilog='Date flag takes date in the form yyyy-mm-dd')  #
parser.add_argument('-d','--date')
args = parser.parse_args()

quote_schema = pa.schema([                       # defining schema for quote dataset, this should include all the columns from the csv that you are generating from
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
    pa.field('size', pa.int64())])               # assigning size column int type

#If using other data that isn't trade or quote data, the schema will look different, and should include the column of that data, with their desired types

trade = ds.dataset(home+"/quack-api/"+str(args.date)+"/trade.csv", format = "csv", schema=trade_schema) #assigning trade to the arrow dataset generated from the trade csv, using the trade schema assigned above
quote = ds.dataset(home+"/quack-api/"+str(args.date)+"/quote.csv", format = "csv", schema=quote_schema) #assigning quote to the arrow dataset generated from the quote csv, using the quote schema assigned above

ds.write_dataset(trade, home+"/quack-api/arrowdb/trade/"+str(args.date), format="arrow", schema=trade_schema) # writing the trade dataset to disk, saving it in quack-api/arrowdb/2020-01-02/trade/ directory 
ds.write_dataset(quote, home+"/quack-api/arrowdb/quote/"+str(args.date), format="arrow", schema=quote_schema) # writing the quote dataset to disk, saving it in quack-api/arrowdb/2020-01-02/quote/ directory 

