#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/8/2
# @Author  : yanxiaodong
# @File    : model_metadata_update.py
"""
import os
import base64
import time
import json
import shutil
from argparse import ArgumentParser
import yaml

import bcelogger
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.graph.graph import build_graph
from windmillmodelv1.client.model_api_model import Category, Label


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--windmill-endpoint", type=str, default="")
    parser.add_argument("--windmill-ak", type=str, default="")
    parser.add_argument("--windmill-sk", type=str, default="")
    parser.add_argument("--org-id", type=str, default="")
    parser.add_argument("--user-id", type=str, default="")
    parser.add_argument("--ensemble-name", type=str, default="")
    parser.add_argument("--sub-models", type=str, default="")
    parser.add_argument("--extra-models", type=str, default="")

    args, _ = parser.parse_known_args()

    return args


def metadata_update(args):
    """
    Update the model metadata.
    """
    windmill_client = WindmillClient(ak=args.windmill_ak,
                                     sk=args.windmill_sk,
                                     endpoint=args.windmill_endpoint,
                                     context={"OrgID": args.org_id, "UserID": args.user_id})

    # 1. Build the model graph
    output_uri = f"/home/windmill/{time.time()}/model"
    sub_models = json.loads(base64.b64decode(args.sub_models))
    sub_models = sub_models if sub_models is not None else {}
    extra_models = json.loads(base64.b64decode(args.extra_models))
    extra_models = extra_models if extra_models is not None else {}
    graph = build_graph(windmill_client=windmill_client,
                        ensemble_name=args.ensemble_name,
                        sub_models=sub_models,
                        extra_models=extra_models,
                        output_uri=output_uri)

    # 2. 获取后处理节点
    model_name = None
    category = None
    for node in graph.nodes:
        for property_ in node.properties:
            if property_.name == "localName":
                model_name = property_.value
            if property_.name == "category" and property_.value == Category.CategoryImagePostprocess.value:
                category = property_.value
        if model_name is not None and category is not None:
            break
    assert category is not None, "No postprocess model found"
    bcelogger.info(f"Postprocess model name: {model_name}, category: {category}")

    # 3. 解析后处理节点
    labels = []
    label_set = set()
    index = 0
    filepath = os.path.join(output_uri, model_name, "parse.yaml")
    data = yaml.load(open(filepath, "r"), Loader=yaml.FullLoader)
    assert len(data["outputs"]) > 0, f"No output found in {data}"
    assert "fields_map" in data["outputs"][0], f'Field fields_map not in {data["outputs"][0]}'
    for item in data["outputs"][0]["fields_map"]:
        for label in item["categories"]:
            if label["id"] in label_set:
                continue
            bcelogger.info(f'Model {item["model_name"]} label: {label}')
            label_set.add(label["id"])
            labels.append(Label(id=index, name=label["id"], displayName=label["name"]).dict())

    # 4. 更新metadata
    response = windmill_client.get_artifact(object_name=args.ensemble_name, version="latest")
    bcelogger.info(f"Model {args.ensemble_name} response: {response}")
    metadata = response.metadata
    metadata["graphContent"] = graph.dict(by_alias=True)
    metadata["labels"] = labels
    windmill_client.update_artifact(name=args.ensemble_name, metadata=metadata)
    bcelogger.info(f"Update model metadata {metadata} successfully")

    # 5. 删除模型
    shutil.rmtree(output_uri)
    bcelogger.info(f"Delete model {output_uri} successfully")


if __name__ == "__main__":
    args = parse_args()
    metadata_update(args)
