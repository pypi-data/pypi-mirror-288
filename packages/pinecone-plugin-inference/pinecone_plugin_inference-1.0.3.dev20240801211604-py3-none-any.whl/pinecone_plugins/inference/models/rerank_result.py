from pinecone_plugins.inference.core.client.models import (
    RankResult as OpenAPIRankResult,
)


class RerankResult:
    """
    A rerank result.
    """

    def __init__(self, rank_result: OpenAPIRankResult):
        self.rank_result = rank_result

    def __str__(self):
        return str(self.rank_result)

    def __repr__(self):
        return repr(self.rank_result)

    def __getattr__(self, attr):
        return getattr(self.rank_result, attr)
