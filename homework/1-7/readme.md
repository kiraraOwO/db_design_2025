
## 大致思路

### 页面

1. 首页
   * 时间排序
   * 限制首页展示数量（有亿点懒，有亿点烦）
   * 最上方做个登录

2. 登录页面
   * 简单点，只要两个输入框和一个submit就行了
   * 登录反馈
     * 成功就跳一个 <i>欢迎回来，xxx</i> ，然后跳回首页或者后台
     * 失败就不跳转，留在当前页，下面写个字说登录失败

3. 后台页面
   * 文章一览（后台主页)，只显示自己账号的文章，还有增删改按钮
   * 文章编辑页，只要一个标题的输入框和一个文章的输入框就行了，简单点


### 数据库设计

初步推定只需要两个表就行了

* users
  * id
  * nickname
  * email
  * passwd

* articles
  * id (from user table)
  * article_id
  * title -> TEXT
  * content -> TEXT
  * created_timestamp
  * updated_timestamp

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(64),
    email VARCHAR(255) UNIQUE,
    passwd VARCHAR(128)
);

CREATE TABLE articles (
    article_id SERIAL PRIMARY KEY,
    id INTEGER REFERENCES users(id),
    title TEXT,
    content TEXT,
    created_timestamp TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_timestamp TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

### flask app route

* / 
  * 首页
  * 返回限制查询数量后的用户文章
  * 终结点
    * / 第一页
    * /{page} 后面的页数

* /login
  * 登录页面，根据请求方法返回内容
    * get：返回登录页模板
    * post：data就一个email一个passwd

* /user
  * 用户后台
    * 如果有cookies就直接看这是谁然后返回这个人的所有articles的title，新到旧
    * 没有就跳到login
    * 点新增就跳到 /user/new ，在提交的时候再插入id，然后返回用户页面
    * 点修改就跳到 /user/{article_id}，权限啥的也要校验一下
    * 最后提交就都是post方法就行了

