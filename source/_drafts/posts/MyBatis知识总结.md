---
date: 2024-10-29T18:14:41.967Z
updated: null
title: MyBatis知识总结
slug: MyBatis
oid: 67212611c10f2bbf49961116
categories: Java
type: post
permalink: /posts/Java/MyBatis
---


MyBatis 是一款优秀的持久层框架，它支持定制化 SQL、存储过程以及高级映射。MyBatis 避免了几乎所有的 JDBC 代码和手动设置参数以及获取结果集。MyBatis 可以使用简单的 XML 或注解来配置和映射原生 SQL 查询，将接口和 Java 的实体类映射成数据库中的记录。

### 优点分析

1. **灵活**：MyBatis 不会对应用程序或数据库的现有设计强加任何限制。它使用简单的 XML 或注解来配置和映射原始类型、接口和 Java POJO 为数据库中的记录。
2. **易于学习**：MyBatis 相对于其他 ORM 框架来说，学习曲线较低，因为它不需要开发人员学习新的领域特定语言（DSL）或复杂的 API。
3. **性能**：MyBatis 可以通过缓存和批量更新等技术来提高性能。
4. **可定制性**：MyBatis 提供了许多插件和扩展点，例如 Plugin 扩展点，它是用于拦截 MyBatis 执行前后操作的接口，可以通过实现该接口来自定义 MyBatis 的行为，这样开发者就可以根据需要进行定制。

### 缺点分析

MyBatis 有以下缺点：

1. **SQL 语句依赖**：MyBatis 需要手动编写 SQL 语句，这意味着开发人员需要具备一定的 SQL 知识。此外，如果数据库模式发生变化，需要手动修改 SQL 语句，这可能会导致一些问题。
2. **XML 配置文件冗长**：MyBatis 的配置文件通常比较冗长，这可能会导致一些维护问题。此外，如果使用注解配置，代码可能会变得混乱。
3. **缺乏自动化创建**：相比于其他 ORM 框架，MyBatis 缺乏自动化。例如，它不支持自动创建表和字段。

### MyBatis 和 Hibernate
两个常用的 Java 持久化框架，主要区别在于对象关系映射、查询语言、学习曲线、性能控制等方面。

- **对象关系映射（ORM）方式**：Hibernate 是一个全自动的 ORM 框架，通过对象关系映射技术，将数据库表与 Java 对象之间的映射关系自动管理，不需要手动编写 SQL 语句。而 MyBatis 是一个半自动的 ORM 框架，需要开发者手动编写和管理 SQL 语句。
- **查询语言**：Hibernate 使用 Hibernate Query Language（HQL）或 Criteria API 进行数据库查询，它们是面向对象的查询语言，类似于 SQL 语法。而 MyBatis 直接使用原生的 SQL 语句进行查询，可以更灵活地进行定制和优化。
- **学习曲线**：由于 Hibernate 提供了全自动的 ORM 特性，对于开发者来说，学习成本相对较高，需要理解和掌握其复杂的特性和概念。相比之下，MyBatis 更接近于传统的 JDBC 编程模型，学习曲线相对较低，开发者可以更灵活地控制和优化 SQL 语句。
- **性能控制**：由于 MyBatis 需要手动编写和优化 SQL 语句，开发者可以更精确地控制查询的性能。而 Hibernate 在某些情况下可能会生成复杂的 SQL 语句，性能方面可能不如 MyBatis 灵活。

### MyBatis 的执行流程

1. **读取配置文件**：读取 MyBatis 配置文件（通常是 mybatis-config.xml），该文件包含了 MyBatis 的全局配置信息，如数据库连接信息、类型别名、插件等。
2. **创建 SqlSessionFactory**：SqlSessionFactory 是 MyBatis 的核心接口之一，它负责创建 SqlSession 对象。SqlSessionFactory 可以通过 XML 配置文件或 Java 代码进行配置。
3. **创建 SqlSession**：SqlSession 是 MyBatis 的另一个核心接口，它负责与数据库进行交互。SqlSession 提供了许多方法，如 selectOne、selectList、insert、update、delete 等，可以执行 SQL 语句并返回结果。
4. **执行 SQL 语句**：SqlSession 会根据 Mapper 接口中的方法名和参数，找到对应的 SQL 语句并执行。在执行 SQL 语句之前，MyBatis 会将 `#{}`替换为实际的参数值，并将 `${}` 替换为实际的 SQL 语句。
5. **返回结果**：执行 SQL 语句后，MyBatis 会将结果映射为 Java 对象并返回。MyBatis 提供了许多映射方式，如基于 XML 的映射、注解映射、自定义映射等。

