import logging
from typing import Any, Dict
import requests
from database import session
from models import Book, Tenant

logger = logging.getLogger(__name__)

class Library:
    """
    This interfaces with the OpenLibrary API.
    """ 

    API_URL = "https://openlibrary.org"

    def __init__(self, tenant_id: str):
        self.tenant = session.get(Tenant, tenant_id)

    def ingest(self, author=None, subject=None):
        if not author and not subject:
            raise Exception("You must specify either an author or subject")
        results = self.search({
            "author": author,
            "subject": subject,
        })
        for request in results:
            book = session.query(Book).filter_by(
                work_identifier=request['key']
            ) or Book(tenant_id=self.tenant.id)
            book.title = request['title']
            book.author = request['author_name'] # todo: parse author alternative name
            book.first_publish_year=request['first_publish_year']
            book.subjects=request['subject_key']
            book.cover_image_url=None # todo ingest all at once for performance   
            self.session.add(book)
        self.session.commit()

    def search(self, query: Dict[str, Any]) -> Dict[str, Any]:
        parameters = []
        for _, (k, v) in enumerate(query.items()):
            if k and v:
                parameters.append(f"{k}:{v}")
        query_str = "AND ".join(parameters)
        response = requests.get(f"{self.API_URL}/search.json?q={query_str}")
        return response.json()["docs"]

