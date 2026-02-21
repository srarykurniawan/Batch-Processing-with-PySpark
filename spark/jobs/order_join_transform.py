from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month

# Create Spark Session
spark = SparkSession.builder \
    .appName("Order Join Transformation") \
    .getOrCreate()

# Paths (SUDAH BENAR)
orders_path = "/opt/airflow/data/orders.csv"
order_items_path = "/opt/airflow/data/order_items.csv"

# Read CSV
orders_df = spark.read.csv(orders_path, header=True, inferSchema=True)
order_items_df = spark.read.csv(order_items_path, header=True, inferSchema=True)

print("Orders Schema:")
orders_df.printSchema()

print("Order Items Schema:")
order_items_df.printSchema()

# =========================
# 1️⃣ DATA CLEANING
# =========================

# Filter invalid quantity
order_items_df = order_items_df.filter(col("quantity") > 0)

# Drop duplicates
orders_df = orders_df.dropDuplicates(["order_id"])

# =========================
# 2️⃣ STANDARIZATION
# =========================

orders_df = orders_df.withColumn("order_date", col("order_date").cast("date"))

order_items_df = order_items_df \
    .withColumn("quantity", col("quantity").cast("int")) \
    .withColumn("price", col("price").cast("int"))

# =========================
# 3️⃣ JOIN
# =========================

joined_df = orders_df.join(order_items_df, on="order_id", how="inner")

# =========================
# 4️⃣ DERIVED COLUMN (WAJIB)
# =========================

joined_df = joined_df.withColumn(
    "value_per_line",
    col("quantity") * col("price")
)

# Extra transformation
joined_df = joined_df \
    .withColumn("order_year", year(col("order_date"))) \
    .withColumn("order_month", month(col("order_date")))

# =========================
# 5️⃣ SAVE TO PARQUET
# =========================

output_path = "/spark/output/order_transformed"

joined_df.write.mode("overwrite").parquet(output_path)

print("Transformation Completed Successfully!")

spark.stop()
