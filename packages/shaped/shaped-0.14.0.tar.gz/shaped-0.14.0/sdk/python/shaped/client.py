import logging
from typing import Any, Dict, List, Optional

from shaped.autogen.api.model_inference_api import ModelInferenceApi
from shaped.autogen.api_client import ApiClient
from shaped.autogen.configuration import Configuration
from shaped.autogen.models.complement_items_request import (
    ComplementItemsRequest,
)
from shaped.autogen.models.inference_config import InferenceConfig
from shaped.autogen.models.interaction import Interaction
from shaped.autogen.models.post_rank_request import PostRankRequest
from shaped.autogen.models.retrieve_request import RetrieveRequest
from shaped.autogen.models.similar_item_request import SimilarItemRequest
from shaped.autogen.models.similar_users_request import (
    SimilarUsersRequest,
)
from pydantic import StrictBool, StrictStr


class Client:
    """
    This class provides a clean user interface to access Shaped functionality.
    It currently supports calls to the Model Inference API.
    """

    def __init__(self, api_key: str):
        self._api_key = api_key
        api_key_dict = {"main": api_key}
        self._configuration = Configuration(api_key=api_key_dict)
        self._api_client = ApiClient(self._configuration)
        self._model_inference_api = ModelInferenceApi(self._api_client)
        self._logger = logging.getLogger(__name__)
        if not self._logger.hasHandlers():
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
            console_handler.setFormatter(console_format)
            self._logger.addHandler(console_handler)
            self._logger.setLevel(logging.INFO)

    def rank(
        self,
        model_name: StrictStr,
        user_id: Optional[StrictStr] = None,
        item_ids: Optional[List[StrictStr]] = None,
        interactions: Optional[List[Interaction]] = None,
        filter_predicate: Optional[StrictStr] = None,
        user_features: Optional[Dict[str, Any]] = None,
        item_features: Optional[Dict[str, Any]] = None,
        text_query: Optional[StrictStr] = None,
        flush_paginations: Optional[StrictBool] = None,
        return_metadata: Optional[StrictBool] = None,
        config: Optional[InferenceConfig] = None,
    ):
        """
        Rank returns the list of relevant item ids (from most-relevant to least) for the
        given request context.

        There are several ways to use rank depending on the combination of request
        arguments given.

        For more information visit https://docs.shaped.ai/docs/api#tag/Model-Inference
        """
        self._logger.debug("Calling rank on model %s", model_name)
        post_rank_request = PostRankRequest(
            user_id=user_id,
            item_ids=item_ids,
            interactions=interactions,
            filter_predicate=filter_predicate,
            user_features=user_features,
            item_features=item_features,
            text_query=text_query,
            flush_paginations=flush_paginations,
            return_metadata=return_metadata,
            config=config,
        )
        return self._model_inference_api.post_rank_models_model_id_rank_post(
            model_name=model_name, 
            x_api_key=self._api_key, 
            post_rank_request=post_rank_request
        )

    def retrieve(
        self,
        model_name: StrictStr,
        user_id_query: Optional[StrictStr] = None,
        text_query: Optional[StrictStr] = None,
        filter_predicate: Optional[StrictStr] = None,
        flush_paginations: Optional[StrictBool] = None,
        return_metadata: Optional[StrictBool] = None,
        config: Optional[InferenceConfig] = None,
    ):
        """
        Retrieve returns relevant item_ids for the given input text or user query. It
        can be used instead of rank if the filtering, scoring and ordering stages aren't
        needed for the final ranking.

        Typically people use this endpoint over rank if they want to reduce latency and
        complexity of the ranking pipeline and only need a subset of the functionality,
        e.g. just search but without personalization.
        """
        self._logger.debug("Calling retrieve on model %s", model_name)
        retrieve_request = RetrieveRequest(
            user_id_query=user_id_query,
            text_query=text_query,
            filter_predicate=filter_predicate,
            flush_paginations=flush_paginations,
            return_metadata=return_metadata,
            config=config,
        )
        return self._model_inference_api.post_retrieve_models_model_id_retrieve_post(
            model_name=model_name,
            x_api_key=self._api_key,
            retrieve_request=retrieve_request,
        )

    def similar_items(
        self,
        model_name: StrictStr,
        item_id: StrictStr = None,
        user_id: Optional[StrictStr] = None,
        return_metadata: Optional[StrictBool] = None,
        flush_paginations: Optional[StrictBool] = None,
        config: Optional[InferenceConfig] = None,
    ):
        """
        Similar Items returns a list of similar items to the given input item query. If
        a user_id is given the response will return similar items personalized for that
        user.
        """
        self._logger.debug("Calling similar_items on model %s", model_name)
        similar_item_request = SimilarItemRequest(
            item_id=item_id,
            user_id=user_id,
            return_metadata=return_metadata,
            flush_paginations=flush_paginations,
            config=config,
        )
        return (
            self._model_inference_api
            .post_similar_items_models_model_name_similar_items_post(
                model_name=model_name,
                x_api_key=self._api_key,
                similar_item_request=similar_item_request,
            )
        )

    def similar_users(
        self,
        model_name: StrictStr,
        user_id: StrictStr = None,
        return_metadata: Optional[StrictBool] = None,
        flush_paginations: Optional[StrictBool] = None,
        config: Optional[InferenceConfig] = None,
    ):
        """
        Similar Users returns a list of similar user to the given input user query.
        """
        self._logger.debug("Calling similar_users on model %s", model_name)
        similar_users_request = SimilarUsersRequest(
            user_id=user_id,
            return_metadata=return_metadata,
            flush_paginations=flush_paginations,
            config=config,
        )
        return (
            self._model_inference_api
            .post_similar_users_models_model_name_similar_users_post(
                model_name=model_name,
                user_id=user_id,
                x_api_key=self._api_key,
                similar_users_request=similar_users_request,
            )
        )

    def complement_items(
        self,
        model_name: StrictStr,
        item_ids: List[StrictStr],
        user_id: Optional[StrictStr] = None,
        return_metadata: Optional[StrictBool] = None,
        config: Optional[InferenceConfig] = None,
    ):
        """
        Complement Items returns a list of items that complement the given input items.
        For example, if you have a list of items in a user's cart, you can use this
        endpoint to return items that complement the cart (i.e. "Complete-the-bag"
        use-cases).
        """
        self._logger.debug("Calling complement_items on model %s", model_name)
        complement_items_request = ComplementItemsRequest(
            item_ids=item_ids,
            user_id=user_id,
            return_metadata=return_metadata,
            config=config,
        )
        return (
            self._model_inference_api
            .post_complement_items_models_model_name_complement_items_post(
                model_name=model_name,
                x_api_key=self._api_key,
                complement_items_request=complement_items_request,
            )
        )
