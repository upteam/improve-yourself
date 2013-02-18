--
-- Alter table structure for initial object
--

-- ir.module.module
ALTER TABLE ir_module_module ADD COLUMN complexity character varying(32);
ALTER TABLE ir_module_module ADD COLUMN application boolean DEFAULT false;
ALTER TABLE ir_module_module ADD COLUMN "sequence" integer DEFAULT 100;
ALTER TABLE ir_module_module ADD COLUMN auto_install boolean DEFAULT false;
ALTER TABLE ir_module_module ADD COLUMN icon character varying(128);
ALTER TABLE ir_module_module ALTER COLUMN web SET DEFAULT false;
COMMENT ON COLUMN ir_module_module.web IS NULL;
COMMENT ON COLUMN ir_module_module.license IS NULL;

-- ir.module.category
ALTER TABLE ir_module_category ADD COLUMN "sequence" integer DEFAULT 100;
ALTER TABLE ir_module_category ADD COLUMN visible boolean DEFAULT true;
ALTER TABLE ir_module_category ADD COLUMN description text;
COMMENT ON COLUMN ir_module_category."sequence" IS 'Sequence';
COMMENT ON COLUMN ir_module_category.visible IS 'Visible';
COMMENT ON COLUMN ir_module_category.description IS 'Description';

UPDATE ir_module_module SET certificate = NULL;

--
-- Use fonction to alter structure for OpenERP
--
SELECT migration61.delete_module('sale_delivery_report');
SELECT migration61.delete_module('document_ics');
SELECT migration61.delete_module('report_analytic_planning');
SELECT migration61.delete_module('profile_association');
SELECT migration61.delete_module('project_caldav');
SELECT migration61.delete_module('account_date_check');
SELECT migration61.delete_module('base_report_creator');

--
-- Rename module
--
SELECT migration61.rename_module('thunderbird', 'plugin_thunderbird');
SELECT migration61.rename_module('outlook', 'plugin_outlook');
SELECT migration61.rename_module('mail_gateway', 'mail');

SELECT migration61.check_upgrade();
