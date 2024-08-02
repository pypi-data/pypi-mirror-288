from typing import Optional, Dict, List, Union, Any

from pinecone_plugin_interface import PineconePlugin

from .core.client import ApiClient
from .core.client.api.inference_api import InferenceApi
from .core.client.model.embed_request import EmbedRequest
from .core.client.model.embed_request_inputs import EmbedRequestInputs
from .core.client.model.embed_request_parameters import EmbedRequestParameters
from .core.client.model.document import Document
from .core.client.model.inline_object import InlineObject
from .models import EmbeddingsList, RerankResult
from .version import API_VERSION


class Inference(PineconePlugin):
    """
    The `Inference` class configures and utilizes the Pinecone Inference API to generate embeddings.

    :param config: A `pinecone.config.Config` object, configured and built in the Pinecone class.
    :type config: `pinecone.config.Config`, required
    """

    def __init__(self, config, openapi_client_builder):
        self.config = config
        self.inference_api = openapi_client_builder(
            ApiClient, InferenceApi, API_VERSION
        )

    def embed(
        self,
        model: str,
        inputs: Union[str, List[Dict], List[str]],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> EmbeddingsList:
        """
        Generates embeddings for the provided inputs using the specified model and (optional) parameters.

        :param model: The model to use for generating embeddings.
        :type model: str, required

        :param inputs: A list of items to generate embeddings for.
        :type inputs: list, required

        :param parameters: A dictionary of parameters to use when generating embeddings.
        :type parameters: dict, optional

        :return: EmbeddingsList object with keys `data`, `model`, and `usage`. The `data` key contains a list of
        `n` embeddings, where `n` = len(inputs) and type(n) = Embedding. Precision of returned embeddings is either
        float16 or float32, with float32 being the default. `model` key is the model used to generate the embeddings.
        `usage` key contains the total number of tokens used at request-time.

        Example:
        >>> inputs = ["Who created the first computer?"]
        >>> outputs = pc.inference.embed(model="multilingual-e5-large", inputs=inputs, parameters={"input_type": "passage", "truncate": "END"})
        >>> print(outputs)
        EmbeddingsList(
            model='multilingual-e5-large',
            data=[
                {'values': [0.1, ...., 0.2]},
              ],
            usage={'total_tokens': 6}
        )
        """
        embeddings_inputs: List[EmbedRequestInputs] = []
        if isinstance(inputs, str):
            embeddings_inputs = [EmbedRequestInputs(text=inputs)]
        elif isinstance(inputs, list) and len(inputs) > 0:
            if isinstance(inputs[0], str):
                embeddings_inputs = [EmbedRequestInputs(text=i) for i in inputs]
            elif isinstance(inputs[0], dict):
                embeddings_inputs = [EmbedRequestInputs(**i) for i in inputs]
            else:
                raise Exception("Invalid type for variable 'inputs'")
        else:
            raise Exception("Invalid type for variable 'inputs'")

        if parameters:
            request_body = EmbedRequest(
                model=model,
                inputs=embeddings_inputs,
                parameters=EmbedRequestParameters(**parameters),
            )
        else:
            request_body = EmbedRequest(
                model=model,
                inputs=embeddings_inputs,
            )

        embeddings_list = self.inference_api.embed(embed_request=request_body)
        return EmbeddingsList(embeddings_list=embeddings_list)

    def rerank(
        self,
        model: str,
        query: str,
        documents: Union[List[str], List[Dict[str, Any]]],
        rank_fields: List[str] = ["text"],
        return_documents: bool = True,
        top_n: Optional[int] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> RerankResult:
        if isinstance(documents, list) and len(documents) > 0:
            if isinstance(documents[0], str):
                documents = [Document(text=doc) for doc in documents]
            elif isinstance(documents[0], dict):
                documents = [Document(**doc) for doc in documents]
            else:
                raise Exception("Invalid type for variable 'inputs'")
        else:
            raise Exception("Invalid type for variable 'inputs'")

        args = {
            "model": model,
            "query": query,
            "documents": documents,
            "rerank_fields": rank_fields,
            "return_documents": return_documents,
        }
        if top_n:
            args["top_n"] = top_n
        if parameters:
            args["parameters"] = parameters

        rerank_request = InlineObject(**args)
        api_response = self.inference_api.rerank(inline_object=rerank_request)
        return RerankResult(rank_result=api_response)
