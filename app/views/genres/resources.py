from flask.views import MethodView
from flask_smorest import Page

from app.extensions.api import CursorPage  # noqa:F401
from app.extensions.api import Blueprint
from app.models import Genre

from .schemas import GenreArgsSchema, GenreSchema

blp = Blueprint("Genres", __name__, url_prefix="/api/genres", description="API endpoints about genres")


@blp.route("/")
class Genres(MethodView):
    @blp.etag
    @blp.response(200, GenreSchema(many=True))
    @blp.paginate(Page)
    @blp.doc(description="Get information for multiple genres")
    def get(self):
        """List Genres"""
        ret = Genre.find_all()
        return ret

    @blp.etag
    @blp.arguments(GenreSchema)
    @blp.response(201, GenreSchema)
    @blp.doc(description="Add information for a single genre")
    def post(self, new_genre):
        """Add a new genre"""
        item = Genre(**new_genre)
        item.create()
        return item


@blp.route("/<int:id>")
class GenreById(MethodView):
    @blp.etag
    @blp.response(200, GenreSchema)
    @blp.doc(description="Get information for a single genre")
    def get(self, id):
        """Get genre by ID"""
        ret = Genre.find_by_id(id)
        return ret

    @blp.etag
    @blp.arguments(GenreArgsSchema)
    @blp.response(200, GenreSchema)
    @blp.doc(description="Update information for an genre")
    def put(self, data, id):
        """Update an existing genre"""
        item = Genre.find_by_id(id)
        blp.check_etag(item, GenreArgsSchema)
        GenreArgsSchema().update(item, data)
        item.update()
        return item

    @blp.etag
    @blp.response(204)
    @blp.doc(description="Delete information for a single genre")
    def delete(self, id):
        """Delete an existing genre"""
        item = Genre.find_by_id(id)
        blp.check_etag(item, GenreSchema)
        item.delete()
