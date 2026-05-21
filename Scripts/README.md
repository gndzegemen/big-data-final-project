# Big Data Final Project - Çalıştırma Yönergesi

Bu klasör, Jupyter Notebook içinde geliştirilen haber verileri konu modelleme projesinin `.py` dosyalarına ayrılmış halidir.

## 1. Proje Mimarisi

Çalışma ortamı şu yapı üzerine kuruludur:

- Windows ana makine
- VirtualBox üzerinde Ubuntu sanal makinesi
- Ubuntu içinde Docker Compose
- Hadoop HDFS kümesi
  - 1 NameNode
  - 2 DataNode
- Spark kümesi
  - 1 Spark Master
  - 2 Spark Worker
- Jupyter Notebook / PySpark istemcisi

Veri seti HDFS üzerinde saklanır, PySpark ile okunur, TF-IDF özellikleri çıkarılır ve LDA modeli ile topic modeling yapılır.

## 2. Dosya Açıklamaları

| Dosya | Görev |
|---|---|
| `config.py` | HDFS, Spark, container ve dosya yolu ayarları |
| `spark_session.py` | SparkSession oluşturma |
| `read_data.py` | HDFS üzerindeki JSON veri setini okuma |
| `preprocess.py` | Sütun seçimi, text oluşturma, lowercase, regex temizleme, filter |
| `tokenize_stopwords.py` | Tokenization ve stopword temizleme |
| `tfidf_features.py` | CountVectorizer + IDF ile TF-IDF oluşturma |
| `train_lda.py` | LDA modelini eğitme ve metrikleri hesaplama |
| `results.py` | Kategori dağılımı, topic kelimeleri, dominant topic sonuçları |
| `run_all.py` | Tüm pipeline'ı baştan sona çalıştırma |

## 3. Bağımlılıklar

Python ortamında aşağıdaki paketler gerekir:

```bash
pip install -r requirements.txt
```

Gerekli sistem bileşenleri:

- Docker
- Docker Compose
- Hadoop containerları
- Spark containerları
- Java
- Python 3.8+ / 3.10

## 4. Docker Cluster'ı Başlatma

Docker Compose dosyasının bulunduğu klasöre gir:

```bash
cd ~/bigdata-cluster/docker-hadoop
```

Servisleri başlat:

```bash
docker-compose up -d
```

Container durumunu kontrol et:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

HDFS durumunu kontrol et:

```bash
docker exec -it namenode hdfs dfsadmin -report
```

Spark UI:

```text
http://localhost:8081
```

HDFS UI:

```text
http://localhost:9870
```

## 5. Veri Setini HDFS'e Yükleme

Veri seti dosyasının bulunduğu proje klasörüne git:

```bash
cd ~/Desktop/big-data-final-project
```

Dosyayı NameNode container içine kopyala:

```bash
docker cp News_Category_Dataset_v3.json namenode:/tmp/
```

HDFS klasörünü oluştur:

```bash
docker exec -it namenode hdfs dfs -mkdir -p /bigdata/news/input
```

Veriyi HDFS'e yükle:

```bash
docker exec -it namenode hdfs dfs -put -f /tmp/News_Category_Dataset_v3.json /bigdata/news/input/
```

Yüklendiğini doğrula:

```bash
docker exec -it namenode hdfs dfs -ls /bigdata/news/input
```

## 6. Kodları Çalıştırma

Bu klasörü proje dizinine kopyala ve içine gir:

```bash
cd project_py_scripts
```

Tüm pipeline'ı çalıştır:

```bash
python run_all.py
```

Tek tek çalıştırmak istersen:

```bash
python spark_session.py
python 01_read_data.py   # Bu dosya yerine run_all önerilir
```

Not: Ana önerilen çalışma şekli `run_all.py` dosyasıdır.

## 7. Beklenen Çıktılar

Çalışma sonunda terminalde şu sonuçlar görülür:

- Spark Master bilgisi
- Default parallelism
- Toplam kayıt sayısı
- Partition sayısı
- Ön işleme sonrası kayıt sayısı
- Token sayısı karşılaştırması
- Vocabulary size
- Log Likelihood
- Log Perplexity
- Kategori dağılımı
- Topic anahtar kelimeleri
- Her haber için dominant topic

## 8. Olası Hatalar ve Çözümler

### Hata: Initial job has not accepted any resources

Spark worker kaynak ayırmıyor olabilir. Kontrol et:

```bash
docker restart spark-master spark-worker-1 spark-worker-2
```

Sonra Spark UI'de workerların göründüğünü kontrol et.

### Hata: UnknownHostException: namenode

Notebook veya Python script Docker ağı dışından `namenode` ismini çözemiyor olabilir. Bu proje bu nedenle NameNode IP adresini `docker inspect` ile otomatik bulur.

### Hata: Python version mismatch

Driver ve worker Python sürümleri farklıysa UDF içeren kodlarda hata alınabilir. Bu proje UDF kullanımını minimumda tutar ve Spark SQL fonksiyonlarını tercih eder.

### Hata: Bellek yetersizliği / worker lost

`config.py` içinde kaynakları düşük tut:

```python
EXECUTOR_MEMORY = "512m"
CORES_MAX = "2"
```

## 9. Notlar

- Pandas yalnızca küçük örnek çıktıları göstermek için kullanılmıştır.
- Veri işleme PySpark DataFrame ve Spark MLlib üzerinde yapılmaktadır.
- `filter`, `groupBy`, `aggregation`, TF-IDF ve LDA adımları proje isterlerini karşılamak için görünür biçimde ayrılmıştır.
