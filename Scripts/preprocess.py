"""
Veri ön işleme modülü.
- gerekli sütunları seçer
- headline + short_description alanlarını birleştirir
- metni küçük harfe çevirir
- link ve özel karakter temizliği yapar
- filter ile boş/kısa metinleri çıkarır
"""
from pyspark.sql.functions import col, lower, regexp_replace, concat_ws, length


def preprocess_data(df):
    df_selected = df.select("category", "headline", "short_description", "date")

    df_selected = df_selected.withColumn(
        "text",
        concat_ws(" ", "headline", "short_description")
    )

    df_selected = df_selected.withColumn("text", lower(col("text")))

    df_selected = df_selected.withColumn(
        "text",
        regexp_replace(col("text"), r"http\S+|[^a-zA-Z\s]", "")
    )

    df_selected = df_selected.filter(
        col("text").isNotNull() & (length(col("text")) > 20)
    )

    print("Ön işleme sonrası kayıt sayısı:", df_selected.count())
    return df_selected
