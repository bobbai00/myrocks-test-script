# 第一阶段 Baseline 系统测试结果

## 1. Mysql Server Information

### system

| Field  | Value                                             |
| ------ | ------------------------------------------------- |
| CPU    | 64 core(Intel(R) Xeon(R) Gold 5218 CPU @ 2.30GHz) |
| Memory | 192GB                                             |



### MySQL Instance

| Field                    | Value           |
| ------------------------ | --------------- |
| version                  | 5.6.35          |
| max_connections          | 151             |
| rocksdb_block_cache_size | 536870912       |
| rocksdb_block_size       | 4096            |
| rocksdb_write_policy     | write_committed |



## 2. Benchmark: sysbench

- Link：https://github.com/akopytov/sysbench



## 3. Results

### Fileio benchmark

#### · Configuration

| Field           | Description                                            | Value |
| --------------- | ------------------------------------------------------ | ----- |
| file-total-size | total size of files to create                          | on    |
| file-test-mode  | test mode {seqwr, seqrewr, seqrd, rndrd, rndwr, rndrw} | rndrw |
| file-num        | number of files to create                              | 128   |

#### · Result

```
Throughput:
         read:  IOPS=3175.24 49.61 MiB/s (52.02 MB/s)
         write: IOPS=2116.79 33.07 MiB/s (34.68 MB/s)
         fsync: IOPS=6775.34

Latency (ms):
         min:                                  0.00
         avg:                                  0.08
         max:                                  1.94
         95th percentile:                      0.15
         sum:                               9913.08
```



### CPU benchmark

#### · Configuration

| Field         | Description                        | Value |
| ------------- | ---------------------------------- | ----- |
| cpu-max-prime | N upper limit for primes generator | 10000 |

#### · Result

```
CPU speed:
    events per second:   780.69

Throughput:
    events/s (eps):                      780.6922
    time elapsed:                        10.0001s
    total number of events:              7807

Latency (ms):
         min:                                    1.27
         avg:                                    1.28
         max:                                    1.55
         95th percentile:                        1.34
         sum:                                 9997.73

Threads fairness:
    events (avg/stddev):           7807.0000/0.00
    execution time (avg/stddev):   9.9977/0.00
```



### Mutex benchmark

#### · Configuration

| Field       | Description                                      | Value |
| ----------- | ------------------------------------------------ | ----- |
| mutex-num   | total size of mutex array                        | 4096  |
| mutex-locks | N number of mutex locks to do per thread         | 50000 |
| mutex-loops | N number of empty loops to do outside mutex lock | 10000 |

#### · Result

```
Throughput:
    events/s (eps):                      4.5087
    time elapsed:                        0.2218s
    total number of events:              1

Latency (ms):
         min:                                  221.74
         avg:                                  221.74
         max:                                  221.74
         95th percentile:                      223.34
         sum:                                  221.74

Threads fairness:
    events (avg/stddev):           1.0000/0.00
    execution time (avg/stddev):   0.2217/0.00
```



### Memory benchmark

#### · Configuration

| Field              | Description                        | Value  |
| ------------------ | ---------------------------------- | ------ |
| memory-block-size  | size of memory block for test      | 1K     |
| memory-total-size  | total size of data to transfer     | 256G   |
| memory-scope       | memory access scope {global,local} | global |
| memory-oper        | type of memory operations          | write  |
| memory-access-mode | memory access mode                 | And    |

#### · Result

```
Throughput:
    events/s (eps):                      1211487.5816
    time elapsed:                        10.0000s
    total number of events:              12114922

Latency (ms):
         min:                                    0.00
         avg:                                    0.00
         max:                                    0.09
         95th percentile:                        0.00
         sum:                                 8044.53

Threads fairness:
    events (avg/stddev):           12114922.0000/0.00
    execution time (avg/stddev):   8.0445/0.00
```



### Threads benchmark

#### · Configuration

| Field         | Description                        | Value |
| ------------- | ---------------------------------- | ----- |
| thread-yields | number of yields to do per request | 10000 |
| thread-locks  | number of locks per thread         | 8     |

#### · Result

```
Throughput:
    events/s (eps):                      249.1560
    time elapsed:                        10.0018s
    total number of events:              2492

Latency (ms):
         min:                                    3.96
         avg:                                    4.01
         max:                                    4.23
         95th percentile:                        4.03
         sum:                                10000.74

Threads fairness:
    events (avg/stddev):           2492.0000/0.00
    execution time (avg/stddev):   10.0007/0.00
```





### OLTP benchmark

#### · Configuration

