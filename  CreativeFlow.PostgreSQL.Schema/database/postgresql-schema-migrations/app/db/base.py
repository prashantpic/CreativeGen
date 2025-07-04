from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Define a naming convention for constraints to ensure consistency,
# which is particularly helpful for Alembic autogeneration.
# See: https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Create a MetaData instance with the defined naming convention.
metadata = MetaData(naming_convention=convention)

# Create the declarative base. All ORM models will inherit from this class.
# The metadata object is passed to the base, so all tables derived from this
# base will use the specified naming convention.
Base = declarative_base(metadata=metadata)