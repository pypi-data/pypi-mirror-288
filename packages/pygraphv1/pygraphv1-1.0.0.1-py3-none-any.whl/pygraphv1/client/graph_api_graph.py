#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/7/19
# @Author  : yanxiaodong
# @File    : types.py
"""
from typing import List
from pydantic import BaseModel, Field

from .graph_api_variable import Variable
from .graph_api_operator import Operator


class EdgeTarget(BaseModel):
    """
    EdgeTarget
    """
    operator: str = None
    property: str = None
    input: str = None
    output: str = None
    state: str = None


class Edge(BaseModel):
    """
    Edge
    """
    from_: EdgeTarget = Field(None, alias="from")
    to: EdgeTarget = None


class GraphContent(BaseModel):
    """
    Graph Content
    """
    name: str = None
    local_name: str = Field(None, alias="localName")
    environment: str = None
    properties: List[Variable] = None
    inputs: List[Variable] = None
    outputs: List[Variable] = None
    nodes: List[Operator] = None
    edges: List[Edge] = None
    visuals: str = None



