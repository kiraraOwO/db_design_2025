# title

<details>
<summary>PDF总结</summary>

## table的创建和删除

```sql
CREATE TABLE 表名 (
列名1 列名1の型,
列名2 列名2の型,
...
);
```

* sql 大小写不敏感
* 命令最后加封号（;）
* 表名可以用非英文

### 常见type
- INTEGER 整数(4byte)
- BIGINT 広範囲整数(8byte)
- REAL 単精度浮動小数点数(4byte)
- DOUBLE PRECISION 倍精度浮動小数点数(8byte)
- SERIAL 連番整数型(4byte)
- BIGSERIAL 広範囲連番整数型(8byte)
- CHAR(n) 空白で埋められた固定⻑文字列
- VARCHAR(n) 上限付き可変⻑文字列
- TEXT 制限なし可変⻑文字列

### PRIMARY KEY / NOT NULL / SERIAL
- 主键不能为空，不可重复，一般和SERIAL自动连号拼在一起（SERIAL PRIMARY KEY）
- NOT NULL 拼在任意不可为null值的行的type后

## 删表

```
DROP TABLE 表名;
```
如果有别的表用这个表的键作为外键那是删不了的

## SELECT 格式和sql处理顺序

- SELECT <カラムを指定する>
- FROM <テーブルを指定する>
- WHERE <抽出条件を指定する>
- GROUP BY <グループ化の条件を指定する>
- HAVING <グループ化した後の抽出条件を指定する>
- ORDER BY <データの並び順を指定する>
- LIMIT <取得する行数を制限する>

FROM 句 → WHERE 句 → GROUP BY 句 → HAVING 句 → SELECT 句 → ORDER BY 句 → LIMIT 句

## 操作演示

### 拼表

[cnblogs](https://www.cnblogs.com/ThinkVenus/p/10095543.html)

#### INNER JOIN

- INNER JOIN
  - 写法：`SELECT * FROM TableA INNER JOIN TableB ON TableA.name = TableB.name;`
  - 会把表中name列中相同的内容分别打印出来

#### <FULL/LEFT/RIGHT> OUTER JOIN

- FULL OUTER JOIN
  - 写法：`SELECT * FROM TableA FULL OUTER JOIN TableB ON TableA.name = TableB.name;`
  - 会把两个表的所有数据列出来，相同name的列在同一行，没有相同数据的会在另一张上写null
  - 如果只想要没有交集的合集可以用where实现

- LEFT OUTER JOIN
  - 写法：`SELECT * FROM TableA FEFT OUTER JOIN TableB ON TableA.name = TableB.name;`
  - 显示所有左边表的数据，右边表显示相同的部分，不同填null

- RIGHT OUTER JOIN
  - 同上，就是反过来

#### CROSS JOIN

- 两表相乘拼表，求笛卡尔积，表太大容易爆破
- 写法：`SELECT * FROM a, b;` & `SELECT * FROM a CROSS JOIN b;`

#### UNION, UNION ALL, EXCEPT, INTERSECT

- UNION
  - 合并两个或多个SELECT的结果，去重
  - 注：SELECT选取的列数量和类型需相同，选取多个列时需要当前行字段和另一张表完全相同时才会合并
 
- UNION ALL
  - 同上，但不去重，全部打印
 
- EXCEPT
  - 第一个SELECT的结果上减去第二个SELECT的结果，用于只在第一个SELECT中出现的结果
  - 例：第一个SELECT结果A,B,C，第二个SELECT结果B,D，那么最后的结果就是A,C

- INTERSECT
  - 返回两SELECT的重复值，会去重
 
#### VIEW

- 是一个虚拟表，根据查询条件来显示内容
- 用法：在SELECT语句前插入创表语句，稍微不同
- `CREATE VIEW <TABLE> AS ...`
- 之后就可以和表一样操作，INSERT/UPDATE/DELETE 有限制
- 删表和正常删表差不多，就是多个VIEW：`DROP VIEW <TABLE>;`

### 其他东西

* 查数据
  * `SELECT 列名1, 列名2, ... FROM 表名 WHERE 条件式`
  * 用 * 会显示整个表

* SELECT 展示别名
  *  `SELECT listA AS A, listB AS B FROM table;`
  *  说明：listA在打印时会显示为A，listB同理
 
* 生成固定数据
  * 如果这个表没这一列，但又需要生成的时候用
  * `SELECT name, '<值>' AS <列名>, ... FROM table;`

## 条件搜索

[cnblogs](https://www.cnblogs.com/xiaowange/p/17870864.html)

### 算数运算符

* `+ - * / MOD`
* SELECT和WHERE中都可以用
* 比如SELECT一个 price 和一个 price*0.9 AS 90ps_price，然后where条件写 price * 0.9 < 1000，这样就能同时列出原始价格和九折价格

### 比较运算符

* `= <> < > <= >=`
* 注：<> 是 !=

### NULL (IS NULL, IS NOT NULL)

* 用来筛某个条件是不是null的
* 例：`SELECT * FROM customers WHERE email IS NULL;`

### 逻辑运算符

* `AND OR NOT`

### 加括号

* 把两个条件合为一组

### IN

* 在where里用的，相当于OR的简洁写法
* 例：`WHERE <product_id> IN (1, 3, 4)` 打印出 id 为 1,3,4 的行（如果SELECT是*）

### BETWEEN

* 字面意思，在两个值之间，比如筛日期
* 例：`WHERE order_date BETWEEN '2025-03-01' AND '2025-03-02'`

### LIKE

* 条件模糊匹配，%任意数量字符，_单个字符
* `WHERE name LIKE 'A%'`
  * 开头：A%
  * 结尾：%D
  * 中间（左右任意）：%byd%
  * 首字符任意：_gg%
* 大小写敏感问题：在WHERE后的条件上加`LOWER()`，匹配全用小写就行

### 位运算符

* `. ^ $ [ ] * + ? | ( )`
  * `.` 任一字符
  * `^` 开头
  * `$` 结尾
  * `[]` 字符集中的任一字符（\[abc]匹配a或b或c）
  * `*` 前一个字符0次或多次
  * `+` 前一个字符一次或多次
  * `?` 前一个字符
  * `|` 或，前一个或后一个
  * `()` 分组
  * `{}` 指定前一个字符或前一个模式重复出现的次数
    * `{n}` 重复n次
    * `{n,}` 至少重复n次
    * `{n,m}` 重复n到m次
    * 所有都是包含
    * 例：`[a-zA-Z]{2,}` 会匹配ab，abc等

### 聚合函数

* COUNT, MAX, MIN, SUM, AVG, VAR, STDDEV

### GROUP BY

* `GROUP BY <list>`

### HAVING

* 聚合后条件

### DISTINCT

* 重复行消除

### ORDER BY

* 排序

### LIMIT 和 OFFSET

* 限制和偏移

</details>
