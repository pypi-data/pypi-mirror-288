# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: model.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass

import betterproto


@dataclass(eq=False, repr=False)
class Model(betterproto.Message):
    id: int = betterproto.int64_field(1)
    date_added: int = betterproto.int64_field(2)
    company_id: int = betterproto.int64_field(3)
    provider: str = betterproto.string_field(4)
    model: str = betterproto.string_field(5)
    points_to: str = betterproto.string_field(6)
    status: str = betterproto.string_field(7)
    use_fallback: bool = betterproto.bool_field(8)
