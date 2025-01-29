
1. Устанавливаем Kafka и Spark в Docker (docker-compose.yml)

2. Создаем топики

3. producer.py - посылает сообщения в топики в формате id , action
Пример
{"id": 3, "action": "LOS818V101FNOFNPKY3Z"}
{"id": 4, "action": "78Y2PO4V1Q5ZOB6ZVHN5"}
{"id": 0, "action": "N0TZLG4LZDYBGDOC2LYQ"}

4. structure_streaming_kafka.py - Обрабатывает сообщения из Kafka с помощью объекта  Spark -и выводит поток сообщений в консоль

5. join_action_users.png - скрин из консоли - результат join с статическим dataset где каждому id сопоставлен user users_data = [(1,"Jimmy",18),(2,"Hank",48),(3,"Johnny",9),(4,"Erle",40)]

join_stream = stat_stream.join(users, stat_stream.id == users.id, "left_outer").select(users.id,users.user_name, users.user_age, col('count'), col('last_timestamp'))
join_stream.writeStream.format("console").outputMode("complete").option("truncate", False).start().awaitTermination()


   В результате в консоли видим
|           timestamp| id|user_name|user_age|              action|
+--------------------+---+---------+--------+--------------------+
|2025-01-26 17:02:...|  2|     Hank|      48|A9E1DUZUSWL7CEC37A8M|


6. agg_count_users.png - скрин из консоли где считаем количество сообщений по каждому user_id

#добавим агрегат - отображать число уникальных айдишников
stat_stream = clean_data.groupBy("id").agg(
        count("*").alias("count"),
        max("timestamp").alias("last_timestamp")  # Сохраняем последний timestamp
    )
#stat_stream.writeStream.format("console").outputMode("complete").option("truncate", False).start().awaitTermination()

Результат
   Batch: 2
-------------------------------------------
+----+---------+--------+-----+-----------------------+
|id  |user_name|user_age|count|last_timestamp         |
+----+---------+--------+-----+-----------------------+
|1   |Jimmy    |18      |1    |2025-01-26 16:58:02.633|
|3   |Johnny   |9       |2    |2025-01-26 16:57:58.626|
|4   |Erle     |40      |6    |2025-01-26 16:58:05.64 |
|2   |Hank     |48      |5    |2025-01-26 16:57:52.622|
|NULL|NULL     |NULL    |2    |2025-01-26 16:58:02.632|

   
