"""Migración inicial

Revision ID: bd3425f707ea
Revises: 
Create Date: 2025-03-08 11:09:06.202248

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bd3425f707ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('areas', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('documentos', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.alter_column('actualizado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True)
        batch_op.drop_constraint('documentos_ibfk_4', type_='foreignkey')
        batch_op.drop_constraint('documentos_ibfk_7', type_='foreignkey')
        batch_op.drop_constraint('documentos_ibfk_6', type_='foreignkey')
        batch_op.drop_constraint('documentos_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('documentos_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('documentos_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('documentos_ibfk_5', type_='foreignkey')
        batch_op.create_foreign_key(None, 'areas', ['area_actual_id'], ['id'])
        batch_op.create_foreign_key(None, 'tipos_documento', ['tipo_documento_id'], ['id'])
        batch_op.create_foreign_key(None, 'personas', ['persona_actual_id'], ['id'])
        batch_op.create_foreign_key(None, 'usuarios', ['usuario_actualizacion_id'], ['id'])
        batch_op.create_foreign_key(None, 'transportadoras', ['transportadora_id'], ['id'])
        batch_op.create_foreign_key(None, 'estados_documento', ['estado_id'], ['id'])
        batch_op.create_foreign_key(None, 'usuarios', ['usuario_creacion_id'], ['id'])

    with op.batch_alter_table('estados_documento', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('historial_movimientos', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.drop_constraint('historial_movimientos_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('historial_movimientos_ibfk_4', type_='foreignkey')
        batch_op.drop_constraint('historial_movimientos_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('historial_movimientos_ibfk_5', type_='foreignkey')
        batch_op.drop_constraint('historial_movimientos_ibfk_7', type_='foreignkey')
        batch_op.drop_constraint('historial_movimientos_ibfk_6', type_='foreignkey')
        batch_op.drop_constraint('historial_movimientos_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'areas', ['area_origen_id'], ['id'])
        batch_op.create_foreign_key(None, 'documentos', ['documento_id'], ['id'])
        batch_op.create_foreign_key(None, 'areas', ['area_destino_id'], ['id'])
        batch_op.create_foreign_key(None, 'personas', ['persona_destino_id'], ['id'])
        batch_op.create_foreign_key(None, 'personas', ['persona_origen_id'], ['id'])
        batch_op.create_foreign_key(None, 'estados_documento', ['estado_id'], ['id'])
        batch_op.create_foreign_key(None, 'usuarios', ['usuario_id'], ['id'])

    with op.batch_alter_table('personas', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.drop_constraint('personas_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'areas', ['area_id'], ['id'])

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('tipos_documento', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('transportadoras', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('ultimo_acceso',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True)
        batch_op.alter_column('creado_en',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.drop_constraint('usuarios_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('usuarios_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'personas', ['persona_id'], ['id'])
        batch_op.create_foreign_key(None, 'roles', ['rol_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('usuarios_ibfk_2', 'roles', ['rol_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('usuarios_ibfk_1', 'personas', ['persona_id'], ['id'], ondelete='RESTRICT')
        batch_op.alter_column('creado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.alter_column('ultimo_acceso',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True)

    with op.batch_alter_table('transportadoras', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('tipos_documento', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('personas', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('personas_ibfk_1', 'areas', ['area_id'], ['id'], ondelete='RESTRICT')
        batch_op.alter_column('creado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('historial_movimientos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('historial_movimientos_ibfk_3', 'personas', ['persona_origen_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('historial_movimientos_ibfk_6', 'estados_documento', ['estado_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('historial_movimientos_ibfk_7', 'usuarios', ['usuario_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('historial_movimientos_ibfk_5', 'personas', ['persona_destino_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('historial_movimientos_ibfk_1', 'documentos', ['documento_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('historial_movimientos_ibfk_4', 'areas', ['area_destino_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('historial_movimientos_ibfk_2', 'areas', ['area_origen_id'], ['id'], ondelete='RESTRICT')
        batch_op.alter_column('creado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('estados_documento', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('documentos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('documentos_ibfk_5', 'estados_documento', ['estado_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('documentos_ibfk_3', 'areas', ['area_actual_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('documentos_ibfk_2', 'tipos_documento', ['tipo_documento_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('documentos_ibfk_1', 'transportadoras', ['transportadora_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('documentos_ibfk_6', 'usuarios', ['usuario_creacion_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('documentos_ibfk_7', 'usuarios', ['usuario_actualizacion_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_foreign_key('documentos_ibfk_4', 'personas', ['persona_actual_id'], ['id'], ondelete='RESTRICT')
        batch_op.alter_column('actualizado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True)
        batch_op.alter_column('creado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('areas', schema=None) as batch_op:
        batch_op.alter_column('creado_en',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    # ### end Alembic commands ###
