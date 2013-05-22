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

import logging
logger = logging.getLogger('migration.crm')


def migrate(cr, v):
    """
    """
    logger.info('Unlink group for crm module from ir_model_data')

    cr.execute("""UPDATE res_groups SET name='OLD / '||name WHERE id = (SELECT res_id FROM ir_model_data WHERE module='crm' AND name='group_crm_manager')""")
    cr.execute("""DELETE FROM ir_model_data WHERE module='crm' AND name='group_crm_manager'""")
    cr.execute("""UPDATE res_groups SET name='OLD / '||name WHERE id = (SELECT res_id FROM ir_model_data WHERE module='crm' AND name='group_crm_user')""")
    cr.execute("""DELETE FROM ir_model_data WHERE module='crm' AND name='group_crm_user'""")
    cr.commit()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
