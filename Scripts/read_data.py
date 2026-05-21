"""HDFS üzerindeki News Category Dataset dosyasını PySpark DataFrame olarak okur."""
from config import get_hdfs_data_path


def read_dataset(spark):
    data_path = get_hdfs_data_path()
    print("Okunan HDFS yolu:", data_path)
    df = spark.read.json(data_path)
    print("Toplam kayıt:", df.count())
    print("Partition sayısı:", df.rdd.getNumPartitions())
    df.printSchema()
    return df
