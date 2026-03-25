from pathlib import Path
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from flask import Blueprint, Request, request, jsonify
from dataclasses import dataclass

@dataclass
class GraphQLContext:
    request: Request
    
    def get_tenant_id(self) -> str:
        if not request.headers.get('X-Tenant-Id'):
            raise Exception('You must specify a tenant id')
        return self.request.headers.get('X-Tenant-Id', 'default')

DEFAULT_QUERY = """
# Titan banking catalogue service
# Created on 25th March 2026
# by www.ingeniousgeni.us

"""

graphql = Blueprint('graphql', __name__)
explorer_html = ExplorerGraphiQL(
    title="Titan banking catalogue service",
    default_query=DEFAULT_QUERY,
).html(None)

type_defs = load_schema_from_path("./schema.graphql")
schema = make_executable_schema(type_defs)

@graphql.route('/', methods=['GET'])
def playground():
    return explorer_html, 200

@graphql.route('/', methods=['POST'])
def api():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=GraphQLContext(request)
    )
    return jsonify(result), 200 if success else 400