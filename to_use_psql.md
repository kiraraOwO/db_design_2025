# 使用pSQL

## 初始化
* `createdb <db_name>` 创建数据库
* `psql -l` 列出可用库
* `psql <db_name>` 进入数据库

psql有点像mangodb的shell，就是用来管理的

## 创表
* `CREATE TABLE <table_name> ();`
  * 内容物
    * `<列名> TYPE [约束项],`  详见[如何在 PostgreSQL 中创建和删除数据库和表](https://prisma.org.cn/dataguide/postgresql/create-and-delete-databases-and-tables)
    * 其中一般会插入的固定按顺序生成的递增的列 `<it_can_be_id> SERIAL PRIMARY KEY` 称之为[主键](https://prisma.org.cn/dataguide/intro/database-glossary#primary-key)
    * 常见的列约束
      * `PRIMARY KEY` 上面提到的主键，一个表只能有一个主键
      * `NOT NULL` 不能存储 NULL 值
      * `UNIQUE` 确保此列值唯一
