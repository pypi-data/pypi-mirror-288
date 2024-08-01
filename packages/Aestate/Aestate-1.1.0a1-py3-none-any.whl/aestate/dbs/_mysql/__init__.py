from datetime import datetime

from typing import List, Tuple

from aestate.dbs import base
from aestate.exception import FieldNotExist
from aestate.dbs._mysql import tag
from aestate.util import others
from aestate.util.Log import ALog
import threading
from aestate.work.Modes import Singleton, EX_MODEL


class ParseUtil:

    def parse_main(self, *args, to_str=False, symbol='%s', left='`', right='`', **kwargs):
        """
            解析属性:
                将属性格式设置为:['`a`,','`b`,','`c`']
            :param to_str:是否转成str格式
            :param args:参数
            :param symbol:分隔符语法
            :param left:分隔符语法
            :param right:分隔符语法
            :return:
        """

        is_field = kwargs['is_field'] if 'is_field' in kwargs.keys() else False

        fields = []
        for value in args:
            value = others.conversion_types(value)
            if to_str:
                if is_field:
                    fields.append(f'{left}{symbol}{right},' % (str(value)))
                else:
                    fields.append(f'{symbol},' % (str(value)))
            else:
                fields.append(value if not ParseUtil.is_default(value) else None)
        if len(fields) != 0:
            fields[len(fields) - 1] = fields[len(fields) - 1].replace(',', '')
            field_str = ''
            # 转成字符串的话 "`field1`,`field2`,`field3`"
            if to_str:
                for field in fields:
                    field_str += field
                return field_str
            return fields
        else:
            return None

    def parse_key(self, *args, **kwargs):
        """
        如果 is_field=True `field` [field]


        解析键格式,如:
            INSERT INTO `demo` (这里的就是键) VALUES ('','','','');
        :param args:
        :return:
        """
        if 'is_field' not in kwargs.keys():
            kwargs['is_field'] = True
        fields = self.parse_main(*args, to_str=True, **kwargs)
        return fields

    def parse_update(self, pojo, key):
        f = pojo.sqlFields
        kes = [f.update_str, f.left_subscript, pojo.__table_name__, f.right_subscript, f.set_str]
        params = []
        for i in pojo.fields:
            if i != key and not pojo.getFields()[i].auto_time:
                kes.append(f'`{i}`=%s')
                kes.append(", ")
                if pojo.getFields()[i].update_auto_time:
                    params.append(datetime.now())
                else:
                    params.append(getattr(pojo, i))
        kes = kes[:-1]
        kes.append(f.where_str)
        kes.append(f'`{key}`=%s')
        params.append(getattr(pojo, key))
        sql = ''.join(kes)
        return sql, params

    def parse_remove(self, pojo, key):
        f = pojo.sqlFields
        kes = [f.delete_str, f.from_str, f.left_subscript, pojo.__table_name__, f.right_subscript, f.where_str]
        params = []
        kes.append(f'`{key}`=%s')
        params.append(getattr(pojo, key))
        sql = ''.join(kes)
        return sql, params

    def parse_value(self, *args, **kwargs):
        """
        解析值格式,如:
            INSERT INTO `demo` (`index`, `title`, `selects`, `success`) VALUES (这里的就是值);
        :param args:
        :return:
        """
        values = self.parse_main(*args, **kwargs)
        return values

    def parse_insert(self, keys, values, __table_name__, insert_str, values_str, symbol='%s',
                     sql_format='%s %s (%s)%s(%s)'):
        """
        实现此方法可自定义sql生成模式

        keys:包含了所有需要解析的字段名
        values:包含了所有需要用到的字段的值
        __table_name__:表名称
        insert_str:insert的字符串
        values_str:values字符串
        symbol:格式化方式，以`%s`作为匿名符号
        """
        fields = self.parse_key(*keys)
        values = self.parse_value(*values)
        # 分析需要几个隐藏值
        hides_value = [f'{symbol},' for i in range(len(values))]
        # 去除末尾的逗号
        end = hides_value[len(hides_value) - 1]
        hides_value[len(hides_value) - 1] = end[0: len(end) - 1]
        # 得到最后隐藏符号的字符串表达格式
        value = ''.join(hides_value)
        sql = sql_format % (
            insert_str,
            str(__table_name__), fields, values_str, value
        )

        kes = {'sql': sql}
        args = []
        [args.append(i) for i in values]
        kes['params'] = args
        return kes

    def parse_insert_pojo(self, pojo, __table_name__, insert_str, values_str):
        """
        解析插入语句

        INSERT INTO `__table_name__`(`title`,'selects') VALUE ('','')

        :param pojo:POJO对象
        :param __table_name__:表名
        :param insert_str:insert的sql方言
        :param values_str:values的sql方言
        :return:
        """
        # 得到所有的键
        ParseUtil.fieldExist(pojo, 'fields', raise_exception=True)
        # 在得到值之后解析是否为空并删除为空的值和对应的字段
        cp_value = []
        # 复制新的一张字段信息
        keys_copy = []

        keys_c, cp_v = ParseUtil.parse_pojo(pojo)
        keys_copy += keys_c
        cp_value += cp_v

        return self.parse_insert(keys_copy, cp_value, __table_name__, insert_str=insert_str,
                                 values_str=values_str)

    @staticmethod
    def parse_pojo(pojo) -> Tuple[list, list]:
        keys = pojo.fields
        # 在得到值之后解析是否为空并删除为空的值和对应的字段
        cp_value = []
        # 复制新的一张字段信息
        keys_copy = []
        values = [getattr(pojo, v) for v in keys]
        for i, j in enumerate(values):
            if j is not None and not ParseUtil.is_default(j):
                keys_copy.append(keys[i])
                cp_value.append(j)

        return keys_copy, cp_value

    @staticmethod
    def parse_obj(data: dict, instance: object) -> object:
        """
        将数据解析成对象
        注意事项:
            数据来源必须是DbUtil下查询出来的
        :param data:单行数据
        :param instance:参与解析的对象
        :return:POJO对象
        """
        # 深度复制对象
        part_obj = instance.copy()
        for key, value in data.items():
            setattr(part_obj, key, value)
        return part_obj

    @staticmethod
    def find_last_id(**kwargs):
        """

        遵循规则：

            内部>配置文件

        是否包含返回最后一行ID的配置

        只存在于更新操做的方法内，如：

            insert,

            update,

            delete

         Attributes:

             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'last_id' not in kwargs.keys():
            c_dict = conf_obj.get_dict()
            if 'last_id' in c_dict.keys():
                kwargs['last_id'] = c_dict['last_id']
            else:
                kwargs['last_id'] = False
        return kwargs

    @staticmethod
    def find_print_sql(**kwargs):
        """
        遵循规则：
            内部>配置文件

        是否包含打印sql的配置

        存在于所有数据库操做

        Attributes:
             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'print_sql' not in kwargs.keys():
            c_dict = conf_obj.get_dict()
            if 'print_sql' in c_dict.keys():
                kwargs['print_sql'] = c_dict['print_sql']
            else:
                kwargs['print_sql'] = False
        return kwargs

    @staticmethod
    def case_name(text, rep_text='_', lower=True, upper=False):
        """
        将驼峰文本改为使用指定符号分割的字符串表达形式并全部小写
        :param text:需要替换的文本
        :param rep_text:在大写文本后面追加的字符串
        :param lower:是否需要全部小写
        :param upper:是否需要全部大写
        """
        lst = []
        for index, char in enumerate(text):
            if char.isupper() and index != 0:
                lst.append(rep_text)
            lst.append(char)
        # 替换名称
        if lower:
            return "".join(lst).lower()
        elif upper:
            return "".join(lst).upper()
        else:
            return "".join(lst)

    @staticmethod
    def is_default(__val):
        """
        是否等于默认值
        """
        try:
            t_v = __val.__class__.__base__
            if t_v in [tag.Template, tag.baseTag]:
                return __val.default is None
        except SyntaxError:
            return False

    @staticmethod
    def set_field(obj, key, value):
        """
        当对象没有这个字段时，为对象设置一个字段

        为了方便提高拓展性可解耦，框架内部务必使用此

        方法或者set_field_compulsory()为操作管理类提供对象

        """
        if not hasattr(obj, key):
            setattr(obj, key, value)

    @staticmethod
    def set_field_compulsory(obj, key: str, data: dict, val: object) -> None:
        """
        如果键存在于data中，为obj插入该值，反之插入val
        """
        if key in data.keys():
            setattr(obj, key, data[key])
        else:
            setattr(obj, key, val)

    @staticmethod
    def fieldExist(obj: object, field: str, el=None, raise_exception=False) -> object:
        """
        在对象中获取一个字段的值,如果这个字段不存在,则将值设置为`el`
        """
        if isinstance(obj, dict):
            if field in obj.keys():
                return obj[field]
            else:
                if raise_exception:
                    raise ALog.log_error(
                        msg=f'the key of `{field}` cannot be found in the `{obj.__class__.__name__}`',
                        obj=FieldNotExist,
                        raise_exception=True)
                else:
                    return el
        else:
            if hasattr(obj, field):
                return getattr(obj, field)
            else:
                if raise_exception:
                    raise ALog.log_error(
                        msg=f'the key of `{field}` cannot be found in the `{obj.__class__.__name__}`',
                        obj=FieldNotExist,
                        raise_exception=True)
                else:
                    return el

    @staticmethod
    def parse_pojo_many(pojo_many: list) -> List[tuple]:

        # 在得到值之后解析是否为空并删除为空的值和对应的字段
        cp_value = []
        for pojo in pojo_many:
            keys_c, cp_v = ParseUtil.parse_pojo(pojo)
            cp_value.append(tuple(cp_v))
        # 真实值
        return cp_value

    @staticmethod
    def insert_to_obj(obj, kwargs):
        for key, value in kwargs.items():
            ParseUtil.set_field_compulsory(obj=obj, key=key, data=kwargs, val=value)

    def get_pojo_sql(self, instance):
        """
        获取创建pojo对象的sql语句
        """
        fields = instance.getFields()
        print(fields)


