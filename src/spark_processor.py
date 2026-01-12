from pyspark.sql import SparkSession
from src.cobol_parser import COBOLParser
import os
from typing import List

class COBOLSparkProcessor:
    def __init__(self):
        # Initializing Spark for distributed processing
        self.spark = SparkSession.builder \
            .appName("IBM-Modernization-Scaler") \
            .master("local[*]") \
            .getOrCreate()
        self.parser = COBOLParser()

    def process_batch(self, input_folder: str):
        # 1. Get list of files
        files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.cbl')]
        
        # 2. Parallelize across the cluster (RDD)
        file_rdd = self.spark.sparkContext.parallelize(files)

        # 3. Distributed Map operation
        def analyze(path):
            with open(path, 'r') as f:
                content = f.read()
            # Note: Import inside function for Spark serialization
            from src.cobol_parser import COBOLParser
            p = COBOLParser()
            res = p.parse(content)
            return (res.name, res.complexity_score)

        results = file_rdd.map(analyze).collect()
        
        print(f"✓ PySpark: Distributed processing complete for {len(results)} files.")
        return results

if __name__ == "__main__":
    processor = COBOLSparkProcessor()
    processor.process_batch("data/sample_cobol")