### [#{} 和 ${} 的区别是什么？](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#%E5%92%8C-%E7%9A%84%E5%8C%BA%E5%88%AB%E6%98%AF%E4%BB%80%E4%B9%88)

`${}`是 Properties 文件中的变量占位符，它可以用于标签属性值和 sql 内部，属于原样文本替换，可以替换任意内容，比如${driver}会被原样替换为`com.mysql.jdbc. Driver`。

`#{}`是 sql 的参数占位符，MyBatis 会将 sql 中的`#{}`替换为? 号，在 sql 执行前会使用 PreparedStatement 的参数设置方法，按序给 sql 的? 号占位符设置参数值，比如 ps.setInt(0, parameterValue)，`#{item.name}` 的取值方式为使用反射从参数对象中获取 item 对象的 name 属性值，相当于 `param.getItem().getName()`。

- **功能不同**：`${}` 是直接替换，而 `#{}`是预处理；
- **使用场景不同**：普通参数使用 `#{}`，如果传递的是 SQL 命令或 SQL 关键字，需要使用 `${}`，但在使用前一定要做好安全验证；
- **安全性不同**：使用 `${}` 存在安全问题，如 SQL 注入，而 `#{}` 则不存在安全问题。

### SQL 注入

是指应用程序对用户输入数据的合法性没有判断或过滤不严，攻击者可以在应用程序中事先定义好的查询语句的结尾上添加额外的 SQL 语句，在管理员不知情的情况下实现非法操作

```sql
<select id="isLogin" resultType="com.example.demo.model.User">
    select * from userinfo where username='${name}' and password='${pwd}'
</select>

“' or 1='1”
```

### 动态SQL
可以根据不同的参数信息来动态拼接的不确定的 SQL 叫做动态 SQL，MyBatis 动态 SQL 的主要元素有：if、choose/when/otherwise、trim、where、set、foreach 等。

```sql
<select id="findUser" parameterType="com.interview.entity.User" resultType="com.interview.entity.User">
      select * from t_user where 1=1
      <if test="id!=null">
        and id = #{id}
      </if>
      <if test="username!=null">
        and username = #{username}
      </if>
      <if test="password!=null">
        and password = #{password}
      </if>
</select>
```

### MyBatis 二级缓存

作用是减少数据库的查询次数，提高系统性能。

二级缓存包含两级缓存：一级缓存和二级缓存。

1. 一级缓存是 SqlSession 级别的，是 MyBatis 自带的缓存功能，并且无法关闭，因此当有两个 SqlSession 访问相同的 SQL 时，一级缓存也不会生效，需要查询两次数据库；
2. 二级缓存是 Mapper 级别的，只要是同一个 Mapper，无论使用多少个 SqlSession 来操作，数据都是共享的，多个不同的 SqlSession 可以共用二级缓存，MyBatis 二级缓存默认是关闭的，需要使用时可手动开启，二级缓存也可以使用第三方的缓存，比如，使用 Ehcache 作为二级缓存。

#### 一级缓存 VS 二级缓存

一级缓存和二级缓存的区别如下：

1. 一级缓存是 SqlSession 级别的缓存，它的作用域是同一个 SqlSession，同一个 SqlSession 中的多次查询会共享同一个缓存。二级缓存是 Mapper 级别的缓存，它的作用域是同一个 Mapper，同一个 Mapper 中的多次查询会共享同一个缓存。
2. 一级缓存是默认开启的，不需要手动配置。二级缓存需要手动配置，需要在 Mapper.xml 文件中添加 cache 标签。
3. 一级缓存的生命周期是和 SqlSession 一样长的，当 SqlSession 关闭时，一级缓存也会被清空。二级缓存的生命周期是和 MapperFactory 一样长的，当应用程序关闭时，二级缓存也会被清空。
4. 一级缓存只能用于同一个 SqlSession 中的多次查询，不能用于跨 SqlSession 的查询。二级缓存可以用于跨 SqlSession 的查询，多个 SqlSession 可以共享同一个二级缓存。
5. 一级缓存是线程私有的，不同的 SqlSession 之间的缓存数据不会互相干扰。二级缓存是线程共享的，多个 SqlSession 可以共享同一个二级缓存，需要考虑线程安全问题。

