from app.extensions.schema import ma
from app.models.genres import Genre


class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre

    id = ma.auto_field(dump_only=True)


class GenreArgsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        include_fk = True

    id = ma.auto_field(dump_only=True)
