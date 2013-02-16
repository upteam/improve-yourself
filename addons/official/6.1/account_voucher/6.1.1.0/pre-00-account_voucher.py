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
logger = logging.getLogger('migration.account_voucher')

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

    logger.info('Alter account_voucher structure')
    cr.execute("""ALTER TABLE res_company ADD COLUMN income_currency_exchange_account_id integer;""")
    cr.execute("""ALTER TABLE res_company ADD CONSTRAINT res_company_income_currency_exchange_account_id_fkey
                                          FOREIGN KEY (income_currency_exchange_account_id)
                                          REFERENCES res_company (id) ON DELETE SET NULL;""")
    cr.execute("""ALTER TABLE res_company ADD COLUMN expense_currency_exchange_account_id integer;""")
    cr.execute("""ALTER TABLE res_company ADD CONSTRAINT res_company_expense_currency_exchange_account_id_fkey
                                          FOREIGN KEY (expense_currency_exchange_account_id)
                                          REFERENCES res_company (id) ON DELETE SET NULL;""")
    cr.commit()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