### MyBatis设计模式

工厂模式、建造者模式、单例模式、适配器模式、代理模式、模板方法模式等

#### 1.工厂模式

工厂模式想必都比较熟悉，它是 Java 中最常用的设计模式之一。工厂模式就是提供一个工厂类，当有客户端需要调用的时候，只调用这个工厂类就可以得到自己想要的结果，从而无需关注某类的具体实现过程。这就好比你去餐馆吃饭，可以直接点菜，而不用考虑厨师是怎么做的。

工厂模式在 MyBatis 中的典型代表是 SqlSessionFactory。SqlSession 是 MyBatis 中的重要 Java 接口，可以通过该接口来执行 SQL 命令、获取映射器示例和管理事务，而 SqlSessionFactory 正是用来产生 SqlSession 对象的，所以它在 MyBatis 中是比较核心的接口之一。

####  [2.建造者模式](https://javacn.site/interview/mybatis/mybatis_design.html#_2-%E5%BB%BA%E9%80%A0%E8%80%85%E6%A8%A1%E5%BC%8F) 

建造者模式指的是将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。也就是说建造者模式是通过多个模块一步步实现了对象的构建，相同的构建过程可以创建不同的产品。

例如，组装电脑，最终的产品就是一台主机，然而不同的人对它的要求是不同的，比如设计人员需要显卡配置高的；而影片爱好者则需要硬盘足够大的（能把视频都保存起来），但对于显卡却没有太大的要求，我们的装机人员根据每个人不同的要求，组装相应电脑的过程就是建造者模式。

建造者模式在 MyBatis 中的典型代表是 SqlSessionFactoryBuilder。普通的对象都是通过 new 关键字直接创建的，但是如果创建对象需要的构造参数很多，且不能保证每个参数都是正确的或者不能一次性得到构建所需的所有参数，那么就需要将构建逻辑从对象本身抽离出来，让对象只关注功能，把构建交给构建类，这样可以简化对象的构建，也可以达到分步构建对象的目的，而 SqlSessionFactoryBuilder 的构建过程正是如此。

#### 3.单例模式

单例模式（Singleton Pattern）是 Java 中最简单的设计模式之一，此模式保证某个类在运行期间，只有一个实例对外提供服务，而这个类被称为单例类。

单例模式也比较好理解，比如一个人一生当中只能有一个真实的身份证号，每个收费站的窗口都只能一辆车子一辆车子的经过，类似的场景都是属于单例模式。单例模式在 MyBatis 中的典型代表是 ErrorContext。

ErrorContext 是线程级别的的单例，每个线程中有一个此对象的单例，用于记录该线程的执行环境的错误信息。

### [xml 映射文件select、insert、update、delete ，还有哪些标签？](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#xml-%E6%98%A0%E5%B0%84%E6%96%87%E4%BB%B6%E4%B8%AD-%E9%99%A4%E4%BA%86%E5%B8%B8%E8%A7%81%E7%9A%84-select%E3%80%81insert%E3%80%81update%E3%80%81delete-%E6%A0%87%E7%AD%BE%E4%B9%8B%E5%A4%96-%E8%BF%98%E6%9C%89%E5%93%AA%E4%BA%9B%E6%A0%87%E7%AD%BE)

`<resultMap>`、 `<parameterMap>`、 `<sql>`、 `<include>`、 `<selectKey>` ，加上动态 sql 的 9 个标签， `trim|where|set|foreach|if|choose|when|otherwise|bind` 等，其中 `<sql>` 为 sql 片段标签，通过 `<include>` 标签引入 sql 片段， `<selectKey>` 为不支持自增的主键生成策略标签。

### [Dao 接口的工作原理是什么？Dao 接口里的方法，参数不同时，方法能重载吗？](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#dao-%E6%8E%A5%E5%8F%A3%E7%9A%84%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86%E6%98%AF%E4%BB%80%E4%B9%88-dao-%E6%8E%A5%E5%8F%A3%E9%87%8C%E7%9A%84%E6%96%B9%E6%B3%95-%E5%8F%82%E6%95%B0%E4%B8%8D%E5%90%8C%E6%97%B6-%E6%96%B9%E6%B3%95%E8%83%BD%E9%87%8D%E8%BD%BD%E5%90%97)

