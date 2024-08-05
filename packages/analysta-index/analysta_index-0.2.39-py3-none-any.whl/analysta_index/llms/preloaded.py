#!/usr/bin/python3
# coding=utf-8

# Copyright (c) 2024 Artem Rozumenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Preloaded models support """

import json
from typing import Optional, Any

from pydantic import PrivateAttr  # pylint: disable=E0401

from langchain_core.embeddings import Embeddings  # pylint: disable=E0401
from langchain_core.language_models import BaseChatModel  # pylint: disable=E0401
from langchain_core.messages import AIMessage  # pylint: disable=E0401
from langchain_core.outputs import ChatGeneration, ChatResult  # pylint: disable=E0401

from ..tools import log


class PreloadedEmbeddings(Embeddings):
    """ Embeddings shim """

    def __init__(self, model_name, *args, **kwargs):  # pylint: disable=W0613
        self.model_name = model_name
        #
        import arbiter  # pylint: disable=E0401,C0415
        from tools import worker_core  # pylint: disable=E0401,C0415
        #
        self.event_node = arbiter.make_event_node(
            config=worker_core.event_node_config,
        )
        self.event_node.start()
        # TaskNode
        self.task_node = arbiter.TaskNode(
            self.event_node,
            pool="indexer",
            task_limit=0,
            ident_prefix="indexer_",
            multiprocessing_context="threading",
            kill_on_stop=False,
            task_retention_period=3600,
            housekeeping_interval=60,
            start_max_wait=3,
            query_wait=3,
            watcher_max_wait=3,
            stop_node_task_wait=3,
            result_max_wait=3,
        )
        self.task_node.start()

    def embed_documents(self, texts):
        """ Embed search docs """
        task_id = self.task_node.start_task(
            name="invoke_model",
            kwargs={
                "routing_key": self.model_name,
                "method": "embed_documents",
                "method_args": [texts],
                "method_kwargs": {},
            },
            pool="indexer",
        )
        return self.task_node.join_task(task_id)

    def embed_query(self, text):
        """ Embed query text """
        task_id = self.task_node.start_task(
            name="invoke_model",
            kwargs={
                "routing_key": self.model_name,
                "method": "embed_query",
                "method_args": [text],
                "method_kwargs": {},
            },
            pool="indexer",
        )
        return self.task_node.join_task(task_id)


class PreloadedChatModel(BaseChatModel):  # pylint: disable=R0903
    """ ChatModel shim """

    model_name: str = ""
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.9
    top_p: Optional[float] = 0.9
    top_k: Optional[int] = 20

    _event_node: Any = PrivateAttr()
    _task_node: Any = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #
        import arbiter  # pylint: disable=E0401,C0415
        from tools import worker_core  # pylint: disable=E0401,C0415
        #
        self._event_node = arbiter.make_event_node(
            config=worker_core.event_node_config,
        )
        self._event_node.start()
        # TaskNode
        self._task_node = arbiter.TaskNode(
            self._event_node,
            pool="indexer",
            task_limit=0,
            ident_prefix="indexer_",
            multiprocessing_context="threading",
            kill_on_stop=False,
            task_retention_period=3600,
            housekeeping_interval=60,
            start_max_wait=3,
            query_wait=3,
            watcher_max_wait=3,
            stop_node_task_wait=3,
            result_max_wait=3,
        )
        self._task_node.start()

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):  # pylint: disable=W0613
        role_map = {
            "system": "system",
            "human": "user",
            "ai": "assistant",
        }
        #
        call_messages = json.loads(json.dumps([
            {
                "role": role_map.get(item.type, "user"),
                "content": item.content,
            } for item in messages
        ]))
        #
        call_kwargs = {
            "max_new_tokens": self.max_tokens,
            "return_full_text": False,
            "temperature": self.temperature,
            "do_sample": True,
            "top_k": self.top_k,
            "top_p": self.top_p,
        }
        #
        try:
            task_id = self._task_node.start_task(
                name="invoke_model",
                kwargs={
                    "routing_key": self.model_name,
                    "method": "__call__",
                    "method_args": [call_messages],
                    "method_kwargs": call_kwargs,
                },
                pool="indexer",
            )
            #
            task_result = self._task_node.join_task(task_id)
        except:  # pylint: disable=W0702
            log.exception("Exception from invoke_model")
            raise
        #
        generated_text = task_result[0]["generated_text"]
        #
        message = AIMessage(content=generated_text)
        generation = ChatGeneration(message=message)
        result = ChatResult(generations=[generation])
        #
        return result

    @property
    def _llm_type(self):
        return self.model_name