# 所有常量以空格开头并且以空格结束
# 空格符
class Fields:
    """
    默认的数据库方言配置
    """

    _instance_lock = threading.RLock()

    @staticmethod
    def parse_field(key: str) -> str:
        return f' {key} '

    @property
    def left_subscript(self):
        """
        左角标
        """
        return '`'

    @property
    def space(self):
        """
        空格
        """
        return ' '

    @property
    def right_subscript(self):
        """
        右角标
        """
        return '`'

    @property
    def insert_str(self):
        """
        插入
        """
        return self.parse_field('INSERT INTO')

    @property
    def delete_str(self):
        """
        删除
        """
        return self.parse_field('DELETE')

    @property
    def update_str(self):
        """
        更新
        """
        return self.parse_field('UPDATE')

    @property
    def find_str(self):
        return self.parse_field('SELECT')

    @property
    def where_str(self):
        return self.parse_field('WHERE')

    @property
    def by_str(self):
        return self.parse_field('BY')

    @property
    def order_by_str(self):
        return self.parse_field('ORDER BY')

    @property
    def group_by_str(self):
        return self.parse_field('GROUP BY')

    @property
    def desc_str(self):
        return self.parse_field('DESC')

    @property
    def set_str(self):
        return self.parse_field('SET')

    @property
    def ander_str(self):
        return self.parse_field('AND')

    @property
    def limit_str(self):
        return self.parse_field('LIMIT')

    @property
    def from_str(self):
        return self.parse_field('FROM')

    @property
    def value_str(self):
        return self.parse_field('VALUE')

    @property
    def values_str(self):
        return self.parse_field('VALUES')

    @property
    def asses_str(self):
        return self.parse_field('AS')

    @property
    def left_par(self):
        return self.parse_field('(')

    @property
    def right_par(self):
        return self.parse_field(')')

    @property
    def comma(self):
        return self.parse_field(',')

    @property
    def eq(self):
        return self.parse_field('=')

    @property
    def on_str(self):
        return self.parse_field('on')

    @property
    def left_join_str(self):
        return self.parse_field('LEFT JOIN')

    @property
    def symbol(self):
        return '>> << == <= >= != - + / * %'.split(' ')

    def __new__(cls, *args, **kwargs):
        instance = Singleton.createObject(cls)
        return instance


