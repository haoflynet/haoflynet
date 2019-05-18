spark和hadoop的区别这里讲得很清楚了

<http://dblab.xmu.edu.cn/blog/1710-2/>





pyspark的使用，读取csv文件举例

<https://stackoverflow.com/questions/28782940/load-csv-file-with-spark>

```python
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

df = spark.read.csv("/home/stp/test1.csv",header=True,sep="|");

print(df.collect())
```

