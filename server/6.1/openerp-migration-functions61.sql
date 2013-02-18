--
-- This file containt PostgreSQL Function to upgrade structure for OpenERP Database
--
CREATE OR REPLACE FUNCTION migration61.delete_module(modulename varchar)
RETURNS void AS 
$BODY$

DECLARE
        modulename_id integer;

BEGIN

        SELECT INTO modulename_id id FROM ir_module_module WHERE name = modulename;

        -- UNINSTALL module
        UPDATE ir_module_module SET state=E'uninstalled' WHERE name = modulename;

        -- REMOVE all dependancies for this module
        DELETE FROM ir_module_module_dependency WHERE name = modulename;
        DELETE FROM ir_module_module_dependency WHERE module_id = modulename_id;

        -- DELETE ALL reference in the current objects
        DELETE FROM ir_act_window WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.actions.act_window' AND module=modulename);
        DELETE FROM ir_act_report_xml WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.actions.report.xml' AND module=modulename);
        DELETE FROM ir_model WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.model' AND module=modulename);
        DELETE FROM ir_model_access WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.model.access' AND module=modulename);
        DELETE FROM ir_model_fields WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.model.fields' AND module=modulename);
        DELETE FROM ir_property WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.property' AND module=modulename);
        DELETE FROM ir_rule WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.rule' AND module=modulename);
        DELETE FROM ir_ui_menu WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.ui.menu' AND module=modulename);
        DELETE FROM ir_ui_view WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.ui.view' AND module=modulename);
        DELETE FROM ir_ui_view_sc WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.ui.view_sc' AND module=modulename);
        DELETE FROM ir_values WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.values' AND module=modulename);

        -- process
        DELETE FROM  process_node WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='process.node' AND module=modulename);
        DELETE FROM  process_transition WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='process.transition' AND module=modulename);
        DELETE FROM  process_process WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='process.process' AND module=modulename);

        DELETE FROM res_request_link WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='res.request.link' AND module=modulename);

        -- DELETE all links for this module in ir_model_data
        DELETE FROM ir_model_data WHERE module = modulename;

END;

$BODY$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION migration61.rename_module(oldname varchar, newname varchar)
RETURNS void AS $$

DECLARE
        modulename_id integer;

BEGIN

        SELECT INTO modulename_id id FROM ir_module_module WHERE name = oldname;

        UPDATE ir_module_module_dependency SET name=newname where name=oldname;
        UPDATE ir_module_module SET name=newname where name=oldname;
        UPDATE ir_model_data SET module=newname where module=oldname and name != 'module_meta_information';

END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION migration61.rename_model(oldmodel varchar, newmodel varchar)
RETURNS void AS $$

BEGIN

        UPDATE ir_model SET model = newmodel where model = oldmodel;
        UPDATE ir_model_data SET model=newmodel where model = oldmodel;
        UPDATE ir_attachment SET res_model = newmodel where res_model = oldmodel;
        UPDATE ir_model_data SET model = newmodel where model=oldmodel;

END;

$$ LANGUAGE plpgsql;

--
-- This function indicate if module is installed, 
-- return true if installed, otherwise return false
--
CREATE OR REPLACE FUNCTION migration61.is_module_installed(modulename varchar)
RETURNS boolean AS $$

DECLARE

    module_id integer;

BEGIN

    SELECT INTO module_id id FROM ir_module_module WHERE name=modulename and state='installed';

    IF NOT FOUND THEN
        RETURN false;
    ELSE
        RETURN true;
    END IF;

END;

$$ LANGUAGE plpgsql;

--
-- This function check all modules to installed or upgrade
-- and verify if there dependencies is installed or to installed
--
CREATE OR REPLACE FUNCTION migration61.check_upgrade()
RETURNS void AS 
$BODY$

DECLARE

    rm record;
    rd record;

BEGIN

    FOR rm IN SELECT id, name FROM ir_module_module WHERE state='installed'
    LOOP

        FOR rd IN SELECT id, name FROM ir_module_module_dependency WHERE module_id=rm.id
        LOOP

            UPDATE ir_module_module SET state='to install' WHERE name=rd.name AND state='uninstalled';

        END LOOP;

    END LOOP;

END;

$BODY$ LANGUAGE plpgsql;

