from flask.views import MethodView
from flask_smorest import Page

from app.extensions.api import CursorPage  # noqa:F401
from app.extensions.api import Blueprint
from app.models import Track

from .schemas import TrackArgsSchema, TrackSchema

blp = Blueprint("Tracks", __name__, url_prefix="/api/tracks", description="API endpoints about tracks")


@blp.route("/")
class Tracks(MethodView):
    @blp.etag
    @blp.response(200, TrackSchema(many=True))
    @blp.paginate(Page)
    @blp.doc(description="Get information for multiple tracks")
    def get(self):
        """List tracks"""
        ret = Track.find_all()
        return ret

    @blp.etag
    @blp.arguments(TrackSchema)
    @blp.response(201, TrackSchema)
    @blp.doc(description="Add information for a single track")
    def post(self, new_track):
        """Add a new track"""
        item = Track(**new_track)
        item.create()
        return item


@blp.route("/<int:id>")
class TrackById(MethodView):
    @blp.etag
    @blp.response(200, TrackSchema)
    @blp.doc(description="Get information for a single track")
    def get(self, id):
        """Get track by ID"""
        ret = Track.find_by_id(id)
        return ret

    @blp.etag
    @blp.arguments(TrackArgsSchema)
    @blp.response(200, TrackSchema)
    @blp.doc(description="Update information for an track")
    def put(self, data, id):
        """Update an existing track"""
        item = Track.find_by_id(id)
        blp.check_etag(item, TrackArgsSchema)
        TrackArgsSchema().update(item, data)
        item.update()
        return item

    @blp.etag
    @blp.response(204)
    @blp.doc(description="Delete information for a single track")
    def delete(self, id):
        """Delete an existing track"""
        item = Track.find_by_id(id)
        blp.check_etag(item, TrackSchema)
        item.delete()
