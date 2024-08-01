"""Move everything to persistent DB

Revision ID: b33993e87db3
Revises: e91195719c2c
Create Date: 2024-06-25 16:09:36.663953

"""

import shutil
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

import slidge.db.meta
from slidge import global_config

# revision identifiers, used by Alembic.
revision: str = "b33993e87db3"
down_revision: Union[str, None] = "e91195719c2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "avatar",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("hash", sa.String(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("legacy_id", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("etag", sa.String(), nullable=True),
        sa.Column("last_modified", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("filename"),
        sa.UniqueConstraint("hash"),
        sa.UniqueConstraint("legacy_id"),
    )
    op.create_table(
        "attachment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_account_id", sa.Integer(), nullable=False),
        sa.Column("legacy_file_id", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("sims", sa.String(), nullable=True),
        sa.Column("sfs", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_account_id"],
            ["user_account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_attachment_legacy_file_id"),
        "attachment",
        ["legacy_file_id"],
        unique=False,
    )
    op.create_index(op.f("ix_attachment_url"), "attachment", ["url"], unique=False)
    op.create_table(
        "contact",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_account_id", sa.Integer(), nullable=False),
        sa.Column("legacy_id", sa.String(), nullable=False),
        sa.Column("jid", slidge.db.meta.JIDType(), nullable=False),
        sa.Column("avatar_id", sa.Integer(), nullable=True),
        sa.Column("nick", sa.String(), nullable=True),
        sa.Column("cached_presence", sa.Boolean(), nullable=False),
        sa.Column("last_seen", sa.DateTime(), nullable=True),
        sa.Column("ptype", sa.String(), nullable=True),
        sa.Column("pstatus", sa.String(), nullable=True),
        sa.Column("pshow", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["avatar_id"],
            ["avatar.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_account_id"],
            ["user_account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_account_id", "jid"),
        sa.UniqueConstraint("user_account_id", "legacy_id"),
    )
    op.create_table(
        "legacy_ids_multi",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_account_id", sa.Integer(), nullable=False),
        sa.Column("legacy_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_account_id"],
            ["user_account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "legacy_ids_multi_user_account_id_legacy_id",
        "legacy_ids_multi",
        ["user_account_id", "legacy_id"],
        unique=True,
    )
    op.create_table(
        "room",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_account_id", sa.Integer(), nullable=False),
        sa.Column("legacy_id", sa.String(), nullable=False),
        sa.Column("jid", slidge.db.meta.JIDType(), nullable=False),
        sa.Column("avatar_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["avatar_id"],
            ["avatar.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_account_id"],
            ["user_account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("jid"),
        sa.UniqueConstraint("legacy_id"),
    )
    op.create_table(
        "xmpp_to_legacy_ids",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_account_id", sa.Integer(), nullable=False),
        sa.Column("xmpp_id", sa.String(), nullable=False),
        sa.Column("legacy_id", sa.String(), nullable=False),
        sa.Column(
            "type",
            sa.Enum("DM", "GROUP_CHAT", "THREAD", name="xmpptolegacyenum"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_account_id"],
            ["user_account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "xmpp_legacy",
        "xmpp_to_legacy_ids",
        ["user_account_id", "xmpp_id", "legacy_id"],
        unique=True,
    )
    op.create_table(
        "mam",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("stanza_id", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("author_jid", slidge.db.meta.JIDType(), nullable=False),
        sa.Column("stanza", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["room.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_id", "stanza_id"),
    )
    op.create_table(
        "xmpp_ids_multi",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_account_id", sa.Integer(), nullable=False),
        sa.Column("xmpp_id", sa.String(), nullable=False),
        sa.Column("legacy_ids_multi_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["legacy_ids_multi_id"],
            ["legacy_ids_multi.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_account_id"],
            ["user_account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "legacy_ids_multi_user_account_id_xmpp_id",
        "xmpp_ids_multi",
        ["user_account_id", "xmpp_id"],
        unique=True,
    )

    try:
        shutil.rmtree(global_config.HOME_DIR / "slidge_avatars_v2")
    except (FileNotFoundError, AttributeError):
        pass

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "legacy_ids_multi_user_account_id_xmpp_id", table_name="xmpp_ids_multi"
    )
    op.drop_table("xmpp_ids_multi")
    op.drop_table("mam")
    op.drop_index("xmpp_legacy", table_name="xmpp_to_legacy_ids")
    op.drop_table("xmpp_to_legacy_ids")
    op.drop_table("room")
    op.drop_index(
        "legacy_ids_multi_user_account_id_legacy_id", table_name="legacy_ids_multi"
    )
    op.drop_table("legacy_ids_multi")
    op.drop_table("contact")
    op.drop_index(op.f("ix_attachment_url"), table_name="attachment")
    op.drop_index(op.f("ix_attachment_legacy_file_id"), table_name="attachment")
    op.drop_table("attachment")
    op.drop_table("avatar")
    # ### end Alembic commands ###
