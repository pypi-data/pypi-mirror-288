#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Generic, Any, final

from ..config.serialize import SerializeConfig
from ..exceptions import SerializeException, NotImplementedException
from ..generic import T
from ..utils.strings import StringUtils
from . import _tools


def __parser_iter(values, camel):
    l = []
    l_append = l.append
    for value in values:
        l_append(__parser(value, camel))
    return l


def __parser_dict(values, camel):
    d = {}
    for key, value in values.items():
        if camel:
            k = StringUtils.convert_to_camel(key).origin()
        else:
            k = key
        d[k] = __parser(value, camel)
    return d


def __parser(value, camel):
    if issubclass(type(value), (list, tuple, set)):
        return __parser_iter(value, camel)
    elif issubclass(type(value), dict):
        return __parser_dict(value, camel)
    elif isinstance(value, _Serializable):
        return value.serializer()
    return value


def _serializer(value, camel):
    return __parser(value, camel)


class _SerializeField:
    __params__ = ['name', 'autoname', 'camel', 'hooks', 'types']

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        instance.__attr_name__ = None
        __head = f"{_SerializeField.__name__}__"
        for param in _SerializeField.__params__:
            setattr(instance, f"{__head}{param}", kwargs.get(param, None))
        return instance

    def __set_name__(self, owner, name):
        self.__attr_name__ = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.__attr_name__)

    def __set__(self, instance, value):
        if instance is not None:
            self.__types_handler(instance, value)
            instance.__dict__[self.__attr_name__] = self.__hook_handler(instance, value)

    @final
    def __hook_handler(self, instance, value):
        hooks = self.__hooks
        if hooks is not None:
            if not isinstance(hooks, (list, tuple)):
                raise TypeError(f'{instance.__class__.__name__}.'
                                f'{_tools.parser_private_attr_name(instance.__class__, self.__attr_name__)} '
                                f'params "types" type error: Excepted type "tuple[Callable[[Any], tuple[bool, Any]]] '
                                f'or list[Callable[[Any], tuple[bool, Any]]]", got "{type(hooks).__name__}"')
            for hook in hooks:
                result, value = hook(value)
                if not result:
                    raise SerializeException(f"{instance.__class__.__name__}."
                                             f"{_tools.parser_private_attr_name(instance.__class__, self.__attr_name__)}"
                                             f" hook exec fail: hook result fail => '{result}', '{value}'.")
        return value

    @final
    def __types_handler(self, instance, value):
        types = self.__types
        if types is not None:
            if not isinstance(types, (list, tuple)):
                raise TypeError(f'{instance.__class__.__name__}.'
                                f'{_tools.parser_private_attr_name(instance.__class__, self.__attr_name__)} '
                                f'params "types" type error: Excepted type "tuple[type]", got "{type(types).__name__}"')
            if not isinstance(value, tuple(types)):
                raise TypeError(f'{instance.__class__.__name__}.'
                                f'{_tools.parser_private_attr_name(instance.__class__, self.__attr_name__)}: '
                                f'Excepted type "{[type_.__name__ for type_ in types]}", '
                                f'got "{type(value).__name__}"')


class _Serializable(Generic[T]):
    __field_head = f"{_SerializeField.__name__}__"

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        head = f"_{cls.__name__}"
        instance.__head__ = head
        instance.__serialize_fields = dict(instance.__class__.__dict__)
        return instance

    @final
    def __get_field_attr(self, field: _SerializeField, attr_name):
        return getattr(field, f"{self.__field_head}{attr_name}", None)

    @property
    def autoname(self) -> bool:
        return False

    @property
    def camel(self) -> bool:
        return False

    @final
    def __serializer(self) -> dict[str, T]:
        d = {}
        index = 0
        for key, value in self.__dict__.items():
            if key not in self.__serialize_fields:
                continue
            v = self.__serialize_fields.get(key)
            if isinstance(v, _SerializeField):
                index += 1
                camel = self.__get_field_attr(v, "camel") or self.camel or SerializeConfig.camel
                name = self.__get_field_attr(v, "name")
                if not name:
                    if key.startswith(self.__head__):
                        name = key.replace(self.__head__, "")
                    else:
                        name = key
                    if self.__get_field_attr(v, "autoname") or self.autoname or SerializeConfig.autoname:
                        name = _tools.rm_underline_start_end(name)
                        if camel:
                            name = StringUtils.convert_to_camel(name).origin()
                if (name and (len(name) == 1 and name == "_")) or StringUtils.is_black(name):
                    continue
                d[name] = _serializer(value, camel)
        return d

    @final
    def serializer(self) -> dict[str, T] or Any:
        """
        For serialization operations, custom serialization methods are used first,
        and defaults are used if not implemented
        :return:
        """
        try:
            return self.custom_serializer()
        except (NotImplementedError, NotImplementedException):
            return self.__serializer()

    def custom_serializer(self):
        """
        A custom serialization interface is provided to the user, and if the interface is implemented,
        the serialization results of the interface are preferentially used。
        :return:
        """
        raise NotImplementedException("need implemented")


__all__ = [_Serializable, _SerializeField, _serializer]
