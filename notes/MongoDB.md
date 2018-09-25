## MongoDB

MongoDB属于NoSQL数据库，MongoDB的基本概念是文档、集合、数据库。

与SQL的对比如下：

| SQL概念  | MonogoDB概念 | 说明          |
| -------- | ------------ | ------------- |
| database | database     | 数据库        |
| table    | collection   | 数据库表/集合 |
| row      | document     | 数据行        |
| column   | field        | 数据字段列/域 |
| index    | index        | 索引          |



### 文档

文档是Mono'goDB中数据的基本单元，类似关系型数据库中行。文档有唯一的标识id，数据库可以自动生成。文档以key/value的方式组织。比如：

{"name": "lee", "age": 20 }

### 集合

集合是MongoDB的一组文档，类似关系型数据库中的数据表。集合存在于数据库中，集合没有固定的结构，这移位者可以插入不同格式和类型的数据。比如

{"name": "lee", "age": 19}、{”name": "lee", "age": 19, "sex": 1}可以在一个集合中。

### 常用操作

1. 创建和删除数据库

   use DATA_NAME

   db.dropDatabase() ：可以删除当前数据库

2. 插入文档

   db.COLLECTION_NAME.insert(document)

   例如：

   db.python.insert({"name": "lee"})

3. 查找文档

   ```
   集合python下的所有文档
   db.python.find().pretty()
   
   集合python中name等于lee和age等于19的文档.
   db.python.find({"name": "lee", "age": 19}).pretty()
   
   集合python中name等于lee或者age等于19的文档
   db.python.find(
   $or[
       "name": "lee",
       "age": 19
   ])
   
   ```

4. 更新文档

   ```
   db.python.update(
   	query,
   	update,
   	{
           upsert:boolean
           multi: boolean
           writeConcern:document
   	}
   )
   ```

   参数分析：

   - query: update的查询条件，类似where自居
   - update:updated的对象和一些更新的操作等，类似于set后面的内容
   - upsert：可选，这个参数意思是如果不存在update的记录，是否插入新文档，true为插入
   - multi: 可选，false为只更新找到的第一条记录，如果这个参数为true，就把按条件查出来的多条记录全部更新。

5. 删除文档

   db.python.remove({'name': 'lee'})