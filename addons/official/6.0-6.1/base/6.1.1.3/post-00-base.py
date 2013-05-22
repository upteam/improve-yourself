# -*- coding: utf-8 -*-
##############################################################################
#
#    migration module for OpenERP, Script to migrate version
#    Copyright (C) 2012 UPTEAM (<http://github.com/upteam/improve-yourself>) Christophe CHAUVET
#
#    This file is a part of migration
#
#    migration is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    migration is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import sys
import logging
logger = logging.getLogger('migration.base')


def table_exists(cr, tablename):
    """
    Return True if table exists
    """
    cr.execute("""SELECT * FROM pg_tables WHERE tablename=%s;""", (tablename,))
    if cr.fetchone():
        return True
    return False


def table_columns_exists(cr, tablename, columns):
    """
    Return true if columsn exists on the table
    """
    cr.execute("""SELECT * FROM information_schema.columns WHERE table_name =%s AND column_name=%s;""", (tablename, columns))
    if cr.fetchone():
        return True
    return False


def migrate(cr, v):
    """
    Premier script en point d'entrée.
    """
    logger.info('Update partner and rights configuration')
    # update ir_act_server set action_id = null where ...
    if table_columns_exists(cr, 'res_partner_address', 'address_id'):
        cr.execute("""update res_users set user_email=rpa.email from res_partner_address rpa where address_id=rpa.id""")

    cr.execute("""UPDATE ir_model_access SET group_id = NULL FROM ir_model_data imd WHERE imd.res_id = ir_model_access.id AND imd.model=E'ir.model.access'
                  AND imd.name=E'access_ir_module_category_group_user'""")
    cr.execute("""DELETE FROM ir_model where id = (select res_id from ir_model_data where module = E'base_setup' and model = E'ir.model' and name = E'model_base_setup_config')""")
    cr.execute("""DELETE FROM ir_model_data where module = E'base_setup' and model = E'ir.model' and name = E'model_base_setup_config'""")
    cr.execute("""DELETE FROM ir_model_fields WHERE id = (SELECT res_id from ir_model_data where module = E'base_setup' and model = E'ir.model.fields'
                  AND name = E'field_base_setup_config_installed_users')""")
    cr.execute("""DELETE FROM ir_model_data where module = E'base_setup' and model = E'ir.model.fields' and name = E'field_base_setup_config_installed_users'""")
    cr.execute("""DELETE FROM ir_model_fields where id = (SELECT res_id from ir_model_data where module = E'base_setup' and model = E'ir.model.fields'
                                                          and name = E'field_base_setup_config_config_logo')""")
    cr.execute("""DELETE FROM ir_model_data where module = E'base_setup' and model = E'ir.model.fields' and name = E'field_base_setup_config_config_logo'""")
    cr.execute("""delete from ir_ui_view where id = (select res_id from ir_model_data where module = E'base_setup' and model = E'ir.ui.view' and name = E'view_base_setup')""")
    cr.execute("""delete from ir_model_data where module = E'base_setup' and model = E'ir.ui.view' and name = E'view_base_setup'""")
    cr.execute("""delete from ir_act_window where id = (SELECT res_id from ir_model_data where module = E'base_setup' and model = E'ir.actions.act_window' and name = E'action_base_setup')""")
    cr.execute("""delete from ir_model_data where module = E'base_setup' and model = E'ir.actions.act_window' and name = E'action_base_setup'""")
    # TODO check this
    # update res_users set menu_id = 1 where menu_id = 85
    cr.execute("""update ir_sequence_type t set code = t.code || '(' || t.id || ')' where code='crm.case'""")

    # Delete all bad reference from
    cr.execute("""DELETE FROM ir_values WHERE id in (
                  select ir_values.id
                  from ir_values
                  left join ir_act_window win on (win.id = replace(value, 'ir.actions.act_window,', '')::integer)
                  where key2='client_action_relate'
                  and win.id IS NULL)""")

    # Suppression des wizard supprimés
    cr.execute("""DELETE FROM ir_values
                  WHERE id IN (select ir_values.id
                  from ir_values
                  left join ir_act_window win on (win.id = replace(value, 'ir.actions.act_window,', '')::integer)
                  where key2='client_action_multi'
                  and value like 'ir.actions.act_window,%'
                  and win.id IS NULL)""")

    cr.execute("""DELETE FROM ir_values WHERE id IN (
                        select ir_values.id
                        from ir_values
                        left join ir_act_window win on (win.id = replace(value, 'ir.actions.server,', '')::integer)
                        where key2='client_action_multi'
                        and value like 'ir.actions.server,%'
                        and win.id IS NULL)""")

    cr.commit()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
