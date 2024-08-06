#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/7/19
# @Author  : yanxiaodong
# @File    : graph.py
"""
import os
import json
import copy
from typing import Any, Dict, List
from collections import defaultdict

import bcelogger
from pygraphv1.client.graph_api_graph import EdgeTarget, Edge, GraphContent
from pygraphv1.client.graph_api_operator import Operator
from pygraphv1.client.graph_api_variable import Variable
from tritonv2.model_config import ModelConfig
from windmillclient.client.windmill_client import WindmillClient
from windmillartifactv1.client.artifact_api_artifact import get_name, parse_artifact_name
from windmillmodelv1.client.model_api_model import parse_model_name, ModelName


class Graph:
    """
    Graph class.
    """

    def __init__(self, models: Dict):
        self.models = models
        self.nodes = []
        self.edges = []

    def build_nodes(self, ensemble_steps: Dict):
        """
        Build nodes from steps.
        """
        for name, model in self.models.items():
            assert name in ensemble_steps, f"Model {name} not in steps {ensemble_steps}."
            step = ensemble_steps[name]
            bcelogger.info(f"Building node for model {name}")

            operator = Operator()
            operator.name = step["modelName"]
            operator.local_name = step["modelName"]

            operator.properties = []
            for key, value in model.items():
                variable = self._set_node_property(key, value)
                if variable is not None:
                    bcelogger.info(f"Setting node for model {name} properties for {key}:{value}")
                    operator.properties.append(variable)

            operator.inputs = []
            for key, value in step["inputMap"].items():
                bcelogger.info(f"Setting node for model {name} inputs for {key}:{value}")
                operator.inputs.append((Variable(name=key, type="int")))

            operator.outputs = []
            for key, value in step["outputMap"].items():
                bcelogger.info(f"Setting node for model {name} outputs for {key}:{value}")
                operator.outputs.append((Variable(name=key, type="int")))

            self.nodes.append(operator)

    def build_edges(self, ensemble_steps: Dict):
        """
        Build edges from steps.
        """
        inputs = defaultdict(list)
        outputs = defaultdict(dict)
        for name, step in ensemble_steps.items():
            new_step = copy.deepcopy(step)
            for key, value in step["inputMap"].items():
                new_step["inputMap"][value] = key
                inputs[value].append(new_step)
            for key, value in step["outputMap"].items():
                outputs[value] = new_step

        for key, output in outputs.items():
            if key not in inputs:
                bcelogger.info(f"It's the last node, no input for {key}")

            for input_ in inputs[key]:
                edge = Edge()
                bcelogger.info(f'Setting edge output for {output["modelName"]}:{key}')
                edge.from_ = EdgeTarget(operator=output["modelName"], output=key)
                bcelogger.info(f'Setting edge input for {input_["modelName"]}:{input_["inputMap"][key]}')
                edge.to = EdgeTarget(operator=input_["modelName"], input=input_["inputMap"][key])
                self.edges.append(edge)

    def _set_node_property(self, name: str, value: Any):
        if isinstance(value, str):
            variable = Variable(name=name, type="string", value=value, option="false", readonly="false")
            return variable

        if isinstance(value, List):
            variable = Variable(name=name, type="object", option="false", readonly="false", schema=[])
            for v in value:
                index = 1
                if isinstance(v, str):
                    variable.schema.append(Variable(name=name + "_" + str(index),
                                                    type="string",
                                                    value=v,
                                                    option="false",
                                                    readonly="false"))
            return variable

        return

    def __call__(self, name: str, local_name: str, ensemble_steps: Dict):
        """
        __call__ method.
        """
        self.build_nodes(ensemble_steps)
        self.build_edges(ensemble_steps)

        graph_content = GraphContent()
        graph_content.name = name
        graph_content.local_name = local_name
        graph_content.nodes = self.nodes
        graph_content.edges = self.edges

        return graph_content


def build_graph(windmill_client: WindmillClient,
                ensemble_name: str,
                sub_models: Dict,
                extra_models: Dict,
                output_uri: str):
    """
    Build graph from steps.
    """
    # 1. 下载ensemble model
    ensemble_model = parse_model_name(parse_artifact_name(name=ensemble_name).object_name)
    ensemble_output_uri = os.path.join(output_uri, ensemble_model.local_name)
    windmill_client.download_artifact(name=ensemble_name, output_uri=ensemble_output_uri)

    # 2. 获取ensemble config
    ensemble_config = ModelConfig.create_from_file(
        model_config_filepath=os.path.join(ensemble_output_uri, "config.pbtxt"))

    # 3. 解析 scheduling step
    ensemble_steps = {}
    sub_models.update(extra_models)
    for name, step in ensemble_config.get_ensemble_steps().items():
        bcelogger.info(f"Parsing step {name} is {step}")
        ensemble_steps[name] = step
        sub_models[name] = sub_models.get(name, "latest")
        bcelogger.info(f"Model name {name} version {sub_models[name]}")

    # 4. 解析bls节点
    for name, _ in ensemble_config.get_ensemble_steps().items():
        object_name = ModelName(workspace_id=ensemble_model.workspace_id,
                                model_store_name=ensemble_model.model_store_name,
                                local_name=name).get_name()
        model_output_uri = os.path.join(output_uri, name)
        windmill_client.download_artifact(object_name=object_name,
                                          version=sub_models[name],
                                          output_uri=model_output_uri)

    # 5. 获取 models 属性
    models = {}
    for name, step in ensemble_steps.items():
        bcelogger.info(f"Parsing step {name} is {step}")

        response = windmill_client.get_model(workspace_id=ensemble_model.workspace_id,
                                             model_store_name=ensemble_model.model_store_name,
                                             local_name=name)

        response = json.loads(response.raw_data)
        response["version"] = sub_models[name] if sub_models[name] != "latest" else response["artifact"]["version"]
        response["category"] = response["category"]["category"]
        models[name] = response

    # 6. 构建graph
    graph = Graph(models=models)
    graph = graph(name=ensemble_name,
                  local_name=ensemble_model.local_name,
                  ensemble_steps=ensemble_steps)

    return graph
