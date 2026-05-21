"""SparkSession oluşturma modülü."""
from pyspark.sql import SparkSession
from config import (
    APP_NAME, SPARK_MASTER, SPARK_DRIVER_HOST, SPARK_DRIVER_BIND_ADDRESS,
    SPARK_DRIVER_PORT, SPARK_BLOCKMANAGER_PORT, EXECUTOR_MEMORY, CORES_MAX,
    get_namenode_ip,
)


def create_spark_session() -> SparkSession:
    namenode_ip = get_namenode_ip()
    spark = (
        SparkSession.builder
        .appName(APP_NAME)
        .master(SPARK_MASTER)
        .config("spark.driver.host", SPARK_DRIVER_HOST)
        .config("spark.driver.bindAddress", SPARK_DRIVER_BIND_ADDRESS)
        .config("spark.driver.port", SPARK_DRIVER_PORT)
        .config("spark.blockManager.port", SPARK_BLOCKMANAGER_PORT)
        .config("spark.hadoop.fs.defaultFS", f"hdfs://{namenode_ip}:9000")
        .config("spark.hadoop.dfs.client.use.datanode.hostname", "false")
        .config("spark.executor.memory", EXECUTOR_MEMORY)
        .config("spark.cores.max", CORES_MAX)
        .config("spark.executor.extraJavaOptions", "-Dhadoop.security.logger=ERROR,RFAS")
        .getOrCreate()
    )
    sc = spark.sparkContext
    print("Spark Master:", sc.master)
    print("Default Parallelism:", sc.defaultParallelism)
    print("NameNode IP:", namenode_ip)
    return spark

if __name__ == "__main__":
    spark = create_spark_session()
    spark.stop()
