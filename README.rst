Migrate Yourself
================

Migrate Yourself purpose to made a migration yourself in a context of privacy datas (anonymization takes too long and the reverse also)

If you don't have the time and expertise, we recommande to use an OPW, and let the editor to migrate database for yourself


How to use it
-------------

Manual mode
^^^^^^^^^^^

You must install the new version of OpenERP and create the configuration file, and migrate your own module to the last version

Create a new database and install your module resent in the current version, when it's done you can prepare your migration

Copy ``openerp-migration`` file in the server root (at the same place as ``openerp-server``) and the SQL file

For example if you migrate from version 5.0 to 7.0, replace X.Y by 5.0 and Z.A by 7.0

and copy the content of ``addons/official/X.Y-Z.A/`` and ``addons/extra/X.Y-Z.A`` to the folder ``openerp/addons/base/maintenance/migrations``

in this example

::

    cp server/7.0/openerp-migration /srv/openerp/server/
    cp server/7.0/*.sql /srv/openerp/server/
    cp addons/official/5.0-7.0 /srv/openerp/server/openerp/addons/base/maintenance/migrations/
    cp addons/extra/5.0-7.0 /srv/openerp/server/openerp/addons/base/maintenance/migrations/

Automatic mode
^^^^^^^^^^^^^^

Launch this command (same example as manual mode)

execute make prepare-X.Y-Z.A

::

    make prepare-5.0-7.0

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
