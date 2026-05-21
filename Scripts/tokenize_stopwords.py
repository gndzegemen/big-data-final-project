"""Tokenization ve stopword temizleme modülü."""
import nltk
from nltk.corpus import stopwords
from pyspark.ml.feature import Tokenizer, StopWordsRemover
from pyspark.sql.functions import size


def tokenize_text(df_selected):
    tokenizer = Tokenizer(inputCol="text", outputCol="tokens")
    df_tokenized = tokenizer.transform(df_selected)
    return df_tokenized


def remove_stopwords(df_tokenized):
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")

    spark_stopwords = StopWordsRemover.loadDefaultStopWords("english")
    nltk_stopwords = stopwords.words("english")
    custom_stopwords = [
        "said", "new", "one", "time", "day", "week",
        "best", "photos", "photo", "video", "people",
        "make", "get", "like", "may"
    ]

    all_stopwords = list(set(spark_stopwords + nltk_stopwords + custom_stopwords))

    remover = StopWordsRemover(
        inputCol="tokens",
        outputCol="filtered_tokens",
        stopWords=all_stopwords
    )

    df_filtered = remover.transform(df_tokenized)
    df_counts = df_filtered.select(
        size("tokens").alias("token_count_before"),
        size("filtered_tokens").alias("token_count_after")
    )
    df_counts.show(10, truncate=False)
    return df_filtered
