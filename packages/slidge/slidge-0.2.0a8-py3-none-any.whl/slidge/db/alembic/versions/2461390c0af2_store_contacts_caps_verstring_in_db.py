"""Store contacts caps verstring in DB

Revision ID: 2461390c0af2
Revises: 2b1f45ab7379
Create Date: 2024-07-20 08:00:11.675735

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2461390c0af2"
down_revision: Union[str, None] = "2b1f45ab7379"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("contact", schema=None) as batch_op:
        batch_op.add_column(sa.Column("caps_ver_bare", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("caps_ver", sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("contact", schema=None) as batch_op:
        batch_op.drop_column("caps_ver")
        batch_op.drop_column("caps_ver_bare")

    # ### end Alembic commands ###
