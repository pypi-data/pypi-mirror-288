# -*- utf-8 -*-
import importlib
import re
from abc import ABC

from aestate.exception import NotFindTemplateError, TagAttributeError, TagHandlerError, XmlParseError
from aestate.i18n import ExceptionI18n
from aestate.util import others
from aestate.util.Log import ALog
from aestate.work.Serialize import QuerySet
from aestate.work.repository import Repository
from aestate.work.xmlhandler.XMLScriptBuilder import IfHandler
from aestate.work.xmlhandler.base import AestateNode


class AbstractNode(ABC):
    """抽象节点，所有节点的父类"""

    # 节点自身的操作

    def __init__(self, target_obj, params, aestate_xml_cls, root, value, XML_KEY, XML_IGNORE_NODES):
        self.target_obj = target_obj
        self.params = params
        self.aestate_xml_cls = aestate_xml_cls
        self.root = root
        self.node = value
        self.XML_KEY = XML_KEY
        self.XML_IGNORE_NODES = XML_IGNORE_NODES

    # 得到节点的值
    def apply(self, *args, **kwargs):
        ...

    def parseNode(self, texts: AestateNode, node):
        for root_index, root_value in enumerate(node.childNodes):
            if root_value.nodeName in self.XML_KEY.keys():
                obj = self.XML_KEY[root_value.nodeName](self.target_obj, self.params, self.aestate_xml_cls, self.root,
                                                        root_value, self.XML_KEY, self.XML_IGNORE_NODES)
                texts = obj.apply(texts=texts)
            elif root_value.nodeName in self.XML_IGNORE_NODES:
                try:
                    texts.add(node=root_value, index=root_index)
                except Exception as e:
                    ALog.log_error(
                        msg=''.join(e.args),
                        obj=e, LogObject=self.target_obj.log_obj, raise_exception=True)
            try:
                texts.extend(AestateNode(self.root, root_value))
            except Exception as e:
                ALog.log_error(
                    msg=''.join(e.args),
                    obj=e, LogObject=self.target_obj.log_obj, raise_exception=True)
        return texts


class SelectNode(AbstractNode):

    def apply(self, *args, **kwargs):
        # 取得已有的文本
        texts = kwargs['texts']
        axc_node = self.aestate_xml_cls(self.root, self.node, self.params)
        # 返回值类型
        resultType = axc_node.attrs['resultType']
        return self.parseNode(texts, self.node)


class UpdateNode(AbstractNode):
    class TempTextNode:
        def __init__(self, text):
            self.text = text

    def apply(self, *args, **kwargs):
        # 取得已有的文本
        texts = kwargs['texts']
        axc_node = self.aestate_xml_cls(self.root, self.node, self.params)
        # 返回值类型
        has_last_id = axc_node.attrs['last'] if 'last' in axc_node.attrs.keys() else self.TempTextNode('True')
        texts.expand_data['has_last_id'] = has_last_id.text == 'True'
        return self.parseNode(texts, self.node)


