from pyspark.sql import SparkSession

# Создаем SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkTest") \
    .getOrCreate()

# Чтение данных из Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "my_topic") \
    .load()

# Преобразование данных в строки
messageDF = df.selectExpr(
    "CAST(key AS STRING) AS key",
    "CAST(value AS STRING) AS value",
    "topic",
    "partition",
    "offset",
    "timestamp"
)

# Вывод данных в консоль
query = messageDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Ожидаем завершения
query.awaitTermination()
