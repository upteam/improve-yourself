--
-- rename table
--
ALTER SEQUENCE res_partner_canal_id_seq rename to crm_case_channel_id_seq;
ALTER TABLE res_partner_canal RENAME TO crm_case_channel;
SELECT migration61.rename_model('res.partner.canal', 'crm.case.channel');

--
-- Sequence have now a new type for implementation
--
ALTER TABLE ir_sequence ADD COLUMN implementation varchar(16);
UPDATE ir_sequence SET implementation=E'no_gap';

--
-- field value_boolean have been drop on ir_property, the content is now be store in value_integer
--
UPDATE ir_property SET value_integer=value_boolean::integer WHERE type='boolean';

ALTER TABLE ir_model_fields ADD COLUMN serialization_field_id int REFERENCES ir_model_fields ON DELETE cascade;
UPDATE ir_model_data SET name='XOF' WHERE name='CFA' AND model=E'res.currency';

--
-- The currency model have change, content of name got to symbol
--
UPDATE res_currency SET symbol=name;
UPDATE res_currency SET name=coalesce(code, name);
ALTER TABLE res_currency DROP COLUMN code;

--
-- Update color field for each 
--
ALTER TABLE res_partner ADD COLUMN color integer DEFAULT 0;
COMMENT ON COLUMN res_partner.color IS 'Color Index';
ALTER TABLE res_partner_address ADD COLUMN color integer DEFAULT 0;
COMMENT ON COLUMN res_partner_address.color IS 'Color Index';



