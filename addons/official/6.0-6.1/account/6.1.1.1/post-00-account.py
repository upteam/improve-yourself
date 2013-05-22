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
logger = logging.getLogger('migration.account')

def table_exists(cr, tablename):
    """
    Return True if table exists
    """
    cr.execute("""SELECT * FROM pg_tables WHERE tablename=%s;""", (tablename,))
    if cr.fetchone():
        return True
    return False

def migrate(cr, v):
    """
    Premier script en point d'entrée.
    """

    logger.info('Alter account structure')


    # delete from ir_model_data where ...
    # delete from ir_model where ...
    # update ir_act_window set view_mode='tree,form' where ...

    # in v6.1 invoices cannot be confirmed if there are some invoices with number = '/'
    cr.execute("""UPDATE account_invoice SET number='//' WHERE number='/';""")

    #
    # avoid duplicated 'period_id' field in journal items tree view
    #
    # delete from account_journal_column where ...
    # delete from ir_values where value in (E'ir.actions.act_window,565', E'ir.actions.act_window,568', E'ir.actions.act_window,561', E'ir.actions.act_window,612', E'ir.actions.act_window,614')
    # delete from ir_act_window where id in (565, 568, 561, 612, 614)
    # delete from ir_ui_menu m where ...
    # delete from ir_values m where ...

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
