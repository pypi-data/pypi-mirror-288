import enum
import functools
import itertools
import textwrap
from dataclasses import dataclass
from typing import *

ReqT = TypeVar('ReqT', bound='_Request')


def qname(module, name):
    return f"{module}::{name}"


PG_TYPE_TO_EDB_TYPE = {
    'character varying': qname('std', 'str'),
    'character': qname('std', 'str'),
    'text': qname('std', 'str'),
    'numeric': qname('std', 'decimal'),
    'edgedb.bigint_t': qname('std', 'bigint'),
    'bigint_t': qname('std', 'bigint'),
    'int4': qname('std', 'int32'),
    'integer': qname('std', 'int32'),
    'bigint': qname('std', 'int64'),
    'int8': qname('std', 'int64'),
    'int2': qname('std', 'int16'),
    'smallint': qname('std', 'int16'),
    'boolean': qname('std', 'bool'),
    'bool': qname('std', 'bool'),
    'double precision': qname('std', 'float64'),
    'float8': qname('std', 'float64'),
    'real': qname('std', 'float32'),
    'float4': qname('std', 'float32'),
    'uuid': qname('std', 'uuid'),
    'timestamp with time zone': qname('std', 'datetime'),
    'edgedb.timestamptz_t': qname('std', 'datetime'),
    'timestamptz_t': qname('std', 'datetime'),
    'timestamptz': qname('std', 'datetime'),
    'duration_t': qname('std', 'duration'),
    'edgedb.duration_t': qname('std', 'duration'),
    'interval': qname('std', 'duration'),
    'bytea': qname('std', 'bytes'),
    'jsonb': qname('std', 'json'),

    'timestamp': qname('cal', 'local_datetime'),
    'timestamp_t': qname('cal', 'local_datetime'),
    'edgedb.timestamp_t': qname('cal', 'local_datetime'),
    'date': qname('cal', 'local_date'),
    'date_t': qname('cal', 'local_date'),
    'edgedb.date_t': qname('cal', 'local_date'),
    'time': qname('cal', 'local_time'),
    'relative_duration_t': qname('cal', 'relative_duration'),
    'edgedb.relative_duration_t': qname('cal', 'relative_duration'),
    'date_duration_t': qname('cal', 'date_duration'),
    'edgedb.date_duration_t': qname('cal', 'date_duration'),

    'edgedb.memory_t': qname('cfg', 'memory'),
    'memory_t': qname('cfg', 'memory'),
    'varchar': 'std::str',
    'str': 'std::str',
}


class Cardinality(str, enum.Enum):
    single = 'SINGLE'
    multi = 'MULTI'

    def is_multi(self):
        return self.value == self.multi

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            uv = value.upper()
            for member in cls:
                if member.value == uv:
                    return member


class ViewDef(NamedTuple):
    relation: str
    columns: Dict[str, str]


@dataclass(init=False)
class _Request:
    def __init__(self, **kwargs):
        self.__dict__.update(self.check_kwargs(kwargs))
        self.validate_fields()

    def check_kwargs(self, kwargs):
        return kwargs

    def validate_fields(self):
        pass

    @staticmethod
    def ensure_checkedlist(
        source: Iterable,
        type: Type[ReqT]
    ) -> List[ReqT]:
        checks = []
        for item in source:
            if not isinstance(item, type):
                checks.append(type(**item))
            else:
                checks.append(item)
        return checks


@dataclass(init=False)
class CreateAnnotation(_Request):
    #: Annotation名称，应为已有Annotation类
    name: str
    #: 声明值
    value: str

    def to_ddl(self, pretty=False):
        return f"CREATE ANNOTATION {self.name} := {self.value!r}"