class OperaBase(base.OperaBase):
    """
    mysql的基操
    """

    class Fields:
        # 表重命名
        RENAME = lambda x, y: f'rename table {x} to {y}'
        # 删除表
        DELETE_TABLE = lambda x: f'DROP TABLE IF EXISTS {x}'

    def extra(self, field) -> Tuple[bool, object]:
        """
        结构检查
        :param field:字段
        """
        target = None

        for i in self.R:
            if field.name == i['Field']:
                target = i
                break

        if target is None:
            return False, f"Check failed:{field.name} not exists"
        self.R.remove(target)

        field_type = field.t_type \
            if field.length is None else \
            f"{field.t_type}({field.length})" \
                if field.d_point is None else \
                f"{field.t_type}({field.length},{field.d_point})"
        field_null = "YES" if field.is_null else "NO"

        if target["Type"] != field_type:
            return False, f"Check failed(Type):{field.name}:{field_type},new:{target['Type']}"

        if target["Null"] != field_null:
            return False, f"Check failed(Null):{field.name}:{field_null},new:{target['Null']}"
        return True, ""

    def check(self) -> bool:
        self.R = self.instance.execute_sql(f"DESC `{self.instance.get_tb_name()}`")
        flag = True
        for k, v in self.instance.getFields().items():
            f = self.extra(v)
            if not f[0]:
                flag = False
                ALog.log_error(f[1], obj=self, task_name="Check")

        if len(self.R) != 0:
            ALog.log_error(f"Extra field:{self.R}", obj=self, task_name="Check")
            flag = False
        return flag

    def create(self, replace=False):
        """
        创建表
        :param replace:是否替换
        :return:
        """
        PRIMARYKEY = None
        FIELDS = []
        default_parse = lambda x: "AUTO_INCREMENT" \
            if x.autoField else 'DEFAULT CURRENT_TIMESTAMP' \
            if x.auto_time else 'DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP' \
            if x.update_auto_time else f"CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '{x.default}'" \
            if isinstance(x.default, str) else f"DEFAULT '{x.default}'" \
            if isinstance(x.default, int) else ""

        type_parse = lambda x: x.t_type \
            if x.length is None else "%s(%s,%s)" % (x.t_type, x.length, x.d_point) \
            if x.d_point is not None and x.length is not None else "%s(%s)" % (x.t_type, x.length) \
            if x.length is not None else x.t_type
        for k, v in self.instance._fields.items():
            FIELDS.append(
                "`%s` %s %s %s," %
                (
                    v.name,
                    type_parse(v),
                    default_parse(v),
                    'NULL' if v.is_null else 'NOT NULL'
                )
            )
            if v.primary_key:
                PRIMARYKEY = v.name

        sql = "CREATE TABLE IF NOT EXISTS `%s` ( %s  %s) ENGINE=InnoDB DEFAULT CHARSET=utf8;" % \
              (self.instance.get_tb_name(), ''.join(FIELDS), "PRIMARY KEY (`%s`)" % PRIMARYKEY)
        # 如果替换的话，就直接删除表
        if replace:
            ALog.log("DROP TABLE IF EXISTS `%s`" % self.instance.get_tb_name())
            self.instance.execute_sql(sql, mode=EX_MODEL.UPDATE)

        ALog.log(sql)
        r = self.instance.execute_sql(sql, mode=EX_MODEL.UPDATE)
        return r
