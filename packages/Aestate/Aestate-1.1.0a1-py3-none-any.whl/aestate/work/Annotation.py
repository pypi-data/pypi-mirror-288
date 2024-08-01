import re

from .AopContainer import AopModelObject
from .Modes import EX_MODEL
from .Serialize import QuerySet
import os
import inspect

from .xmlhandler.nodes import ResultMapNode
from .xmlhandler.utils import AestateXml
from ..exception import TagAttributeError, TagHandlerError
from ..i18n import ExceptionI18n
from ..util.Log import ALog
from ..util.sqlOpera import TextUtil


def Table(name, msg="", **kwargs):
    """
    标注该类为一个表
    :param name:表的名称
    :param msg:表的描述
    :return:
    """

    def set_to_field(cls):
        setattr(cls, '__table_name__', name)
        setattr(cls, '__table_msg__', msg)
        for key, value in kwargs.items():
            setattr(cls, key, value)
        return cls

    return set_to_field


def Select(sql: str):
    """
    快捷的查询装饰器

    使用此装饰器,可以将大量重复代码继承到此装饰器内部实现

    使用方法:

        @Select(sql="SELECT * FROM demo_table WHERE t_id<=${不加密} AND t_msg like #{加密}")

    有两种符号可以作为sql的字段插入形式:

        ${字段}:这种方式是直接将文字插入进去,在面对sql注入时无法有效避免

        #{字段}:将字段使用%s过滤,能有效防止sql注入,但并非100%有效
            依靠的是你所使用的第三方库内置游标的:`mogrify`方法,请在使用前查看


    :param sql:执行的sql语句,需要加密的参数使用`%s`表示
    """

    def base_func(cls):
        def _wrapper_(*args, **kwargs):
            lines = list(args)
            obj = lines[0]

            # 查找参数
            sub_sql, new_args = TextUtil.replace_antlr(sql, **kwargs)

            result = obj.find_sql(sql=sub_sql, params=new_args)
            return QuerySet(obj, result)

        return _wrapper_

    return base_func


def SelectAbst():
    def mysql_rp(n, array, obj) -> str:
        _name = array[len(array) - 1] if len(array) > 0 else ""
        rule = {
            'F': 'FROM',
            'find': "SELECT",
            'where': 'WHERE',
            'eq': "= #{%s}" % _name,
            'lt': '< #{%s}' % _name,
            'gt': '> #{%s}' % _name,
            'le': '<= #{%s}' % _name,
            'ge': '>= #{%s}' % _name,
            'in': 'in #{%s}' % _name,
            'like': 'like #{%s}' % _name,
            'all': ','.join([obj.orm.ParseUtil.parse_key(f) for f in obj.fields]),
        }
        return rule[n] if n in rule.keys() else n

    def base_func(func):
        def _wrapper_(*args, **kwargs):
            lines = list(args)
            if len(lines) == 0 and hasattr(func, 'instance') and not func.instance:
                ALog.log_error(ExceptionI18n.tt(""))
            obj = lines[0]
            _name = func.__name__.split("_")
            S = []
            for i in _name:
                d = mysql_rp(i, S, obj)
                S.append(d if d != "FROM" else f"FROM {obj.__table_name__}")

            sql = ' '.join(S)

            # 查找参数
            sub_sql, new_args = TextUtil.replace_antlr(sql, **kwargs)

            result = obj.find_sql(sql=sub_sql, params=new_args)
            return QuerySet(obj, result)

        return _wrapper_

    return base_func