| Field                | Description                                                  | Value   |
| -------------------- | ------------------------------------------------------------ | ------- |
| auto_inc             | Use AUTO_INCREMENT column as Primary Key                     | on      |
| create_secondary     | Create a secondary index in addition to the PRIMARY KEY      | on      |
| delete_inserts       | Number of DELETE/INSERT combinations per transaction         | 1       |
| distinct_ranges      | Number of SELECT DISTINCT queries per transaction            | 1       |
| index_updates        | Number of UPDATE index queries per transaction               | 1       |
| mysql_storage_engine | Storage engine, if MySQL is used                             | RocksDB |
| non_index_updates    | Number of UPDATE non-index queries per transaction           | 1       |
| order_ranges         | Number of SELECT ORDER BY queries per transaction            | 1       |
| point_selects        | Number of point SELECT queries per transaction               | 10      |
| range_selects        | Enable/disable all range SELECT queries                      | on      |
| range_size           | Range size for range SELECT queries                          | 100     |
| reconnect            | Reconnect after every N events.                              | 0       |
| secondary            | Use a secondary index in place of the PRIMARY KEY            | off     |
| simple_ranges        | Number of simple range SELECT queries per transaction        | 1       |
| skip_trx             | Don't start explicit transactions and execute all queries in the AUTOCOMMIT mode | off     |
| sum_ranges           | Number of SELECT SUM() queries per transaction               | 1       |
| table_size           | Number of rows per table                                     | 10000   |
| tables               | Number of tables                                             | 16      |



#### · Results

##### (1) oltp_read_write

| Field          | Result                                                       |
| -------------- | ------------------------------------------------------------ |
| SQL statistics | ![oltp_read_write](/Users/bob/Desktop/test-script/images/oltp/SQL statistics/oltp_read_write.png) |
| Latency        | ![oltp_read_write](/Users/bob/Desktop/test-script/images/oltp/Latency/oltp_read_write.png) |
| Throughput     | ![oltp_read_write](/Users/bob/Desktop/test-script/images/oltp/Throughput/oltp_read_write.png) |

##### (2) oltp_read_only

| Field          | Result                                                       |
| -------------- | ------------------------------------------------------------ |
| SQL statistics | ![oltp_read_only](/Users/bob/Desktop/test-script/images/oltp/SQL statistics/oltp_read_only.png) |
| Latency        | ![oltp_read_only](/Users/bob/Desktop/test-script/images/oltp/Latency/oltp_read_only.png) |
| Throughput     | ![oltp_read_only](/Users/bob/Desktop/test-script/images/oltp/Throughput/oltp_read_only.png) |

##### (3) oltp_write_only

| Field          | Result                                                       |
| -------------- | ------------------------------------------------------------ |
| SQL statistics | ![oltp_write_only](/Users/bob/Desktop/test-script/images/oltp/SQL statistics/oltp_write_only.png) |
| Latency        | ![oltp_write_only](/Users/bob/Desktop/test-script/images/oltp/SQL statistics/oltp_write_only.png) |
| Throughput     | ![oltp_write_only](/Users/bob/Desktop/test-script/images/oltp/Throughput/oltp_write_only.png) |



##### (4) oltp_update_index

| Field          | Result                                                       |
| -------------- | ------------------------------------------------------------ |
| SQL statistics | ![oltp_update_index](/Users/bob/Desktop/test-script/images/oltp/SQL statistics/oltp_update_index.png) |
| Latency        | ![oltp_update_index](/Users/bob/Desktop/test-script/images/oltp/Latency/oltp_update_index.png) |
| Throughput     | ![oltp_update_index](/Users/bob/Desktop/test-script/images/oltp/Throughput/oltp_update_index.png) |



##### (5) oltp_update_non_index

| Field          | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| SQL statistics | ![oltp_update_non_index](/Users/bob/Desktop/test-script/images/oltp/SQL statistics/oltp_update_non_index.png) |
| Latency        | ![oltp_update_non_index](/Users/bob/Desktop/test-script/images/oltp/Latency/oltp_update_non_index.png) |
| Throughput     | ![oltp_update_non_index](/Users/bob/Desktop/test-script/images/oltp/Throughput/oltp_update_non_index.png) |



##### (6) oltp_insert

| Field          | Result                                                       |
| -------------- | ------------------------------------------------------------ |
| SQL statistics | ![oltp_insert](/Users/bob/Desktop/test-script/images/oltp/Latency/oltp_insert.png) |
| Latency        | ![oltp_insert](/Users/bob/Desktop/test-script/images/oltp/Latency/oltp_insert.png) |
| Throughput     | ![oltp_insert](/Users/bob/Desktop/test-script/images/oltp/Throughput/oltp_insert.png) |



##### (7) oltp_delete

| Field          | Result                                                       |
| -------------- | ------------------------------------------------------------ |
| SQL statistics | ![oltp_delete](/Users/bob/Desktop/test-script/images/oltp/SQL statistics/oltp_delete.png) |
| Latency        | ![oltp_delete](/Users/bob/Desktop/test-script/images/oltp/Latency/oltp_delete.png) |
| Throughput     | ![oltp_delete](/Users/bob/Desktop/test-script/images/oltp/Throughput/oltp_delete.png) |



##### (8) oltp_point_select

| Field          | Result                                                       |
| -------------- | ------------------------------------------------------------ |
| SQL statistics | ![oltp_point_select](/Users/bob/Desktop/test-script/images/oltp/SQL statistics/oltp_point_select.png) |
| Latency        | ![oltp_point_select](/Users/bob/Desktop/test-script/images/oltp/SQL statistics/oltp_point_select.png) |
| Throughput     | ![oltp_point_select](/Users/bob/Desktop/test-script/images/oltp/Throughput/oltp_point_select.png) |