最佳实践中，通常一个 xml 映射文件，都会写一个 Dao 接口与之对应。Dao 接口就是人们常说的 `Mapper` 接口，接口的全限名，就是映射文件中的 namespace 的值，接口的方法名，就是映射文件中 `MappedStatement` 的 id 值，接口方法内的参数，就是传递给 sql 的参数。 `Mapper` 接口是没有实现类的，当调用接口方法时，接口全限名+方法名拼接字符串作为 key 值，可唯一定位一个 `MappedStatement` ，举例：`com.mybatis3.mappers. StudentDao.findStudentById` ，可以唯一找到 namespace 为 `com.mybatis3.mappers. StudentDao` 下面 `id = findStudentById` 的 `MappedStatement` 。在 MyBatis 中，每一个 `<select>`、 `<insert>`、 `<update>`、 `<delete>` 标签，都会被解析为一个 `MappedStatement` 对象。


**Mybatis 的 Dao 接口可以有多个重载方法，但是多个接口对应的映射必须只有一个，否则启动会报错。**

Dao 接口的工作原理是 JDK 动态代理，MyBatis 运行时会使用 JDK 动态代理为 Dao 接口生成代理 proxy 对象，代理对象 proxy 会拦截接口方法，转而执行 `MappedStatement` 所代表的 sql，然后将 sql 执行结果返回。

**补充**：

Dao 接口方法可以重载，但是需要满足以下条件：

1. 仅有一个无参方法和一个有参方法
2. 多个有参方法时，参数数量必须一致。且使用相同的 `@Param` ，或者使用 `param1` 这种

### [MyBatis 进行分页？分页插件的原理](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#mybatis-%E6%98%AF%E5%A6%82%E4%BD%95%E8%BF%9B%E8%A1%8C%E5%88%86%E9%A1%B5%E7%9A%84-%E5%88%86%E9%A1%B5%E6%8F%92%E4%BB%B6%E7%9A%84%E5%8E%9F%E7%90%86%E6%98%AF%E4%BB%80%E4%B9%88)

**(1)** MyBatis 使用 RowBounds 对象进行分页，它是针对 ResultSet 结果集执行的内存分页，而非物理分页；**(2)** 可以在 sql 内直接书写带有物理分页的参数来完成物理分页功能，**(3)** 也可以使用分页插件来完成物理分页。

分页插件的基本原理是使用 MyBatis 提供的插件接口，实现自定义插件，在插件的拦截方法内拦截待执行的 sql，然后重写 sql，根据 dialect 方言，添加对应的物理分页语句和物理分页参数。

举例：`select _ from student` ，拦截 sql 后重写为：`select t._ from （select \* from student）t limit 0，10`

### [简述 MyBatis 的插件运行原理，以及如何编写一个插件](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#%E7%AE%80%E8%BF%B0-mybatis-%E7%9A%84%E6%8F%92%E4%BB%B6%E8%BF%90%E8%A1%8C%E5%8E%9F%E7%90%86-%E4%BB%A5%E5%8F%8A%E5%A6%82%E4%BD%95%E7%BC%96%E5%86%99%E4%B8%80%E4%B8%AA%E6%8F%92%E4%BB%B6)

### [MyBatis 执行批量插入，能返回数据库主键列表](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#mybatis-%E6%89%A7%E8%A1%8C%E6%89%B9%E9%87%8F%E6%8F%92%E5%85%A5-%E8%83%BD%E8%BF%94%E5%9B%9E%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%BB%E9%94%AE%E5%88%97%E8%A1%A8%E5%90%97)

### [MyBatis 动态 sql ](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#mybatis-%E5%8A%A8%E6%80%81-sql-%E6%98%AF%E5%81%9A%E4%BB%80%E4%B9%88%E7%9A%84-%E9%83%BD%E6%9C%89%E5%93%AA%E4%BA%9B%E5%8A%A8%E6%80%81-sql-%E8%83%BD%E7%AE%80%E8%BF%B0%E4%B8%80%E4%B8%8B%E5%8A%A8%E6%80%81-sql-%E7%9A%84%E6%89%A7%E8%A1%8C%E5%8E%9F%E7%90%86%E4%B8%8D)
动态 sql 可以让我们在 xml 映射文件内，以标签的形式编写动态 sql，完成逻辑判断和动态拼接 sql 的功能。其执行原理为，使用 OGNL 从 sql 参数对象中计算表达式的值，根据表达式的值动态拼接 sql，以此来完成动态 sql 的功能。

