"""First revision

Revision ID: d4867f3a4c0a
Revises:
Create Date: 2019-04-17 13:53:32.978401

"""
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.operators import as_
from sqlalchemy.sql.sqltypes import DateTime
import uuid


# revision identifiers, used by Alembic.
revision = "d4867f3a4c0a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ##########
    ## Core ##
    ##########

    op.create_table(
        "user",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False,),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("email", sa.String(60), nullable=False),
        sa.Column("full_name", sa.String(length=60), nullable=False),
        sa.Column("phone_number", sa.Integer, nullable=True),
        sa.Column("is_superuser", sa.Boolean, server_default=text("False")),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "competition",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(20), nullable=False),
        sa.Column("region", sa.String(20), nullable=False),
        sa.Column("date", sa.Date, nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "team",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False,),
        sa.Column("name", sa.String(60), nullable=False),
        sa.Column("organisation", sa.String(60),),
        # sa.Column("registered_division", sa.String(100), nullable=False),
        # sa.Column("uuid_challenge_division", sa.String(13), server_default=text("NULL")),
        sa.Column("num_member", sa.Integer, server_default=text("2")),
        sa.Column("team_present", sa.Integer, server_default=text("0")),
        # sa.Column(
        #     "uuid_challenge_division",
        #     sa.String,
        #     server_default=text("Not Complete"),
        #     nullable=False,
        # ),
        sa.Column("interview_comments", sa.Text),
        # sa.Column(
        #     "interview_status",
        #     sa.String(length=50),
        #     server_default=text("Not Complete"),
        #     nullable=False,
        # ),
        sa.Column(
            "uuid_mentor", UUID(as_uuid=True), nullable=True
        ),
        sa.Column("uuid_competition", UUID(as_uuid=True), nullable=True),
        sa.Column("hardware_type", sa.String(64), nullable=False),
        sa.Column("software_type", sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        sa.ForeignKeyConstraint(["uuid_mentor"], ["user.uuid"]),
        sa.ForeignKeyConstraint(["uuid_competition"], ["competition.uuid"]),

    )

    op.create_table(
        "team_member",
        sa.Column(
            "uuid",
            UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "uuid_team", UUID(as_uuid=True), nullable=False
        ),
        sa.Column("role", sa.String(length=10), nullable=True),
        # sa.Column("competition", UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        sa.ForeignKeyConstraint(["uuid"], ["user.uuid"]),
        sa.ForeignKeyConstraint(["uuid_team"], ["team.uuid"]),

    )



    ############
    ## Awards ##
    ############

    op.create_table(
        "award_types",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        # sa.Column("for_challenge", sa.Text, nullable=False),
        sa.Column("being_given", sa.Integer, nullable=False),
        sa.Column("description", sa.Text, server_default=text("NULL")),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "awards",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        # sa.Column("uuid_challenge_division", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_team", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_award_type", UUID(as_uuid=True), nullable=False),
        sa.Column("comment", sa.Text, server_default=text("NULL")),
        sa.PrimaryKeyConstraint("uuid"),
        sa.ForeignKeyConstraint(["uuid_team"], ["team.uuid"]),
        sa.ForeignKeyConstraint(["uuid_award_type"], ["award_type.uuid"]),
    )

    # #############
    # ## OnStage ##
    # #############

    op.create_table(
        "onstage_round_type",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("round_name", sa.String(50), nullable=False),
        sa.Column("round_type", sa.String(50), nullable=False),
        sa.Column("sort_order", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "onstage_round",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_onstage_round_type", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_challenge_division", UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        sa.ForeignKeyConstraint(["uuid_onstage_round_type"], ["onstage_round_type.uuid"]),
    )

    op.create_table(
        "onstage_interview",
        sa.Column(
            "uuid", UUID(as_uuid=True), nullable=False
        ),
        sa.Column("uuid_team",  UUID(as_uuid=True), nullable=False),
        sa.Column("competition", sa.Integer, nullable=False),
        sa.Column("score", sa.Integer, nullable=False),
        sa.Column("data", sa.JSON, nullable=False),
        sa.Column("comment", sa.Text, nullable=True),
        sa.Column("timesamp", sa.DateTime, nullable=False, server_default=func.now()),
        sa.PrimaryKeyConstraint("uuid"),
        sa.ForeignKeyConstraint(["uuid_team"], ["team.uuid"]),
    )

    op.create_table(
        "onstage_performance",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_team", UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(64), server_default=text("NULL")),
        sa.Column("score", sa.String(32), nullable=False),
        sa.Column("data", sa.String(1028), nullable=False),
        sa.Column("comment", sa.String(1000), server_default=text("NULL")),
        sa.Column(
            "timestamp",
            sa.DateTime,
            nullable=False,
            server_default=func.current_timestamp(),
        ),
        sa.Column("uuid_onstage_round", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_user", UUID(as_uuid=True), nullable=False),
        sa.Column("dnc", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        sa.ForeignKeyConstraint(["uuid_team"], ["team.uuid"]),
        sa.ForeignKeyConstraint(["uuid_onstage_round"], ["onstage_round.uuid"]),
    )

    op.create_table(
        "onstage_scoresheet_categories",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("type", sa.String(13), nullable=False),
        sa.Column("division", sa.String(13), nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("step", sa.String(16), nullable=False, server_default=text("1")),
        sa.Column("sort_order", sa.String(8), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "onstage_scoresheet_criteria",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("descriptor", sa.String(13), nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("points", sa.String(64), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "onstage_scoresheet_descriptors",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False,),
        sa.Column("category", sa.String(13), nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("sort_order", sa.String(8), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    # ############
    # ## Rescue ##
    # ############

    op.create_table(
        "rescue_round_type",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("round_type", sa.String(50), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "rescue_round",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_rescue_round_type", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_challenge_division", UUID(as_uuid=True), nullable=False),
        sa.Column("max_time", sa.String(13), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "rescue_course_setups",
        sa.Column("uuid_rescue_round", UUID(as_uuid=True), nullable=False),
        sa.Column("level0", sa.Text(), nullable=False),
        sa.Column("level1", sa.Text(), nullable=False),
        sa.Column("level0_starts", sa.Text(), nullable=False),
        sa.Column("level1_starts", sa.Text(), nullable=False),
        sa.Column("level0_capsules", sa.Text(), nullable=False),
        sa.Column("level1_capsules", sa.Text(), nullable=False),
        sa.Column("ramps", sa.Text(), nullable=False),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("uuid_rescue_round"),
    )

    op.create_table(
        "rescue_result",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_rescue_round", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_team", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_referee", UUID(as_uuid=True), nullable=False),
        sa.Column("gross_time", sa.Time, nullable=False),
        sa.Column("touch", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime, server_default=func.current_timestamp()),
        sa.Column(
            "total_raw_score", sa.Integer(), nullable=False, server_default=text("0")
        ),
        sa.Column("referee", UUID(as_uuid=True), nullable=False),
        sa.Column("approval_type", sa.Integer(), nullable=True),
        sa.Column("dnc", sa.Integer(), nullable=False),
        sa.Column("comment", sa.String(1000), nullable=True),
        sa.Column("status", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "rescue_result_tile",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_rescue_result", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_tile_round", UUID(as_uuid=True), nullable=False),
        sa.Column("points_a", sa.Integer(), nullable=False, server_default=text("0")),
        sa.Column("points_b", sa.Integer(), nullable=False, server_default=text("0")),
        sa.Column("points_c", sa.Integer(), nullable=False, server_default=text("0")),
        sa.Column("points_d", sa.Integer(), nullable=False, server_default=text("0")),
        sa.Column("points_e", sa.Integer(), nullable=False, server_default=text("0")),
        sa.Column("points_f", sa.Integer(), nullable=False, server_default=text("0")),
        sa.Column("points_g", sa.Integer(), nullable=False, server_default=text("0")),
        sa.Column("points_h", sa.Integer(), nullable=False, server_default=text("0")),
        sa.Column("points_i", sa.Integer(), nullable=False, server_default=text("0")),
        sa.Column("points_j", sa.Integer(), nullable=False, server_default=text("0")),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "rescue_tile",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("tile_name", sa.String(50), nullable=False),
        sa.Column("tile_description", sa.Text(), nullable=False),
        sa.Column("image_name", sa.Text, nullable=False),
        sa.Column("points_a", sa.Integer(), nullable=False),
        sa.Column("points_b", sa.Integer(), nullable=False),
        sa.Column("points_c", sa.Integer(), nullable=False),
        sa.Column("points_d", sa.Integer(), nullable=False),
        sa.Column("points_e", sa.Integer(), nullable=False),
        sa.Column("points_f", sa.Integer(), nullable=False),
        sa.Column("points_g", sa.Integer(), nullable=False),
        sa.Column("points_h", sa.Integer(), nullable=False),
        sa.Column("points_i", sa.Integer(), nullable=False),
        sa.Column("points_j", sa.Integer(), nullable=False),
        sa.Column("tile_rule", sa.String(16), nullable=False),
        sa.Column("tags", sa.String(400), nullable=False),
        sa.Column("hidden", sa.Integer(), nullable=False),
        sa.Column("is_child", sa.Integer(), nullable=False),
        sa.Column("parent_debris", sa.String(16), nullable=False),
        sa.Column("parent_obstacle", sa.String(16), nullable=False),
        sa.Column("scoring_tips", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "rescue_tile_tag",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(64), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    op.create_table(
        "rescue_tile_round",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_rescue_round", UUID(as_uuid=True), nullable=False),
        sa.Column("uuid_rescue_tile", UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )


def downgrade():
    op.drop_table("user")
    op.drop_table("competition")
    op.drop_table("team")
    op.drop_table("team_member")
    op.drop_table("award_types")
    op.drop_table("awards")
    op.drop_table("onstage_interview")
    op.drop_table("onstage_performance")
    op.drop_table("onstage_scoresheet_categories")
    op.drop_table("onstage_scoresheet_criteria")
    op.drop_table("onstage_scoresheet_descriptors")
    op.drop_table("onstage_round")
    op.drop_table("rescue_course_setups")
    op.drop_table("rescue_result")
    op.drop_table("rescue_result_tile")
    op.drop_table("rescue_round")
    op.drop_table("rescue_round_type")
    op.drop_table("rescue_tile")
    op.drop_table("rescue_tile_tag")
    op.drop_table("rescue_tile_round")
