from collections.abc import Mapping
from typing import List, Optional, Any, Sequence, cast

from . import api
from . import types


def convert_to_str(s: Any) -> str:
    if not isinstance(s, str):
        return str(s)
    return s


def to_api_variable_value(instance: types.IntoValuePattern) -> api.VariableValue:
    if instance is None:
        return api.VariableValue(None, None)
    if isinstance(instance, str):
        if instance == "":
            raise TypeError(
                "Oso: Instance cannot be an empty string. "
                + "For wildcards, use the empty dict ({}) or None."
            )
        return api.VariableValue("String", instance)
    if isinstance(instance, bool):
        return api.VariableValue("Boolean", str(instance).lower())
    if isinstance(instance, int):
        return api.VariableValue("Integer", str(instance))
    if isinstance(instance, types.ValueOfType):
        return api.VariableValue(instance.type, None)
    if isinstance(instance, Mapping):
        id_ = instance.get("id")
        type_ = instance.get("type")

        if id_ is None and type_ is None:
            return api.VariableValue(None, None)
        if type_ is None:
            raise TypeError(
                f"Oso: Instances with an ID must also have a type: {instance}"
            )
        return api.VariableValue(type_, id_)
    return api.VariableValue(instance.type, convert_to_str(instance.id))


def to_api_value(instance: types.IntoValue) -> api.ConcreteValue:
    if instance is None:
        raise TypeError("Oso: Expected a concrete value with type and ID. Got None.")
    if isinstance(instance, str):
        if instance == "":
            raise TypeError("Oso: Value cannot be an empty string. ")
        return api.ConcreteValue("String", instance)
    if isinstance(instance, bool):
        return api.ConcreteValue("Boolean", str(instance).lower())
    if isinstance(instance, int):
        return api.ConcreteValue("Integer", str(instance))
    if isinstance(instance, Mapping):
        return api.ConcreteValue(instance["type"], convert_to_str(instance["id"]))
    return api.ConcreteValue(instance.type, convert_to_str(instance.id))


def to_api_variable_fact(fact: types.IntoFactPattern) -> api.VariableFact:
    [name, *args] = fact
    return api.VariableFact(name, [to_api_variable_value(a) for a in args])


def to_api_fact(fact: types.IntoFact) -> api.ConcreteFact:
    [predicate, *args] = fact
    return api.ConcreteFact(predicate, [to_api_value(a) for a in args])


def from_api_concrete_value(value: api.ConcreteValue) -> types.Value:
    return types.Value(id=value.id, type=value.type)


def to_api_facts(params: Optional[Sequence[types.IntoFact]]) -> List[api.ConcreteFact]:
    if not params:
        return []
    return [to_api_fact(param) for param in params]


def from_api_fact(fact: api.ConcreteFact) -> types.Fact:
    if isinstance(fact, api.ConcreteFact):
        return cast(
            types.Fact,
            tuple([fact.predicate, *[from_api_concrete_value(a) for a in fact.args]]),
        )
    assert False


def from_api_facts(
    facts: Optional[Sequence[api.ConcreteFact]],
) -> List[types.Fact]:
    if not facts:
        return []
    return [from_api_fact(fact) for fact in facts]
