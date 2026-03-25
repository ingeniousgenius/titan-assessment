"""
GraphQL api type defs and resolvers
"""
from dataclasses import dataclass
from typing import Optional
from ariadne import QueryType, MutationType, InputType
from graphql import GraphQLResolveInfo

query = QueryType()
mutation = MutationType()

@dataclass
class MinMaxRangeInput:
    min: Optional[int]
    max: Optional[int]

@dataclass
class WorksFilter:
    author: Optional[str]
    subject: Optional[str]
    publishYear: Optional[MinMaxRangeInput]

@dataclass
class SearchWorksInput:
    keyword: Optional[str]
    filter: Optional[WorksFilter]
    limit: Optional[int]
    offset: Optional[int]

def get_search_works_input(data: dict) -> SearchWorksInput:
    filter = data.get('filter', {})
    publish_year = filter.get('publishYear', None)
    range_input = None
    if publish_year:
        range_input = MinMaxRangeInput(
            min=publish_year.get('min', None),
            max=publish_year.get('max', None)
        ) 
    return SearchWorksInput(
        keyword=data.get('keyword', None),
        filter=WorksFilter(
            author=filter.get('author', None),
            subject=filter.get('subject', None),
            publishYear=range_input
        ),
        limit=data.get('limit', None),
        offset=data.get('offset', None)
    )

SearchWorksInputType = InputType(
    "SearchWorksInput",
    get_search_works_input
)

@query.field("works")
def resolve_works(
    _,
    info: GraphQLResolveInfo,
    input: SearchWorksInput
):
    return []

@query.field("book")
def resolve_book(
    _,
    info: GraphQLResolveInfo,
    bookId: str
):
    return {}

@query.field("jobStatus")
def resolve_job_status(
    _,
    info: GraphQLResolveInfo,
    jobId: str,
):
    return {}