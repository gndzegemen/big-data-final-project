"""
Projeyi baştan sona çalıştıran ana dosya.
Sıra:
1. SparkSession oluştur
2. HDFS'ten veri oku
3. Ön işleme
4. Tokenization + stopword temizleme
5. TF-IDF
6. LDA eğitimi
7. Sonuçların üretilmesi
"""
from spark_session import create_spark_session
from read_data import read_dataset
from preprocess import preprocess_data
from tokenize_stopwords import tokenize_text, remove_stopwords
from tfidf_features import build_tfidf_features
from train_lda import train_lda_model
from results import category_distribution, extract_topic_keywords, assign_dominant_topic


def main():
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    try:
        df = read_dataset(spark)
        df_selected = preprocess_data(df)
        df_tokenized = tokenize_text(df_selected)
        df_filtered = remove_stopwords(df_tokenized)
        df_tfidf, cv_model, _ = build_tfidf_features(df_filtered)
        lda_model, _, _ = train_lda_model(df_tfidf)

        category_distribution(df)
        _, topics_pd = extract_topic_keywords(lda_model, cv_model)
        assign_dominant_topic(lda_model, df_tfidf, topics_pd)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