@dataclass(init=False)
class _Pointer(_Request):
    #: 外部表的列名
    name: str
    #: 属性在edge中的类型
    type: str = None
    #: 计算表达式，表达式中的字段必须使用edge属性名，不可使用外部表列名
    expr: str = None
    #: 作为edge对象的属性名，可选，为空时使用name
    alias: str = None
    relation: str = None
    source: str = None
    target: str = None
    #: 属性基数，single/multi 大小写不敏感
    cardinality: Cardinality = Cardinality.single
    #: 是否必须
    required: bool = False
    #: 声明
    annotations: Sequence[CreateAnnotation] = None

    @functools.cached_property
    def column_def(self) -> Dict[str, str]:
        return {self.realname: self.name}

    @functools.cached_property
    def realname(self) -> str:
        return self.alias or self.name

    @functools.cached_property
    def annotation(self) -> List[str]:
        if self.annotations:
            return [anno.to_ddl() for anno in self.annotations]
        return []

    @functools.cached_property
    def has_table(self):
        return (
            self.expr is None
            and self.cardinality.is_multi()
        )

    def check_kwargs(self, kwargs):
        if card := kwargs.get('cardinality'):
            kwargs['cardinality'] = Cardinality(card)
        return kwargs

    def validate_fields(self):
        if self.has_table:
            missing = []

            if not self.relation:
                missing.append('relation')
            if not self.source:
                missing.append('source')
            if not self.target:
                missing.append('target')

            if missing:
                raise ValueError(
                    f"{self.__class__.__name__[6::]} '{self.realname}' has a table but {missing} is missing."
                )


@dataclass(init=False)
class CreateProperty(_Pointer):
    #: 源表的关联字段，如果没有独立表，本字段值将被忽略
    from_ = None
    #: 是否排他（edge不会给外部表增加排他约束，需要依靠外部表自身保证排他性）
    exclusive: bool = False

    @functools.cached_property
    def edb_type(self) -> str:
        return PG_TYPE_TO_EDB_TYPE[self.type]

    @functools.cached_property
    def view_def(self):
        assert self.relation and self.source and self.target
        columns = {
            'source': self.source,
            'target': self.target,
        }

        return ViewDef(relation=self.relation, columns=columns)

    def validate_fields(self):
        super().validate_fields()

        if self.type is None and self.expr is None:
            raise ValueError(
                f'Either type or expr must be specified '
                f'for property {self.realname!r}.')

        if self.type is not None and self.type not in PG_TYPE_TO_EDB_TYPE:
            raise ValueError(
                f'Property {self.realname!r} has unknown pg type {self.type!r}.'
            )

        if self.cardinality.is_multi() and self.from_ is None:
            raise ValueError(
                f"Field 'from' is required for non-computable "
                f"Multi property {self.realname!r}."
            )

    def to_ddl(self, pretty=False):
        if self.expr:
            return f"CREATE PROPERTY {self.realname} := {self.expr}"

        subcommands = list(self.annotation)
        req = ' required ' if self.required else ' '
        stmt = f"CREATE{req} {self.cardinality.value} PROPERTY {self.realname} -> {self.edb_type}"

        if self.cardinality.is_multi():
            subcommands.append(f"ON {self.from_}")
        if self.exclusive:
            subcommands.append("create constraint exclusive")

        body = ";\n".join(subcommands)
        if body:
            return stmt + f"{{{body}}}"
        else:
            return stmt


