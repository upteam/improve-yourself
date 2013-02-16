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

    if not table_exists(cr, 'ir_act_client'):
        logger.info('Add table ir_act_client')
        cr.execute("""CREATE TABLE ir_act_client ( primary key(id) ) INHERITS (ir_actions);""")
        cr.commit()

    # TODO: Identify this
    # delete from ir_ui_view_sc where ...
    # update ir_model_data set model = 'ir.actions.report.xml' where ...

    if table_exists(cr, 'mailgate_message'):
        logger.info('Alter mailgate message')
        cr.execute("""ALTER SEQUENCE mailgate_message_id_seq RENAME TO mail_message_id_seq;""")
        cr.execute("""ALTER INDEX "mailgate_message_pkey" RENAME TO "mail_message_pkey"; """)
        cr.execute("""ALTER INDEX "mailgate_message_message_id_index" RENAME TO "mail_message_message_id_index"; """)
        cr.execute("""alter index "mailgate_message_model_index" RENAME TO "mail_message_model_index"; """)
        cr.execute("""alter index "mailgate_message_ref_id_index" RENAME TO "mail_message_ref_id_index"; """)
        cr.execute("""alter index "mailgate_message_res_id_index" RENAME TO "mail_message_res_id_index"; """)
        cr.execute("""alter index "mailgate_message_res_id_model_idx" rename to "mail_message_res_id_model_idx"; """)
        cr.execute("""alter index "mailgate_message_server_id_index" rename to "mail_message_server_id_index"; """)
        cr.execute("""alter index "mailgate_message_server_type_index" rename to "mail_message_server_type_index"; """)
        cr.execute("""alter table mailgate_message drop constraint "mailgate_message_write_uid_fkey"; """)
        cr.execute("""alter table mailgate_message add constraint "mail_message_write_uid_fkey" foreign key (write_uid) references res_users(id) on delete set null""")
        cr.execute("""alter table mailgate_message drop constraint "mailgate_message_user_id_fkey" """)
        cr.execute("""alter table mailgate_message add constraint "mail_message_user_id_fkey" foreign key (user_id) references res_users(id) on delete set null""")
        cr.execute("""alter table mailgate_message drop constraint "mailgate_message_server_id_fkey";""")
        cr.execute("""alter table mailgate_message add constraint "mail_message_server_id_fkey" foreign key (server_id) references email_server(id) on delete set null""")
        cr.execute("""alter table mailgate_message drop constraint "mailgate_message_partner_id_fkey";""")
        cr.execute("""alter table mailgate_message add constraint "mail_message_partner_id_fkey" foreign key (partner_id) references res_partner(id) on delete set null""")
        cr.execute("""alter table mailgate_message drop constraint "mailgate_message_create_uid_fkey";""")
        cr.execute("""alter table mailgate_message add constraint "mail_message_create_uid_fkey" foreign key (create_uid) references res_users(id) on delete set null""")
        cr.execute("""alter table mailgate_message rename to mail_message""")
        cr.commit()

    if table_exists(cr, 'mail_message'):
        cr.execute("""UPDATE ir_model set model=E'mail.message' where model=E'mailgate.message' """)
        cr.execute("""UPDATE ir_model_data set model=E'mail.message' where model=E'mailgate.message' """)
        cr.execute("""UPDATE ir_attachment set res_model=E'mail.message' where res_model=E'mailgate.message' """)
        cr.execute("""alter table mail_message rename column name to subject""")
        cr.execute("""alter table mail_message rename column description to body_text""")
        cr.execute("""alter table mail_message add column reply_to character varying(256)""")
        cr.execute("""alter table mail_message add column body_html text""")
        cr.execute("""alter table mail_message add column mail_server_id integer""")
        cr.execute("""alter table mail_message add column state character varying(16)""")
        cr.execute("""alter table mail_message add column subtype character varying(16)""")
        cr.execute("""UPDATE mail_message SET subject=E'' WHERE subject IS NULL""")
        cr.execute("""alter sequence mailgate_thread_id_seq rename to mail_thread_id_seq""")
        cr.execute("""alter index "mailgate_thread_pkey" rename to "mail_thread_pkey";""")
        cr.execute("""alter table mailgate_thread drop constraint "mailgate_thread_write_uid_fkey";""")
        cr.execute("""alter table mailgate_thread add constraint "mail_thread_write_uid_fkey" foreign key (write_uid) references res_users(id) on delete set null""")
        cr.execute("""alter table mailgate_thread drop constraint "mailgate_thread_create_uid_fkey";""")
        cr.execute("""alter table mailgate_thread add constraint "mail_thread_create_uid_fkey" foreign key (create_uid) references res_users(id) on delete set null""")
        cr.execute("""alter table mailgate_thread rename to mail_thread""")
        cr.execute("""UPDATE ir_model set model=E'mail.thread' where model=E'mailgate.thread' """)
        cr.execute("""UPDATE ir_model_data set model=E'mail.thread' where model=E'mailgate.thread' """)
        cr.execute("""UPDATE ir_attachment set res_model=E'mail.thread' where res_model=E'mailgate.thread' """)
        cr.commit()

    # if table email_template_account
    if table_exists(cr, 'email_template_account'):
        cr.execute("""ALTER TABLE email_template RENAME COLUMN def_to to email_to""")
        cr.execute("""ALTER TABLE email_template RENAME COLUMN def_cc to email_cc""")
        cr.execute("""ALTER TABLE email_template RENAME COLUMN def_bcc to email_bcc""")
        cr.execute("""ALTER TABLE email_template RENAME COLUMN def_subject to subject""")
        cr.execute("""ALTER TABLE email_template RENAME COLUMN def_body_text to body_text""")
        cr.execute("""ALTER TABLE email_template RENAME COLUMN def_body_html to body_html""")
        cr.execute("""ALTER TABLE email_template RENAME COLUMN object_name to model_id""")
        cr.execute("""ALTER TABLE email_template_mailbox RENAME COLUMN account_id to mail_server_id""")
        cr.execute("""ALTER TABLE email_template_mailbox RENAME COLUMN date_mail to date""")
        cr.execute("""ALTER TABLE email_template_mailbox DROP COLUMN "state";""")
        cr.execute("""ALTER TABLE email_template_mailbox RENAME COLUMN folder to state""")
        cr.execute("""UPDATE email_template_mailbox SET state=E'outgoing' WHERE state=E'outbox'""")
        cr.execute("""UPDATE email_template_mailbox SET state=E'cancel' WHERE state=E'trash'""")
        cr.execute("""UPDATE email_template_mailbox SET state=E'cancel' WHERE state=E'drafts'""")
        cr.execute("""ALTER TABLE email_template_mailbox RENAME COLUMN mail_type TO subtype""")
        cr.execute("""UPDATE email_template_mailbox SET subtype=E'alternative' WHERE subtype=E'multipart/alternative'""")
        cr.execute("""UPDATE email_template_mailbox SET subtype=E'mixed' WHERE subtype=E'multipart/mixed'""")
        cr.execute("""UPDATE email_template_mailbox SET subtype=E'html' WHERE subtype=E'text/html'""")
        cr.execute("""UPDATE email_template_mailbox SET subtype=E'related' WHERE subtype=E'multipart/related'""")
        cr.execute("""UPDATE email_template_mailbox SET subtype=E'plain' WHERE subtype=E'text/plain'""")
        cr.execute("""ALTER TABLE email_template_mailbox ADD COLUMN user_id int REFERENCES res_users ON DELETE SET NULL""")
        # TODO Check this
        #cr.execute("""update email_template_mailbox set user_id = a.user from email_template_account a where ...""")
        cr.commit()

    if table_exists(cr, 'email_template_mailbox'):
        cr.execute("""ALTER TABLE mail_message ADD COLUMN old_id int""")
        cr.execute("""INSERT INTO mail_message (old_id, create_uid, create_date, write_uid, write_date, subject, email_from, email_to, email_cc,
                                                email_bcc, reply_to, message_id, body_text, body_html, date, mail_server_id, user_id, state, subtype)
                      SELECT id, create_uid, create_date, write_uid, write_date, subject, email_from, email_to, email_cc, email_bcc, reply_to,
                             message_id, body_text, body_html, date, mail_server_id, user_id, state, subtype FROM email_template_mailbox""")
        cr.execute("""ALTER TABLE mail_attachments_rel DROP CONSTRAINT "mail_attachments_rel_mail_id_fkey";""")
        # TODO: Check this
        # cr.execute("""update mail_attachments_rel x set mail_id=m.id from mail_message m where ...""")
        cr.execute("""ALTER TABLE mail_attachments_rel ADD CONSTRAINT "mail_attachments_rel_mail_id_fkey" FOREIGN KEY(mail_id) REFERENCES mail_message(id) ON DELETE CASCADE""")

        # TODO: Made this later
        # UPDATE calendar_alarm x SET res_id = m.id, model_id = 342 FROM mail_message m WHERE x.res_id = m.old_id AND x.model_id = 329
        # UPDATE ir_values x SET res_id = m.id, model_id = 342 FROM mail_message m WHERE x.res_id = m.old_id AND x.model_id = 329
        # DELETE FROM ir_model WHERE id=329

        cr.execute("""UPDATE ir_model_data t SET res_id = m.id, model = E'mail.message' FROM mail_message m WHERE t.model = E'email_template.mailbox' AND t.res_id = m.old_id""")
        cr.execute("""UPDATE ir_attachment t SET res_id = m.id, res_model = E'mail.message' FROM mail_message m WHERE t.res_model = E'email_template.mailbox' AND t.res_id = m.old_id""")
        cr.execute("""insert into message_attachment_rel(message_id, attachment_id) select m.id, a.att_id from mail_attachments_rel a inner join mail_message m on a.mail_id = m.old_id""")
        cr.execute("""drop table mail_attachments_rel cascade""")
        cr.execute("""alter table mail_message drop column "old_id";""")
        cr.execute("""drop table email_template_mailbox cascade""")
        cr.execute("""UPDATE ir_attachment set res_model=E'mail.message' where res_model=E'email_template.mailbox'""")
        cr.execute("""alter table email_template_account drop column "user";""")
        cr.execute("""alter sequence email_template_account_id_seq rename to ir_mail_server_id_seq""")
        cr.execute("""alter index "email_template_account_email_uniq" rename to "ir_mail_server_email_uniq";""")
        cr.execute("""alter index "email_template_account_pkey" rename to "ir_mail_server_pkey";""")
        cr.execute("""alter index "email_template_account_name_index" rename to "ir_mail_server_name_index";""")
        cr.execute("""alter table email_template_account drop constraint "ir_mail_server_email_uniq";""")
        cr.execute("""alter table email_template_account add constraint "ir_mail_server_iq" unique (email_id);""")
        cr.execute("""alter table email_template_account drop constraint "email_template_account_write_uid_fkey";""")
        cr.execute("""alter table email_template_account add constraint "ir_mail_server_write_uid_fkey" foreign key (write_uid) references res_users(id) on delete set null;""")
        cr.execute("""alter table email_template_account drop constraint "email_template_account_create_uid_fkey";""")
        cr.execute("""alter table email_template_account add constraint "ir_mail_server_create_uid_fkey" foreign key (create_uid) references res_users(id) on delete set null""")
        cr.execute("""alter table email_template_account rename to ir_mail_server""")
        cr.execute("""UPDATE ir_model set model=E'ir.mail_server' where model=E'email_template.account'""")
        cr.execute("""UPDATE ir_model_data set model=E'ir.mail_server' where model=E'email_template.account'""")
        cr.execute("""UPDATE ir_attachment set res_model=E'ir.mail_server' where res_model=E'email_template.account'""")
        cr.execute("""alter table ir_mail_server rename column smtpserver to smtp_host""")
        cr.execute("""alter table ir_mail_server rename column smtpport to smtp_port""")
        cr.execute("""alter table ir_mail_server rename column smtpuname to smtp_user""")
        cr.execute("""alter table ir_mail_server rename column smtppass to smtp_pass""")
        cr.execute("""alter table ir_mail_server add column smtp_encryption varchar(16)""")
        cr.execute("""alter table ir_mail_server alter column smtp_encryption set default 'none'""")
        cr.execute("""update ir_mail_server set smtp_encryption = (case when smtptls=true then 'starttls' when smtpssl=true then 'ssl' else 'none' end)""")
        cr.execute("""DELETE FROM wkf_workitem WHERE act_id IN (SELECT id FROM wkf_activity WHERE wkf_id IN (SELECT id FROM wkf WHERE osv=E'email_template.account'))""")
        cr.execute("""DELETE FROM wkf WHERE osv=E'email_template.account'""")

    cr.execute("""UPDATE ir_module_module SET state = 'to install' WHERE name = E'email_template'""")
    cr.execute("""UPDATE ir_module_module SET state = 'to install' WHERE name = E'mail'""")
    cr.execute("""UPDATE ir_module_module SET state = 'to install' WHERE name = E'base_tools'""")
    cr.commit()

    # 2 groups are removed from base modules, we remove reference in ir_model_data
    cr.execute("""DELETE FROM ir_model_data WHERE module='base' AND name='group_maintenance_manager'""")
    cr.execute("""DELETE FROM ir_model_data WHERE module='base' AND name='group_sale_salesman_all_leads'""")
    cr.commit()

    # Remove action from partner wizard removed
    if table_exists(cr, 'ir_model_access'):
        cr.execute("""DELETE FROM ir_act_window WHERE id = (select res_id from ir_model_data where module='base' and name='action_partner_mass_mail')""")
        cr.execute("""DELETE FROM ir_ui_view WHERE model='partner.wizard.spam'""")
        cr.execute("""DELETE FROM ir_model_access WHERE model_id = (SELECT id FROM ir_model WHERE model='partner.wizard.spam')""")
        cr.execute("""DELETE FROM ir_model_fields WHERE model_id = (SELECT id FROM ir_model WHERE model='partner.wizard.spam')""")
        cr.execute("""DELETE FROM ir_model WHERE model='partner.wizard.spam'""")
        cr.execute("""DELETE FROM ir_model_data WHERE module='base' AND name='action_partner_mass_mail'""")
        cr.commit()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
