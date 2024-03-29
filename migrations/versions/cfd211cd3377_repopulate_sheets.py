"""repopulate sheets

Revision ID: cfd211cd3377
Revises: c83142b32570
Create Date: 2021-11-28 13:09:44.385518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfd211cd3377'
down_revision = '6f7ad716ca2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('beatcops_weapon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('weapon_type', sa.String(length=128), nullable=True),
    sa.Column('bonus', sa.Integer(), nullable=True),
    sa.Column('damage', sa.String(length=128), nullable=True),
    sa.Column('mag', sa.Integer(), nullable=True),
    sa.Column('weapon_range', sa.String(length=128), nullable=True),
    sa.Column('attribute', sa.String(length=128), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shootout_weapon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('weapon_type', sa.String(length=128), nullable=True),
    sa.Column('bonus', sa.Integer(), nullable=True),
    sa.Column('damage', sa.String(length=128), nullable=True),
    sa.Column('mag', sa.Integer(), nullable=True),
    sa.Column('weapon_range', sa.String(length=128), nullable=True),
    sa.Column('attribute', sa.String(length=128), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('swn_weapon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('weapon_type', sa.String(length=128), nullable=True),
    sa.Column('bonus', sa.Integer(), nullable=True),
    sa.Column('damage', sa.String(length=128), nullable=True),
    sa.Column('mag', sa.Integer(), nullable=True),
    sa.Column('weapon_range', sa.String(length=128), nullable=True),
    sa.Column('attribute', sa.String(length=128), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('beatcops_sheet',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('character_class', sa.String(length=128), nullable=True),
    sa.Column('background', sa.String(length=128), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('xp', sa.Integer(), nullable=True),
    sa.Column('max_hp', sa.Integer(), nullable=True),
    sa.Column('current_hp', sa.Integer(), nullable=True),
    sa.Column('system_strain', sa.Integer(), nullable=True),
    sa.Column('ac', sa.Integer(), nullable=True),
    sa.Column('mental_save', sa.Integer(), nullable=True),
    sa.Column('evasion_save', sa.Integer(), nullable=True),
    sa.Column('physical_save', sa.Integer(), nullable=True),
    sa.Column('strength', sa.Integer(), nullable=True),
    sa.Column('dexterity', sa.Integer(), nullable=True),
    sa.Column('constitution', sa.Integer(), nullable=True),
    sa.Column('intelligence', sa.Integer(), nullable=True),
    sa.Column('wisdom', sa.Integer(), nullable=True),
    sa.Column('charisma', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_update', sa.DateTime(), nullable=False),
    sa.Column('administer', sa.Integer(), nullable=True),
    sa.Column('animal_handling', sa.Integer(), nullable=True),
    sa.Column('connect', sa.Integer(), nullable=True),
    sa.Column('drive', sa.Integer(), nullable=True),
    sa.Column('exert', sa.Integer(), nullable=True),
    sa.Column('fix', sa.Integer(), nullable=True),
    sa.Column('heal', sa.Integer(), nullable=True),
    sa.Column('investigate', sa.Integer(), nullable=True),
    sa.Column('know', sa.Integer(), nullable=True),
    sa.Column('lead', sa.Integer(), nullable=True),
    sa.Column('notice', sa.Integer(), nullable=True),
    sa.Column('perform', sa.Integer(), nullable=True),
    sa.Column('punch', sa.Integer(), nullable=True),
    sa.Column('program', sa.Integer(), nullable=True),
    sa.Column('requisition', sa.Integer(), nullable=True),
    sa.Column('search', sa.Integer(), nullable=True),
    sa.Column('shoot', sa.Integer(), nullable=True),
    sa.Column('stealth', sa.Integer(), nullable=True),
    sa.Column('strike', sa.Integer(), nullable=True),
    sa.Column('survive', sa.Integer(), nullable=True),
    sa.Column('talk', sa.Integer(), nullable=True),
    sa.Column('work', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shootout_sheet',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('character_class', sa.String(length=128), nullable=True),
    sa.Column('background', sa.String(length=128), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('xp', sa.Integer(), nullable=True),
    sa.Column('max_hp', sa.Integer(), nullable=True),
    sa.Column('current_hp', sa.Integer(), nullable=True),
    sa.Column('system_strain', sa.Integer(), nullable=True),
    sa.Column('ac', sa.Integer(), nullable=True),
    sa.Column('mental_save', sa.Integer(), nullable=True),
    sa.Column('evasion_save', sa.Integer(), nullable=True),
    sa.Column('physical_save', sa.Integer(), nullable=True),
    sa.Column('strength', sa.Integer(), nullable=True),
    sa.Column('dexterity', sa.Integer(), nullable=True),
    sa.Column('constitution', sa.Integer(), nullable=True),
    sa.Column('intelligence', sa.Integer(), nullable=True),
    sa.Column('wisdom', sa.Integer(), nullable=True),
    sa.Column('charisma', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_update', sa.DateTime(), nullable=False),
    sa.Column('administer', sa.Integer(), nullable=True),
    sa.Column('cast_magic', sa.Integer(), nullable=True),
    sa.Column('connect', sa.Integer(), nullable=True),
    sa.Column('exert', sa.Integer(), nullable=True),
    sa.Column('fix', sa.Integer(), nullable=True),
    sa.Column('heal', sa.Integer(), nullable=True),
    sa.Column('horsemanship', sa.Integer(), nullable=True),
    sa.Column('know', sa.Integer(), nullable=True),
    sa.Column('know_magic', sa.Integer(), nullable=True),
    sa.Column('lead', sa.Integer(), nullable=True),
    sa.Column('notice', sa.Integer(), nullable=True),
    sa.Column('perform', sa.Integer(), nullable=True),
    sa.Column('punch', sa.Integer(), nullable=True),
    sa.Column('sail', sa.Integer(), nullable=True),
    sa.Column('shoot', sa.Integer(), nullable=True),
    sa.Column('sneak', sa.Integer(), nullable=True),
    sa.Column('stab', sa.Integer(), nullable=True),
    sa.Column('survive', sa.Integer(), nullable=True),
    sa.Column('talk', sa.Integer(), nullable=True),
    sa.Column('trade', sa.Integer(), nullable=True),
    sa.Column('work', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('swn_sheet',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('character_class', sa.String(length=128), nullable=True),
    sa.Column('background', sa.String(length=128), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('xp', sa.Integer(), nullable=True),
    sa.Column('max_hp', sa.Integer(), nullable=True),
    sa.Column('current_hp', sa.Integer(), nullable=True),
    sa.Column('system_strain', sa.Integer(), nullable=True),
    sa.Column('ac', sa.Integer(), nullable=True),
    sa.Column('mental_save', sa.Integer(), nullable=True),
    sa.Column('evasion_save', sa.Integer(), nullable=True),
    sa.Column('physical_save', sa.Integer(), nullable=True),
    sa.Column('strength', sa.Integer(), nullable=True),
    sa.Column('dexterity', sa.Integer(), nullable=True),
    sa.Column('constitution', sa.Integer(), nullable=True),
    sa.Column('intelligence', sa.Integer(), nullable=True),
    sa.Column('wisdom', sa.Integer(), nullable=True),
    sa.Column('charisma', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_update', sa.DateTime(), nullable=False),
    sa.Column('administer', sa.Integer(), nullable=True),
    sa.Column('connect', sa.Integer(), nullable=True),
    sa.Column('exert', sa.Integer(), nullable=True),
    sa.Column('fix', sa.Integer(), nullable=True),
    sa.Column('heal', sa.Integer(), nullable=True),
    sa.Column('know', sa.Integer(), nullable=True),
    sa.Column('lead', sa.Integer(), nullable=True),
    sa.Column('notice', sa.Integer(), nullable=True),
    sa.Column('perform', sa.Integer(), nullable=True),
    sa.Column('pilot', sa.Integer(), nullable=True),
    sa.Column('program', sa.Integer(), nullable=True),
    sa.Column('punch', sa.Integer(), nullable=True),
    sa.Column('shoot', sa.Integer(), nullable=True),
    sa.Column('sneak', sa.Integer(), nullable=True),
    sa.Column('stab', sa.Integer(), nullable=True),
    sa.Column('survive', sa.Integer(), nullable=True),
    sa.Column('talk', sa.Integer(), nullable=True),
    sa.Column('trade', sa.Integer(), nullable=True),
    sa.Column('work', sa.Integer(), nullable=True),
    sa.Column('biopsionics', sa.Integer(), nullable=True),
    sa.Column('metapsionics', sa.Integer(), nullable=True),
    sa.Column('precognition', sa.Integer(), nullable=True),
    sa.Column('telekinesis', sa.Integer(), nullable=True),
    sa.Column('telepathy', sa.Integer(), nullable=True),
    sa.Column('teleportation', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('beatcops_weapon_identifier',
    sa.Column('sheet_id', sa.Integer(), nullable=True),
    sa.Column('weapon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sheet_id'], ['beatcops_sheet.id'], ),
    sa.ForeignKeyConstraint(['weapon_id'], ['beatcops_weapon.id'], )
    )
    op.create_table('shootout_weapon_identifier',
    sa.Column('sheet_id', sa.Integer(), nullable=True),
    sa.Column('weapon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sheet_id'], ['shootout_sheet.id'], ),
    sa.ForeignKeyConstraint(['weapon_id'], ['shootout_weapon.id'], )
    )
    op.create_table('swn_weapon_identifier',
    sa.Column('sheet_id', sa.Integer(), nullable=True),
    sa.Column('weapon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sheet_id'], ['swn_sheet.id'], ),
    sa.ForeignKeyConstraint(['weapon_id'], ['swn_weapon.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('swn_weapon_identifier')
    op.drop_table('shootout_weapon_identifier')
    op.drop_table('beatcops_weapon_identifier')
    op.drop_table('swn_sheet')
    op.drop_table('shootout_sheet')
    op.drop_table('beatcops_sheet')
    op.drop_table('swn_weapon')
    op.drop_table('shootout_weapon')
    op.drop_table('beatcops_weapon')
    # ### end Alembic commands ###
