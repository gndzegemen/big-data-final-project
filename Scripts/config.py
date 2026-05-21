"""
Ortak proje ayarları.
Bu dosyadaki değerleri kendi Docker/HDFS/Spark ortamına göre değiştirebilirsin.
"""

import subprocess
from pathlib import Path

APP_NAME = "HaberAnalizi"
SPARK_MASTER = "spark://localhost:7077"

SPARK_DRIVER_HOST = "172.18.0.1"
SPARK_DRIVER_BIND_ADDRESS = "0.0.0.0"
SPARK_DRIVER_PORT = "4045"
SPARK_BLOCKMANAGER_PORT = "4046"

EXECUTOR_MEMORY = "512m"
CORES_MAX = "2"

HDFS_INPUT_DIR = "/bigdata/news/input"
DATASET_FILE = "News_Category_Dataset_v3.json"
LOCAL_DATASET_PATH = Path("News_Category_Dataset_v3.json")


def get_namenode_ip(container_name: str = "namenode") -> str:
    """Docker içindeki NameNode container IP adresini otomatik bulur."""
    cmd = (
        "docker inspect -f "
        "'{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "
        f"{container_name}"
    )
    try:
        ip = subprocess.check_output(cmd, shell=True, text=True).strip().strip("'")
        if ip:
            return ip
    except Exception:
        pass
    return "172.18.0.4"


def get_hdfs_data_path() -> str:
    namenode_ip = get_namenode_ip()
    return f"hdfs://{namenode_ip}:9000{HDFS_INPUT_DIR}/{DATASET_FILE}"