class IfNode(AbstractNode):

    def conditional_test(self, text, syntax_re_text):
        # 移除空集
        syntax_using = [x for x in syntax_re_text[0] if x != '']
        if len(syntax_using) == 2 or len(syntax_using) > 3:
            ALog.log_error(
                msg=ExceptionI18n.tt('xml_syntax_error') % text,
                obj=TagHandlerError, LogObject=self.target_obj.log_obj, raise_exception=True)

        # 左边的匹配字段名,这就意味着变量必须写在左边
        initial_field = syntax_using[0]
        symbol = syntax_using[1]
        value = syntax_using[2]

        rfield = re.findall('#{(.*?)}', initial_field)

        field = rfield[0] if len(rfield) > 0 and rfield[0] in self.params.keys() else initial_field
        # 让事件器来执行
        ifhandler = IfHandler(initial_field=initial_field, field=field, params=self.params, value=value,
                              symbol=symbol)

        return ifhandler.handleNode(self.target_obj)

    def signal_conditional_test(self, text, field):
        """单个判断值对否"""
        rfield = re.findall('#{(.*?)}', field)
        if len(rfield) == 1 and rfield[0] not in self.params.keys():
            # 这里理应等于false,但是由于存在不等号,所以当没有时他应该为!false,也就是true
            return True
        return not bool(self.params[rfield[0]])

    def apply(self, *args, **kwargs):
        texts = kwargs['texts']
        axc_node = self.aestate_xml_cls(self.root, self.node, self.params)
        if 'test' not in axc_node.attrs.keys():
            ALog.log_error(
                msg=ExceptionI18n.tt('if_tag_not_test'),
                obj=TagAttributeError, LogObject=self.target_obj.log_obj, raise_exception=True)
            return
        test_syntax = axc_node.attrs['test']
        # UPDATE: 1.0.6a2 增加!=
        tests = re.split('and|or|&&|\|\|', test_syntax.text)
        conditions = re.findall('(and|or|&&|\|\|)', test_syntax.text)
        if len(conditions) != len(tests) - 1:
            ALog.log_error(
                msg=ExceptionI18n.tt('xml_syntax_error') % test_syntax.text,
                obj=XmlParseError, LogObject=self.target_obj.log_obj, raise_exception=True)
        # UPDATE: 1.0.6a2 增加可以识别多个条件
        # 是否可以继续判断
        if_next = None
        for t in tests:
            success = False
            # 去除首尾空格寻找匹配的语法
            text = t.strip()
            # 一种是 字段-符号-值
            syntax_re_text = re.findall('(#\{.*?\})([>=|<=|==|<|>|!=]+)(.*)', text)
            # 一种是 符号-空格(可有可无)-字段
            signal_syntax_re_text = re.findall('!\s*(#\{.*?\})', text)
            if len(syntax_re_text) != 0:
                success = self.conditional_test(text, syntax_re_text)
            elif len(signal_syntax_re_text) == 1:
                success = self.signal_conditional_test(text[0], signal_syntax_re_text[0])
            else:
                # 缺少必要的test标签语法
                ALog.log_error(
                    msg=ExceptionI18n.tt('xml_syntax_error') % test_syntax.text,
                    obj=TagAttributeError, LogObject=self.target_obj.log_obj, raise_exception=True)

            if len(conditions) > 0:
                _and = re.search('and|&&', conditions[0])
                _or = re.search('or|\|\|', conditions[0])
                if if_next is None:
                    if_next = success
                    continue
                if _and:
                    if_next = if_next and success
                elif _or:
                    if_next = if_next or success
                else:
                    ALog.log_error(
                        msg=ExceptionI18n.tt('before_else_not_if'),
                        obj=TagHandlerError, LogObject=self.target_obj.log_obj, raise_exception=True)
                # 分割应该放在末尾,因为条件需要比判断的符号多一个索引
                conditions = conditions[1:]
            else:
                if_next = success
            # 如果已经是false
            if not if_next:
                break
        if if_next:
            texts = self.parseNode(texts, node=self.node)

        if IfHandler.checking_mark(self.node):
            # 设置为反的
            texts.expand_data['if_next'] = not if_next

        return texts


class ElseNode(AbstractNode):

    def apply(self, *args, **kwargs):
        texts = kwargs['texts']
        if 'if_next' not in texts.expand_data.keys():
            ALog.log_error(
                msg=ExceptionI18n.tt('before_else_not_if'),
                obj=TagHandlerError, LogObject=self.target_obj.log_obj, raise_exception=True)
        else:
            if_next = texts.expand_data['if_next']
            if not if_next:
                texts.expand_data.pop('if_next')
                return texts
            else:
                texts.expand_data.pop('if_next')
                return self.parseNode(texts, self.node)


class SwitchNode(AbstractNode):

    def apply(self, *args, **kwargs):
        texts = kwargs['texts']
        axc_node = self.aestate_xml_cls(self.root, self.node, self.params)
        field_name = axc_node.attrs['field'].text
        try:
            value = self.params[field_name]
        except KeyError as ke:
            ALog.log_error(
                msg=ExceptionI18n.tt('not_field_name') % field_name,
                obj=TagHandlerError, LogObject=self.target_obj.log_obj, raise_exception=True)
        case_nodes = axc_node.children['case']
        check_node = None
        for cn in case_nodes:
            if cn.attrs['value'].text == value:
                check_node = cn.node
                break
        if check_node is None:
            check_node = axc_node.children['default'][0].node
        texts = self.parseNode(texts, check_node)

        return texts


class IncludeNode(AbstractNode):

    def apply(self, *args, **kwargs):
        texts = kwargs['texts']
        axc_node = self.aestate_xml_cls(self.root, self.node, self.params)
        from_node_name = axc_node.attrs['from'].text
        sql_nodes = self.target_obj.xNode.children['sql']
        target_template = None
        for t in sql_nodes:
            if t.attrs['id'].text == from_node_name:
                target_template = t
                break
        if target_template is None:
            ALog.log_error(
                msg=ExceptionI18n.tt('not_from_node_name') % from_node_name,
                obj=NotFindTemplateError, LogObject=self.target_obj.log_obj, raise_exception=True)
        texts = self.parseNode(texts, target_template.node)
        return texts


