# 📊 Daily Transaction Fact Table Pipeline (PySpark)

## 📌 Deskripsi Assignment

Project ini bertujuan untuk membangun fact table transaksi harian yang rapi, konsisten, dan efisien untuk kebutuhan analitik.

Pipeline dibangun menggunakan PySpark dengan proses:

* Membaca dataset transaksi
* Membersihkan dan standarisasi data
* Join antar tabel
* Membuat kolom turunan (GMV)
* Menyimpan hasil dalam format Parquet

Output akhir berupa dataset siap analisis dalam format Parquet.

## 🏗️ Arsitektur Pipeline

Pipeline terdiri dari tahapan berikut:

1. Read Data
* orders.csv
* order_items.csv

2. Data Cleaning
* Menghapus kolom tidak relevan
* Menangani nilai null
* Memfilter data tidak valid

3. Standardisasi Data
* Casting tipe data
* Rename kolom
* Standarisasi format tanggal

4. Join Dataset
* Join berdasarkan order_id

5. Derived Column
* Membuat kolom gmv (gross merchandise value)

6. Write Output
* Simpan sebagai .parquet
* Mode: overwrite / append


## Proses Transformasi
✅ 1. Data Cleaning

Minimal satu dari:
* drop() → Menghapus kolom tidak relevan
* fillna() → Mengisi nilai null
* filter() → Menghapus data tidak valid

Contoh:
df = df.filter(df.quantity > 0)

✅ 2. Standardisasi Data

Minimal satu dari:
* cast() → Konversi tipe data
* withColumnRenamed() → Rename kolom
* Standarisasi format tanggal

Contoh:
df = df.withColumn("order_date", col("order_date").cast("date"))

✅ 3. Kolom Turunan (WAJIB)

Membuat kolom:
* gmv = quantity * price

Contoh:
df = df.withColumn("gmv", col("quantity") * col("price"))

### 🔗 Join Dataset

Join dilakukan berdasarkan:
order_id

Contoh:
df_join = orders.join(order_items, "order_id", "inner")

Output akhir merupakan fact table transaksi harian dengan struktur detail per item.

## airflow
`docker compose --profile airflow up -d`

## grafana
`docker compose --profile grafana up -d`

## postgres
`docker compose --profile postgres up -d`
or `docker compose --profile db up -d` (mysql + postgres)

## mysql
`docker compose --profile mysql up -d`
or `docker compose --profile db up -d` (mysql + postgres)

## hive
`docker compose --profile hive up -d`

## kafka
`docker compose --profile kafka up -d`

## spark
`docker compose --profile spark up -d`
