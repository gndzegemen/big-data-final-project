"""CountVectorizer ve IDF ile TF-IDF özellik çıkarımı."""
from pyspark.ml.feature import CountVectorizer, IDF


def build_tfidf_features(df_filtered, vocab_size=5000, min_df=5):
    cv = CountVectorizer(
        inputCol="filtered_tokens",
        outputCol="raw_features",
        vocabSize=vocab_size,
        minDF=min_df
    )
    cv_model = cv.fit(df_filtered)
    df_cv = cv_model.transform(df_filtered)

    idf = IDF(inputCol="raw_features", outputCol="features")
    idf_model = idf.fit(df_cv)
    df_tfidf = idf_model.transform(df_cv)

    print("Vocabulary size:", len(cv_model.vocabulary))
    return df_tfidf, cv_model, idf_model
