"""LDA topic modeling modeli eğitimi ve model metrikleri."""
from pyspark.ml.clustering import LDA


def train_lda_model(df_tfidf, k=10, max_iter=10, seed=42):
    lda = LDA(k=k, maxIter=max_iter, featuresCol="features", seed=seed)
    lda_model = lda.fit(df_tfidf)

    log_likelihood = lda_model.logLikelihood(df_tfidf)
    log_perplexity = lda_model.logPerplexity(df_tfidf)

    print("Log Likelihood:", log_likelihood)
    print("Log Perplexity:", log_perplexity)
    return lda_model, log_likelihood, log_perplexity