def AopModel(before=None, after=None,
             before_args=None, before_kwargs=None,
             after_args=None, after_kwargs=None):
    """

        AOP切面模式：
            依赖AopModel装饰器,再在方法上加入@AopModel即可切入编程


        优点:

            当使用@AopModel时,内部函数将会逐级调用回调函数,执行循序是:
                - func(*self.args, **self.kwargs)
                - func(*self.args)
                - func(**self.kwargs)
                - func()
            这将意味着,如果你的参数传入错误时,AopModel依旧会遵循原始方法所使用的规则,最令人大跌眼镜的使用方法就是:
<code>
                def Before(**kwargs):
                    print('Before:', kwargs)
                # 此处的Before方法未存在args参数,而使用@AopModel时却传入了args
                @AopModel(before=Before,before_args=(0,1,2), before_kwargs={'1': '1'})
                def find_title_and_selects(self, **kwargs):

                    print('function task', kwargs['uid'])

                    _r = self.orm.find().where(index="<<100").end()

                    print(_r)

                    return _r
</code>
            其中包含参数有:
                before:切入时需要执行的函数

                before_args:切入的参数
                    传入的列表或元组类型数据
                    如果是需要使用当前pojo中的内容时，传参格式为:(pojo.字段名)
                    可扩展格式，例如需要传入字典

                before_kwargs:切入的参数 -- 传入的字典数据

                after:切出前需要执行的参数

                after_args:切出的参数
                    传入的列表或元组类型数据
                    如果是需要使用当前pojo中的内容时，传参格式为:('self.字段名')
                    可扩展格式，例如需要传入字典:('self.dict.key')

                after_kwargs:切出的参数 -- 传入的字典数据


        执行流程:

            Before->original->After

        Before注意事项:

            使用该参数时，方法具有返回值概不做处理,需要返回值内容可使用`global`定义一个全局字段用于保存数值

            当无法解析或者解析失败时m将使用pass关键字忽略操作

        After注意事项:

            使用该参数时，必须搭配至少一个result=None的kwargs存在于方法的形参中,

            当original方法执行完成将把返回值固定使用result键值对注入到该函数中

            当无法解析或者解析失败时m将使用pass关键字忽略操作



        Attributes:

             before:切入时需要执行的函数

             after:切出前需要执行的参数

             before_args:切入的参数
                传入的列表或元组类型数据
                如果是需要使用当前pojo中的内容时，传参格式为:(pojo.字段名)
                可扩展格式，例如需要传入字典

             before_kwargs:切入的参数 -- 传入的字典数据

             after_args:切出的参数
                传入的列表或元组类型数据
                如果是需要使用当前pojo中的内容时，传参格式为:('self.字段名')
                可扩展格式，例如需要传入字典:('self.dict.key')

             after_kwargs:切出的参数 -- 传入的字典数据


            """
    # 得到对象组
    aop_obj = AopModelObject(before, after,
                             before_args, before_kwargs,
                             after_args, after_kwargs)

    def base_func(func):
        aop_obj.func = func

        def _wrapper_(*args, **kwargs):
            aop_obj.set_args(*args, **kwargs)
            return aop_obj.start()

        return _wrapper_

    return base_func


def ReadXml(filename):
    """读取xml"""

    def set_to_field(cls):
        file_path = inspect.getfile(cls)
        # 分割字符串得到当前路径
        file_path = '/'.join(re.split(r'[/|\\]', file_path)[:-1])
        path = os.path.join(file_path, filename)

        setattr(cls, '_xml_file', path)
        xml = AestateXml.read_file(path)
        setattr(cls, 'xNode', xml)
        setattr(cls, '_xml_file_name', os.path.basename(path))
        return cls

    return set_to_field


def Item(_id, d=False):
    """
    将xml的item节点映射到当前方法,对应的id字段为xml节点的id
    :param _id: 节点id
    :param d: 查询时返回原始数据
    """

    def replaceNextLine(sql):
        sql = str(sql).replace('\n', ' ')
        sql = str(sql).replace('  ', ' ')
        if '  ' in sql:
            return replaceNextLine(sql)
        else:
            return sql

    def base_func(cls):
        def _wrapper_(*args, **kwargs):
            lines = list(args)
            obj = lines[0]
            xml = obj.xNode

            xml_node = None
            # 增删改查的节点加起来得到所有操作节点
            node_list = xml.children['select'] \
                        + xml.children['insert'] \
                        + xml.children['update'] \
                        + xml.children['delete']
            # 从所有的可操作节点中寻找id符合的节点
            for v in node_list:
                if 'id' in v.attrs.keys() and v.attrs['id'].text == _id:
                    xml_node = v
                    break
            if xml_node is not None:
                xml_node.params = kwargs
                result_text_node = xml_node.text(obj)
            else:
                result_text_node = None
                ALog.log_error(
                    f"`{_id}` does not exist in the xml node.file:({obj._xml_file_name})", obj=TagAttributeError,
                    raise_exception=True)
            # 美化sql
            if result_text_node is None:
                ALog.log_error(
                    f"`The node did not return any sentences.file:({obj._xml_file_name})", obj=TagHandlerError,
                    raise_exception=True)
                return None
            run_sql = replaceNextLine(result_text_node.text)
            sub_sql, params = TextUtil.replace_antlr(run_sql, **kwargs)
            # 返回值ast
            if xml_node.node.tagName.lower() == 'select':
                result = obj.execute_sql(sql=sub_sql, params=params, mode=EX_MODEL.SELECT, **obj.__dict__)
                # 将返回的结果解析
                resultTree = ResultMapNode(obj, result_text_node, result)
                if d:
                    return result
                return resultTree.apply(xml.children['resultMap'])
            else:
                # 是否需要返回最后一行id，默认返回
                has_last_id = bool(result_text_node.expand_data['last']) \
                    if 'last' in result_text_node.expand_data.keys() else True

                result = obj.execute_sql(sql=sub_sql, params=params, mode=EX_MODEL.UPDATE,
                                         **{'last_id': has_last_id, **obj.__dict__})
                return result

        return _wrapper_

    return base_func


def JsonIgnore(*fields):
    def base_func(fn):
        def _wrapper_(*args, **kwargs):
            _self = args[0]
            _self.EXEC_FUNCTION = [*fields]
            return _self

        return _wrapper_

    return base_func
