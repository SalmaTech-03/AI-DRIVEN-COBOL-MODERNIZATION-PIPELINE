from pyspark.sql import SparkSession
from src.cobol_parser import COBOLParser
import os

def run_distributed_analysis(input_folder="data/sample_cobol"):
    """
    Demonstrates how to scale this POC to millions of lines of code.
    IBM Advantage: Distributed Processing with PySpark.
    """
    # 1. Initialize Spark (Local Mode for Demo)
    spark = SparkSession.builder \
        .appName("IBM-Modernization-Scaler") \
        .getOrCreate()

    # 2. Load all COBOL files as a Spark RDD
    # In production, this would be an S3 bucket or HDFS path
    file_list = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.cbl')]
    
    # Parallelize the file list across the 'cluster'
    dist_files = spark.sparkContext.parallelize(file_list)

    def process_file(path):
        parser = COBOLParser()
        with open(path, 'r') as f:
            content = f.read()
        analysis = parser.parse(content)
        return (analysis.name, analysis.complexity_score)

    # 3. Distributed Mapping (The 'Magic' step)
    results = dist_files.map(process_file).collect()

    print(f"\n[SPARK] Successfully processed {len(results)} files in parallel.")
    for name, score in results:
        print(f"    >> {name}: Scaled Analysis Score = {score}")

    spark.stop()