### [MyBatis将sql执行结果封装为目标对象,都有哪些映射形式？](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#mybatis-%E6%98%AF%E5%A6%82%E4%BD%95%E5%B0%86-sql-%E6%89%A7%E8%A1%8C%E7%BB%93%E6%9E%9C%E5%B0%81%E8%A3%85%E4%B8%BA%E7%9B%AE%E6%A0%87%E5%AF%B9%E8%B1%A1%E5%B9%B6%E8%BF%94%E5%9B%9E%E7%9A%84-%E9%83%BD%E6%9C%89%E5%93%AA%E4%BA%9B%E6%98%A0%E5%B0%84%E5%BD%A2%E5%BC%8F)

第一种是使用 `<resultMap>` 标签，逐一定义列名和对象属性名之间的映射关系。第二种是使用 sql 列的别名功能，将列别名书写为对象属性名，比如 T_NAME AS NAME，对象属性名一般是 name，小写，但是列名不区分大小写，MyBatis 会忽略列名大小写，智能找到与之对应对象属性名，你甚至可以写成 T_NAME AS NaMe，MyBatis 一样可以正常工作。

有了列名与属性名的映射关系后，MyBatis 通过反射创建对象，同时使用反射给对象的属性逐一赋值并返回，那些找不到映射关系的属性，是无法完成赋值的。

### [MyBatis 能执行一对一、一对多的关联查询吗？都有哪些实现方式，以及它们之间的区别](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#mybatis-%E8%83%BD%E6%89%A7%E8%A1%8C%E4%B8%80%E5%AF%B9%E4%B8%80%E3%80%81%E4%B8%80%E5%AF%B9%E5%A4%9A%E7%9A%84%E5%85%B3%E8%81%94%E6%9F%A5%E8%AF%A2%E5%90%97-%E9%83%BD%E6%9C%89%E5%93%AA%E4%BA%9B%E5%AE%9E%E7%8E%B0%E6%96%B9%E5%BC%8F-%E4%BB%A5%E5%8F%8A%E5%AE%83%E4%BB%AC%E4%B9%8B%E9%97%B4%E7%9A%84%E5%8C%BA%E5%88%AB)

- 不仅可以执行一对一、一对多的关联查询，还可以执行多对一，多对多的关联查询，多对一查询，其实就是一对一查询，只需要把 `selectOne()` 修改为 `selectList()` 即可；多对多查询，其实就是一对多查询，只需要把 `selectOne()` 修改为 `selectList()` 即可。

- 关联对象查询，有两种实现方式，一种是单独发送一个 sql 去查询关联对象，赋给主对象，然后返回主对象。另一种是使用嵌套查询，嵌套查询的含义为使用 join 查询，一部分列是 A 对象的属性值，另外一部分列是关联对象 B 的属性值，好处是只发一个 sql 查询，就可以把主对象和其关联对象查出来。

### [MyBatis 是否支持延迟加载？如果支持，它的实现原理是什么？](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#mybatis-%E6%98%AF%E5%90%A6%E6%94%AF%E6%8C%81%E5%BB%B6%E8%BF%9F%E5%8A%A0%E8%BD%BD-%E5%A6%82%E6%9E%9C%E6%94%AF%E6%8C%81-%E5%AE%83%E7%9A%84%E5%AE%9E%E7%8E%B0%E5%8E%9F%E7%90%86%E6%98%AF%E4%BB%80%E4%B9%88)

### [MyBatis 的 xml 映射文件中，不同的 xml 映射文件，id 是否可以重复？](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#mybatis-%E7%9A%84-xml-%E6%98%A0%E5%B0%84%E6%96%87%E4%BB%B6%E4%B8%AD-%E4%B8%8D%E5%90%8C%E7%9A%84-xml-%E6%98%A0%E5%B0%84%E6%96%87%E4%BB%B6-id-%E6%98%AF%E5%90%A6%E5%8F%AF%E4%BB%A5%E9%87%8D%E5%A4%8D)