@dataclass(init=False)
class CreateLink(_Pointer):
    #: link目标表的关联字段
    to: Optional[str] = None
    #: link源表的关联字段，如果link没有独立表，本字段值将被忽略
    from_: str = 'id'
    properties: Sequence[CreateProperty] = None

    def check_kwargs(self, kwargs):
        kwargs = super().check_kwargs(kwargs)
        if props := kwargs.get('properties'):
            kwargs['properties'] = self.ensure_checkedlist(
                props, CreateProperty)
        else:
            kwargs['properties'] = []

        if (from_ := kwargs.pop('from', None)) is not None:
            kwargs['from_'] = from_

        return kwargs

    def validate_fields(self):
        super().validate_fields()

        if self.type is None and self.expr is None:
            raise ValueError(
                f'Either type or expr must be specified '
                f'for link {self.realname!r}.')

        if self.expr is None and self.to is None:
            raise ValueError("Field 'to' is required for non-computable link.")

        if self.has_table and self.from_ == 'id':
            raise ValueError(
                f"Cannot link '{self.realname}' from 'id' because it has a table. "
                f"Hint: You might have to specify the value of field 'from'."
            )

    @functools.cached_property
    def lprops(self) -> List[str]:
        return [p.to_ddl() for p in self.properties]

    def to_ddl(self, pretty=False):
        if self.expr:
            return f"CREATE LINK {self.realname} := ({self.expr})"

        subcommands = list(self.annotation)
        stmt = f"CREATE {self.cardinality.value} LINK {self.realname} -> {self.type}"
        subcommands.append(f"ON {self.from_} TO {self.to}")
        subcommands.extend(self.lprops)

        body = ";\n".join(subcommands)

        if not body:
            return stmt

        if pretty:
            return stmt + f"{{\n{textwrap.indent(body, '  ')}\n}}"

        return stmt + f"{{{body}}}"

    @functools.cached_property
    def has_table(self):
        return (
            self.expr is None
            and (self.cardinality.is_multi() or self.properties)
        )

    @functools.cached_property
    def view_def(self):
        assert self.relation and self.source and self.target
        columns = {
            'source': self.source,
            'target': self.target,
            **{k: v for p in self.properties for k, v in p.column_def.items()}
        }

        return ViewDef(relation=self.relation, columns=columns)


@dataclass(init=False)
class BaseObjectType(_Request):
    name: str
    module: str = 'default'

    @functools.cached_property
    def qualname(self):
        return f"{self.module}::{self.name}"

    @classmethod
    def from_dict(cls, query: Dict):
        return cls(**query)

    def resolve_view(self):
        return {}


@dataclass(init=False)
class CreateObjectType(BaseObjectType):
    relation: str = ''
    properties: Sequence[CreateProperty] = None
    links: Sequence[CreateLink] = None
    annotations: Sequence[CreateAnnotation] = None

    @classmethod
    def _normalize_kwargs(cls, kwargs: Dict):
        kwargs = kwargs.copy()
        kwargs['properties'] = cls.ensure_checkedlist(
            kwargs.get('properties', []),
            CreateProperty
        )

        kwargs['links'] = cls.ensure_checkedlist(
            kwargs.get('links', []),
            CreateLink
        )

        kwargs['annotations'] = cls.ensure_checkedlist(
            kwargs.get('annotations', []),
            CreateAnnotation
        )
        return kwargs

    @classmethod
    def from_dict(cls, query: Dict):
        upd_query = cls._normalize_kwargs(query)
        return cls(**upd_query)

    def check_kwargs(self, kwargs):
        return self._normalize_kwargs(kwargs)

    def pointers(self):
        yield from itertools.chain(
            sorted(self.properties, key=lambda p: p.expr is not None),
            sorted(self.links, key=lambda p: p.expr is not None),
        )

    @functools.cached_property
    def view_def(self):
        columns = {k: v for ptr in self.pointers() for k, v in ptr.column_def.items()}
        return ViewDef(relation=self.relation, columns=columns)

    @functools.cached_property
    def annotation(self) -> List[str]:
        if self.annotations:
            return [anno.to_ddl() for anno in self.annotations]
        return []

    def get_commands(self, pretty=False):
        sub_cmds = [ptr.to_ddl(pretty=pretty) for ptr in self.pointers()]
        return ';\n'.join(sub_cmds + self.annotation)

    def to_ddl(self, pretty=False):
        body = self.get_commands(pretty)
        if pretty:
            stmt = f"CREATE TYPE {self.qualname} {{\n{textwrap.indent(body, '  ')}\n}}"
        else:
            stmt = f"CREATE TYPE {self.qualname} {{{body}}}"
        return stmt

    def resolve_view(self):
        view = {self.qualname: self.view_def}

        for ptr in itertools.chain(self.links, self.properties):
            if ptr.has_table:
                view[(self.qualname, ptr.realname)] = ptr.view_def

        return view

