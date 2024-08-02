from peewee import (
    SQL,
    BareField,
    CharField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

# Use a database unknown before runtime
database = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class ExportVersion(BaseModel):
    version = BareField(adapt=int)

    class Meta:
        table_name = "export_version"
        primary_key = False


class WorkerVersion(BaseModel):
    id = CharField(primary_key=True)
    slug = CharField()
    name = CharField()
    repository_url = TextField(null=True)
    revision = CharField(null=True)
    version = IntegerField(null=True)
    type = CharField()

    class Meta:
        table_name = "worker_version"


class WorkerRun(BaseModel):
    id = CharField(primary_key=True)
    worker_version = ForeignKeyField(
        column_name="worker_version_id", field="id", model=WorkerVersion
    )
    model_version_id = CharField(null=True)
    model_id = CharField(null=True)
    model_name = CharField(null=True)
    configuration_id = CharField(null=True)
    configuration = TextField(null=True)

    class Meta:
        table_name = "worker_run"


class ImageServer(BaseModel):
    id = IntegerField(primary_key=True)
    url = TextField(unique=True)
    display_name = CharField()
    max_width = IntegerField(null=True)
    max_height = IntegerField(null=True)

    class Meta:
        table_name = "image_server"


class Image(BaseModel):
    id = CharField(primary_key=True)
    server = ForeignKeyField(column_name="server_id", field="id", model=ImageServer)
    url = TextField(unique=True)
    width = IntegerField()
    height = IntegerField()

    class Meta:
        table_name = "image"


class Element(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    type = CharField()
    image = ForeignKeyField(column_name="image_id", field="id", model=Image, null=True)
    polygon = TextField(null=True)
    confidence = FloatField(null=True)
    rotation_angle = IntegerField(constraints=[SQL("DEFAULT 0")])
    mirrored = IntegerField(constraints=[SQL("DEFAULT 0")])
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    created = FloatField()
    updated = FloatField()

    class Meta:
        table_name = "element"


class Classification(BaseModel):
    id = CharField(primary_key=True)
    class_name = CharField()
    confidence = FloatField()
    state = CharField(constraints=[SQL("DEFAULT 'pending'")])
    element = ForeignKeyField(column_name="element_id", field="id", model=Element)
    high_confidence = IntegerField(constraints=[SQL("DEFAULT 0")])
    moderator = CharField(null=True)
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    class Meta:
        table_name = "classification"


class ElementPath(BaseModel):
    id = CharField(primary_key=True)
    parent = ForeignKeyField(
        backref="element_parent_set", column_name="parent_id", field="id", model=Element
    )
    child = ForeignKeyField(column_name="child_id", field="id", model=Element)
    ordering = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "element_path"
        indexes = ((("parent", "child"), True),)


class EntityType(BaseModel):
    color = CharField(constraints=[SQL("DEFAULT 'ff0000'")])
    id = CharField(primary_key=True)
    name = TextField(unique=True)

    class Meta:
        table_name = "entity_type"


class Entity(BaseModel):
    id = CharField(primary_key=True)
    name = TextField()
    type = ForeignKeyField(column_name="type_id", field="id", model=EntityType)
    metas = TextField(null=True)
    moderator = CharField(null=True)
    validated = IntegerField(constraints=[SQL("DEFAULT 0")])
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    class Meta:
        table_name = "entity"


class Metadata(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    value = TextField()
    type = CharField()
    element = ForeignKeyField(column_name="element_id", field="id", model=Element)
    entity = ForeignKeyField(
        column_name="entity_id", field="id", model=Entity, null=True
    )
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    class Meta:
        table_name = "metadata"


class Transcription(BaseModel):
    id = CharField(primary_key=True)
    orientation = TextField(constraints=[SQL("DEFAULT 'horizontal-lr'")])
    text = TextField()
    confidence = FloatField(null=True)
    element = ForeignKeyField(column_name="element_id", field="id", model=Element)
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    class Meta:
        table_name = "transcription"


class TranscriptionEntity(BaseModel):
    id = CharField(primary_key=True)
    entity = ForeignKeyField(column_name="entity_id", field="id", model=Entity)
    length = IntegerField()
    offset = IntegerField()
    confidence = FloatField(null=True)
    transcription = ForeignKeyField(
        column_name="transcription_id", field="id", model=Transcription
    )
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    class Meta:
        table_name = "transcription_entity"
        indexes = (
            (("transcription", "entity", "offset", "length", "worker_run"), True),
        )


class Dataset(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    description = TextField()
    state = CharField(constraints=[SQL("DEFAULT 'open'")])
    sets = TextField()


class DatasetElement(BaseModel):
    id = CharField(primary_key=True)
    element = ForeignKeyField(column_name="element_id", field="id", model=Element)
    dataset = ForeignKeyField(column_name="dataset_id", field="id", model=Dataset)
    set_name = CharField()

    class Meta:
        table_name = "dataset_element"