class ResultABC(ABC):
    @staticmethod
    def get_type(type_str: str):
        t = type_str.split('.')
        cls_name = t[len(t) - 1]
        package_name = '.'.join(t[:len(t) - 1])
        try:
            package = importlib.import_module(package_name)
            _type = getattr(package, cls_name)
            return _type
        except Exception:
            ALog.log_error(
                msg=ExceptionI18n.tt('module_not_found') % package_name,
                obj=NotFindTemplateError, raise_exception=True)

    @staticmethod
    def generate(data: list, structure: dict):
        ret = []
        if not isinstance(data, list) and data is not None:
            data = [data]
        if data is not None:
            for _data_item in data:
                cls = ResultABC.get_type(structure['_type'])
                if cls is None:
                    ALog.log_error(
                        msg=ExceptionI18n.tt('not_defined') % structure['_type'],
                        obj=NotFindTemplateError, raise_exception=True)
                # 判断是否是pojo,不同的类使用不同的方法获取字段
                is_pojo = others.dp_equals_base(cls, Repository)
                obj = cls(abst=True) if is_pojo else cls()
                # obj = cls() if others.dp_equals_base(cls, object) else cls
                for field, properties in structure.items():
                    if field != '_type' and field != '_single':
                        if isinstance(properties, dict):
                            if is_pojo:
                                obj.add_field(field, ResultABC.generate(_data_item, properties))
                            else:
                                setattr(obj, field, ResultABC.generate(_data_item, properties))
                            # obj.__append_field__
                            # setattr(obj, field, ResultABC.generate(_data_item, properties))
                        else:
                            # 布尔值替换
                            if is_pojo:
                                obj_fields = obj.getFields()
                                t = str(type(obj_fields[properties] if properties in obj_fields.keys() else object))
                                fields_type = re.findall("\'.*\.(.*)\'", t)
                                if 'boolField' in fields_type:
                                    _data_item[field] = bool(_data_item[field])

                                obj.add_field(properties, _data_item[field])
                            else:
                                setattr(obj, properties, _data_item[field])

                            # setattr(obj, properties, _data_item[field])
                if '_single' in structure.keys() and structure['_single'] is True:
                    ret = obj
                else:
                    ret.append(obj)
        else:
            if '_single' in structure.keys() and structure['_single'] is True:
                ret = None
            else:
                ret.append(None)

        if isinstance(ret, list):
            return QuerySet(query_items=ret)
        else:
            return ret


class ResultMapNode(object):
    def __init__(self, target_obj, node, data):
        self.target_obj = target_obj
        self.node = node
        self.data = data

    def apply(self, resultMaps):
        resultMapTags = self.target_obj.xNode.children['resultMap']
        if 'resultMap' in self.node.expand_data.keys():
            resultType = self.node.expand_data['resultMap']
            resultNode = None
            for i in resultMapTags:
                if i.attrs['id'].text == resultType:
                    # 这里不需要break，因为可以重复，取最后一位
                    resultNode = i
            if resultNode is None:
                ALog.log_error(
                    msg=ExceptionI18n.tt('not_result_map') % resultType,
                    obj=NotFindTemplateError, LogObject=self.target_obj.log_obj, raise_exception=True)
            structure = ForeignNode.apply(resultNode, resultMaps)
            return ResultABC.generate(self.data, structure)
        elif 'resultType' in self.node.expand_data.keys():
            resultType = self.node.expand_data['resultType']
            # 由于使用resultType没有映射字段，所以使用原有的结构
            obj = ResultABC.get_type(resultType)
            # 获取类的字段
            fields = others.get_static_fields(obj)
            structure = {
                '_type': resultType,
                **{f: f for f in fields}
            }
            return ResultABC.generate(self.data, structure)
        else:
            ALog.log_error(
                msg=ExceptionI18n.tt('lack_result_type') % self.node.expand_data['id'],
                obj=NotFindTemplateError, LogObject=self.target_obj.log_obj, raise_exception=True)


class ForeignNode:
    @staticmethod
    def apply(resultNode, resultMaps):
        """
        :params resultNode: resultMap节点
        """
        # 判断是否有引用ref
        if 'ref' in resultNode.attrs:
            result_map_match = None
            for item in resultMaps:
                if item.attrs['id'].text == resultNode.attrs['ref'].text:
                    result_map_match = item
                    break
            if result_map_match is None:
                ALog.log_error(
                    msg=ExceptionI18n.tt('not_result_map') % resultNode.attrs['ref'].text,
                    obj=TagAttributeError, raise_exception=True)
            else:
                resultNode = result_map_match
        # 判断结构是否有type返回值类型
        if 'type' not in resultNode.attrs.keys():
            ALog.log_error(
                msg=ExceptionI18n.tt('result_map_not_type'),
                obj=TagAttributeError, raise_exception=True)

        structure = {'_type': resultNode.attrs['type'].text}
        if 'single' in resultNode.attrs.keys():
            structure['_single'] = True if resultNode.attrs['single'].text == 'true' else False

        if 'result' in resultNode.children.keys():
            for i in resultNode.children['result']:
                structure[i.attrs['column'].text] = i.attrs['properties'].text
        return structure
