Migrate Yourself
================

Migrate Yourself purpose to made a migration yourself in a context of privacy datas (anonymization takes too long and the reverse also)

If you don't have the time and expertise, we reocmmande to use an OPW, and let the editor to migrate database for yourself


How to use it
-------------

Manual mode
^^^^^^^^^^^

You must install the new version of OpenERP and create the configuration file, and create a new database with demo data
when this step is correct, you can prepare your migration

Copy ``openerp-migration`` file in the server root (at the same place as ``openerp-server``)

and copy the content of ``addons/official/X.Y/`` and ``addons/extra/X.Y`` to the folder ``openerp/addons/base/maintenance/migrations``

where X.Y is the version who want to migrate

Automatic mode
^^^^^^^^^^^^^^

Launch this command

::

    make prepare

juste copy the content of the **dist** directory in the server tree

Custom
------

If you want to launch SQL commands before the beginning of the migration, and after the final step you can create theses files

* ``openerp-migration-pre-install61.sql``
* ``openerp-migration-post-install61.sql``

Replace 61 with your version if script is available.for your version

Contribute
----------

You can fork this repo and create a ticket in Github to indicate in which module you work

and if concern an official module, put it in the official for the version you want to use

other module must be put in extra folder

When you're ready to send them, send us a pull request

Regards

The UPTEAM