### MyBatis执行批处理
使用 `BatchExecutor` 完成批处理。

### Executor 执行器 区别

- **`SimpleExecutor`：** 每执行一次 update 或 select，就开启一个 Statement 对象，用完立刻关闭 Statement 对象。
- **`ReuseExecutor`：** 执行 update 或 select，以 sql 作为 key 查找 Statement 对象，存在就使用，不存在就创建，用完后，不关闭 Statement 对象，而是放置于 Map<String, Statement>内，供下一次使用。简言之，就是重复使用 Statement 对象。
- **`BatchExecutor`**：执行 update（没有 select，JDBC 批处理不支持 select），将所有 sql 都添加到批处理中（addBatch()），等待统一执行（executeBatch()），它缓存了多个 Statement 对象，每个 Statement 对象都是 addBatch()完毕后，等待逐一执行 executeBatch()批处理。与 JDBC 批处理相同。

作用范围：`Executor` 的这些特点，都严格限制在 SqlSession 生命周期范围内。

### 指定使用Executor 执行器
在 MyBatis 配置文件中，可以指定默认的 `ExecutorType` 执行器类型，也可以手动给 `DefaultSqlSessionFactory` 的创建 SqlSession 的方法传递 `ExecutorType` 类型参数。

### 是否可以映射 Enum 枚举类

答：MyBatis 可以映射枚举类，不单可以映射枚举类，MyBatis 可以映射任何对象到表的一列上。映射方式为自定义一个 `TypeHandler` ，实现 `TypeHandler` 的 `setParameter()` 和 `getResult()` 接口方法。 `TypeHandler` 有两个作用：

- 一是完成从 javaType 至 jdbcType 的转换；
- 二是完成 jdbcType 至 javaType 的转换，体现为 `setParameter()` 和 `getResult()` 两个方法，分别代表设置 sql 问号占位符参数和获取列查询结果。

### [MyBatis 映射文件中，如果 A 标签通过 include 引用了 B 标签的内容，请问，B 标签能否定义在 A 标签的后面，还是说必须定义在 A 标签的前面？](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#mybatis-%E6%98%A0%E5%B0%84%E6%96%87%E4%BB%B6%E4%B8%AD-%E5%A6%82%E6%9E%9C-a-%E6%A0%87%E7%AD%BE%E9%80%9A%E8%BF%87-include-%E5%BC%95%E7%94%A8%E4%BA%86-b-%E6%A0%87%E7%AD%BE%E7%9A%84%E5%86%85%E5%AE%B9-%E8%AF%B7%E9%97%AE-b-%E6%A0%87%E7%AD%BE%E8%83%BD%E5%90%A6%E5%AE%9A%E4%B9%89%E5%9C%A8-a-%E6%A0%87%E7%AD%BE%E7%9A%84%E5%90%8E%E9%9D%A2-%E8%BF%98%E6%98%AF%E8%AF%B4%E5%BF%85%E9%A1%BB%E5%AE%9A%E4%B9%89%E5%9C%A8-a-%E6%A0%87%E7%AD%BE%E7%9A%84%E5%89%8D%E9%9D%A2)

### [简述 MyBatis 的 xml 映射文件和 MyBatis 内部数据结构之间的映射关系？](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#%E7%AE%80%E8%BF%B0-mybatis-%E7%9A%84-xml-%E6%98%A0%E5%B0%84%E6%96%87%E4%BB%B6%E5%92%8C-mybatis-%E5%86%85%E9%83%A8%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B9%8B%E9%97%B4%E7%9A%84%E6%98%A0%E5%B0%84%E5%85%B3%E7%B3%BB)

### [为什么说 MyBatis 是半自动 ORM 映射工具？它与全自动的区别在哪里？](https://javaguide.cn/system-design/framework/mybatis/mybatis-interview.html#%E4%B8%BA%E4%BB%80%E4%B9%88%E8%AF%B4-mybatis-%E6%98%AF%E5%8D%8A%E8%87%AA%E5%8A%A8-orm-%E6%98%A0%E5%B0%84%E5%B7%A5%E5%85%B7-%E5%AE%83%E4%B8%8E%E5%85%A8%E8%87%AA%E5%8A%A8%E7%9A%84%E5%8C%BA%E5%88%AB%E5%9C%A8%E5%93%AA%E9%87%8C)