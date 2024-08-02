from simple_ddl_parser import DDLParser
import pprint

ddl = r"""CREATE EXTERNAL TABLE `database`.`table` (
    column1 string,
    column2 string
)
PARTITIONED BY
(
    column3 integer
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION 's3://somewhere-in-s3/prefix1'
TBLPROPERTIES (
  'parquet.compression'='GZIP'
)"""

result = DDLParser(ddl).run()
pprint.pprint(result)


