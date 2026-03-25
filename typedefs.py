"""
GraphQL api type defs and resolvers
"""
from ariadne import QueryType, MutationType

query = QueryType()
mutation = MutationType()

@query.field("works")
def resolve_works(_, info):
    return []

@query.field("book")
def resolve_book(_, info):
    return {}

@query.field("jobStatus")
def resolve_job_status(_, info):
    return {}