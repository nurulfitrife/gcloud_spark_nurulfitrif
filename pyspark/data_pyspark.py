from pyspark.sql import SparkSession
import datetime
import os
from airflow import models

# Initialize a Spark session
spark = SparkSession.builder.appName("WordCount").getOrCreate()

BUCKET = 'data-spark-bucket'
spark.conf.set('temporaryGcsBucket', BUCKET)

# Input and output paths
input_path = "gs://pub/shakespeare/rose.txt"  
output_file = os.path.join(
                models.Variable.get('gcs_bucket'), 'wordcount',
                datetime.datetime.now().strftime('%Y%m%d-%H%M%S')) + os.sep

# Read the input text file
text_file = spark.read.text(input_path)

# Split the lines into words and count the occurrences of each word
word_counts = text_file.selectExpr("explode(split(value, ' ')) as word").groupBy("word").count()

# Save the word counts to the specified output path
word_counts.write.mode("overwrite").csv(output_file)

# Stop the Spark session
# spark.stop()
