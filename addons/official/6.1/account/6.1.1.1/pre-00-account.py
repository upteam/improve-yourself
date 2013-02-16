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

def migrate(cr, v):
    """
    Premier script en point d'entrée.
    """

    logger.info('Alter account structure')
    #cr.execute("""update ir_actions_todo set state='done' where ...""")
    cr.execute("""UPDATE ir_model SET model='account.analytic.journal.report' WHERE model='account.analytic.Journal.report'""")
    # TODO check this, and be carefull with multi-company
    #cr.execute("""update account_invoice set partner_bank_id = ( select id from res_partner_bank where ...""")

    # Tax name is unique per company
    if table_exists(cr, 'account_tax'):
        cr.execute("""UPDATE account_tax SET name = substring(name from 1 for 60) || ' [' ||company_id || ']' """)
        cr.commit()

    if table_exists(cr, 'account_bank_statement_line_move_rel'):
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel drop constraint account_bank_statement_line_move_rel_statement_id_fkey""")
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel drop constraint account_bank_statement_line_move_rel_move_id_fkey""")
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel rename column move_id to statment_line_id_old""")
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel rename column statement_id to move_id_old""")
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel add column move_id integer""")
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel add column statement_line_id integer""")
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel add constraint account_bank_statement_line_move_rel_move_id_fkey
                                  foreign key (move_id) references account_move(id) on delete cascade""")
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel add constraint account_bank_statement_line_move_rel_statement_id_fkey
                                  foreign key (statement_line_id) references account_bank_statement_line(id) on delete cascade""")
        cr.execute("""UPDATE account_bank_statement_line_move_rel set statement_line_id=statment_line_id_old""")
        cr.execute("""UPDATE account_bank_statement_line_move_rel set move_id=move_id_old""")
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel drop column move_id_old""")
        cr.execute("""ALTER TABLE account_bank_statement_line_move_rel drop column statment_line_id_old""")
        cr.execute("""CREATE INDEX account_bank_statement_line_move_rel_move_id_index on account_bank_statement_line_move_rel (move_id)""")
        cr.execute("""CREATE INDEX account_bank_statement_line_move_rel_statement_id_index on account_bank_statement_line_move_rel (statement_line_id)""")
        cr.commit()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
