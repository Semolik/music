from backend.models.user import *
from backend.models.roles import *
from backend.models.files import *
from backend.models.genres import *
from backend.models.albums import *
from backend.models.tracks import *
from backend.models.clips import *
from backend.models.playlists import *
from backend.models.slider import *


from backend.core.config import settings

from backend.db.base_class import Base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config
target_metadata = Base.metadata


def get_url():
    return settings.DATABASE_URI


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    url = get_url()

    configuration["sqlalchemy.url"] = url
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    if not database_exists(url):
        create_database(url)
    target_metadata.create_all(connectable)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
