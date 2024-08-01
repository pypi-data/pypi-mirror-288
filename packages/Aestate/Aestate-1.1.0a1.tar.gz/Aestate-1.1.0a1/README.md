<p align="center">
<img width="40%" src="https://gitee.com/aecode/aestate/raw/dev/resource/logo.png"/>
</p>
<h1 align="center">Aestate —— 多样化数据库查询</h1>
<p align="center">
  <a href='https://gitee.com/aecode/aestate/stargazers'>
    <img src='https://svg.hamm.cn/gitee.svg?user=aecode&project=aestate&type=star' alt='star'/>
  </a>
<img src='https://svg.hamm.cn/gitee.svg?user=aecode&project=aestate&type=language' alt='star'/>
<img src='https://svg.hamm.cn/badge.svg?key=Python&value=>=3.6'/>

  <a href="https://doc.cacode.ren">
    <img src='https://svg.hamm.cn/badge.svg?key=Documentation&value=yes'/>
  </a>
  <a href="https://gitee.com/aecode/summer-python/blob/main/LICENSE">
    <img src='https://svg.hamm.cn/gitee.svg?user=aecode&project=aestate&type=license' alt='star'/>
  </a>
</p>

> qq群：[909044439 （Aestate Framework）](https://jq.qq.com/?_wv=1027&k=EK7YEXmh)  
> 开源示例项目：[gitee/aestate-example](https://gitee.com/canotf/aestate-example)（旧版本）

# 介绍

> 当前测试通过数据库有(通过测试并不表示已经适配,内置字段除mysql以外任然需要自主编写):

- MySql8.0
- Sqlserver2019
- PostgreSQL 13.3

`Aestate Framework` 是一款基于`Python`语言开发的`ORM`框架， 你可以使用多种方式去实现基于对象方式的查询.

也就是相对于Java语言的Mybatis-Plus

比如使用类似`Django`的模式去使用：```modelClass.orm.filter(*args, **kwargs)```

或者SQLAlchemy的方式：```find().where(**kwargs).group_by(*args)```

或者像`Java`的`Hibernate`一样：

```Python
@SelectAbst()
def find_all_F_where_id_in_and_name_like_order_by_id(self, **kwargs) -> list: ...


@Select("SELECT * FROM demo WHERE id=#{id} AND name=#{name}")
def find_all_where_id(self, id, name): ...
```

或者像`Java`的`Mybatis`使用xml

```xml
<?xml version="1.0"?>
<aestate xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="aestate  https://gitee.com/aecode/aestate-xml/blob/main/v1/tags.xsd"
         xmlns="aestate">
    <template id="templateField">
        id,name,password,create_time,update_time
        <description>测试模板</description>
    </template>
    <resultMap id="resultMapLeftJoin" type="testOpera.operas.table.demoModels.Demo">
        <result column="d1_id" properties="id"/>
        <result column="d1_name" properties="name"/>
        <result column="d1_password" properties="password"/>
        <foreign ref="demoJoin" single="false">
        </foreign>
    </resultMap>
    <select id="findAllById" resultMap="resultMapLeftJoin">
        SELECT
        <!-- 导入查询的字段 -->
        <!--            <include from="templateField"/>-->
        <include from="tempSymbol"/>
        FROM demo as d1 LEFT JOIN demo as d2 ON d2.id = d1.id WHERE d1.id >
        <switch field="id">
            <case value="10">10</case>
            <case value="5">5</case>
            <default>#{id}</default>
        </switch>
        <if test="#{id}&gt;=20">AND d2.id > 20</if>
        <else>AND d2.id > 10</else>
        LIMIT 2
    </select>
    <!-- insert在最顶上，因为普遍代码量少 -->
    <insert id="insertTest" last="False">
        INSERT INTO `demo`.`demo` (`name`, `password`) VALUES (#{name}, #{password})
    </insert>
    <!-- update在中间，改动最频繁 -->
    <update id="updateTest" last="False">
        UPDATE `demo`.`demo` SET `name` = #{name}, `password` = #{password} WHERE `id` = ${id}
    </update>
    <!-- 删除在最底下，容易找到且代码普遍简单 -->
    <delete id="deleteTest">
        DELETE FROM `demo`.`demo` WHERE `id` = #{id}
        <description>
            删除指定id
        </description>
    </delete>
</aestate>
```

# 相对于其他库有什么区别？

- 首先**Aestate**是基于Django、SQLAlchemy、Mybatis、Mybatis-Plus、SpringJPA整合起来的一个数据库支持库，
  融合了这么多第三方库首先一点就是他的操作方式是多种多样的。目前已有六种操作方法，
  也就是Django模式、SQLAlchemy模式、xml模式、Mybatis-Plus模式，注解模式，原生模式。

- 其次就是在兼容性方面，由于这个世界上的数据库种类太多了没办法做到统一， **Aestate**保留了对其他小众数据库的实现接口，尽可能多兼容数据库。

- 数据库表方面，Django是会生成数据django自己系统内部的表，在迁移的时候呢如果做错一步可能对于新手
  来讲后面的修复操作是极其难的，也未必能够在短时间内定位问题并修复。**Aestate**为了解决这个问题，将make
  和手动建表尽可能的兼容，不会生成额外的表和数据，也不会捆绑某个特定系统，将pojo/model复制出来可以直接为下一个项目使用。

- ~~缓存方面参考了Mybatis的实现方法并略微修改，**Aestate**有两个内存管理模块，用于保证数据的完整性，
  当一些特别大的数据占满缓存时，**Aestate**
  会尽量多的去分配内存保证数据完整性，除外才会去管理内存（不建议操作大于系统内存2/10的数据）。**Aestate**
  有弹性内存管理方式，会根据系统的执行自动调整缓存大小，尽可能的加快运行速度，减少对数据库的连接次数。~~（最新1.0.9已删除缓存策略）

- 自带日志和美化，不需要下载其他插件就可以把日志变色，自动保存日志，这个功能对于爱美的大兄弟简直就 是神仙般的存在（当然也可能只有我喜欢装逼）


- 还有很多......

> windows控制台日志乱码解决办法：下载 [ansicon](https://github.com/adoxa/ansicon/releases) ,执行命令：

```shell
ansicon -i
ansicon -l
```

# 关于教程和文档地址

文档已经迁移到免费托管平台：http://aestate.angid.eu.org，文档将会逐步在gitee更新

> csdn: [AECODE](https://blog.csdn.net/qq_43059459)  
> OSCHINA: [CACode](https://my.oschina.net/u/4841054)  
> bilibili大学堂: [你在写臭虫?](https://space.bilibili.com/371089110)  
> 官网域名: [cacode.ren](https://cacode.ren)（迁移到腾讯云没备案）  
> 文档官网域名: [~~doc.cacode.ren~~](https://doc.cacode.ren)
> &nbsp;[http://aestate.angid.eu.org](http://aestate.angid.eu.org)  
> Gitee官方: [https://aecode.gitee.io/aestate-doc](https://aecode.gitee.io/aestate-doc)  
> 项目体系结构: [aecode.gitee.io/aestate](https://aecode.gitee.io/aestate/)

# 先决条件

> Python >=3.6
> 教程文档地址：~~http://doc.cacode.ren~~&nbsp;http://aestate.angid.eu.org

# 版本说明

基础需要2.7以上的python版本，对于只需要执行sql可以使用2.7以上（不建议）

最优的办法是使用3.6以上，可以使用绝大部分功能

由于1.0.7增加异步方法，需要异步执行的小伙伴可以使用python>=3.7.10以上版本

# 安装

```shell
pip install aestate

conda install aestate 
```

# 我是新手，怎么快速入门呢？

你可以前往[https://doc.cacode.ren](https://doc.cacode.ren)跟着官方文档入门  
也可以在B站 [你在写臭虫](https://space.bilibili.com/371089110) 看视频学
专治疑难杂症，请前往csdn查看官方解决方案: [Aecode的csdn.net](https://blog.csdn.net/qq_43059459)

# 操作方式太多了一下子学不会怎么办？

**Aestate**有五种方式，不是非要全部都会，我当时写的时候只是为了把很多语言的操作方式用Python实现，然后让其他语言转Python的开发者能够找到熟悉的感觉，例如

1. Java专业户：用xml、方法名和注解
2. Python专业户：用Django模式和SQLAlchemy模式
3. 纯萌新：老老实实写SQL，先把基础练好

更多示例项目请前往
> [👉 Go to canotf`s homepage on Gitee 👈](https://gitee.com/canotf)

# 鸣谢

Cpython  
DBPool  
Simplejson  
Gitee

# 感谢捐献

<a href="https://gitee.com/spacexzm">
<img alt="Spacexzm" width="49%" src="https://svg.hamm.cn/gitee-user.svg?user=spacexzm"/>
</a>
<a href="https://gitee.com/canotf">
<img alt="Canotf" width="49%" src="https://svg.hamm.cn/gitee-user.svg?user=canotf"/>
</a>
<a href="https://gitee.com/potuo">
<img alt="Potuo" width="49%" src="https://svg.hamm.cn/gitee-user.svg?user=potuo"/>
</a>
<a href="https://gitee.com/zxiaosi">
<img alt="Zxiaosi" width="49%" src="https://svg.hamm.cn/gitee-user.svg?user=zxiaosi"/>
</a>
<a href="https://gitee.com/xierkz">
<img alt="Xierkz" width="49%" src="https://svg.hamm.cn/gitee-user.svg?user=xierkz"/>
</a>