"""Kategori dağılımı, topic kelimeleri ve dominant topic sonuçları."""
from pyspark.sql.functions import col, expr
from pyspark.ml.functions import vector_to_array


def category_distribution(df):
    category_counts = (
        df.groupBy("category")
        .count()
        .orderBy(col("count").desc())
    )
    category_counts.show(20, truncate=False)
    return category_counts


def extract_topic_keywords(lda_model, cv_model, top_n=10):
    topics = lda_model.describeTopics(top_n)
    vocab = cv_model.vocabulary

    def indices_to_words(indices):
        return [vocab[i] for i in indices]

    topics_pd = topics.toPandas()
    topics_pd["words"] = topics_pd["termIndices"].apply(indices_to_words)
    print(topics_pd[["topic", "words"]])
    return topics, topics_pd


def assign_dominant_topic(lda_model, df_tfidf, topics_pd, sample_size=20):
    df_topics = lda_model.transform(df_tfidf)
    df_topics = df_topics.withColumn(
        "topic_array",
        vector_to_array("topicDistribution")
    )
    df_topics = df_topics.withColumn(
        "dominant_topic",
        expr("array_position(topic_array, array_max(topic_array)) - 1")
    )

    topic_words = {
        row["topic"]: ", ".join(row["words"][:3])
        for _, row in topics_pd.iterrows()
    }

    df_topics_pd = (
        df_topics.select("headline", "dominant_topic")
        .limit(sample_size)
        .toPandas()
    )
    df_topics_pd["dominant_topic_text"] = df_topics_pd["dominant_topic"].map(topic_words)
    print(df_topics_pd[["headline", "dominant_topic_text"]])
    return df_topics, df_topics_pd
