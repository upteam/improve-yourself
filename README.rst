Migrate Yourself
================

Migrate Yourself purpose to made a migration yourself in a context of privacy datas

If you don't have the time and expertise, we reocmmande to use an OPW, and let the editor to migrate database for yourself


How to use it
-------------

Copy ``openerp-migration`` file in the server root (at the same place as ``openerp-server``)

and copy the content of ``addons/official/X.Y/`` and ``addons/extra/X.Y`` to the folder ``openerp/addons/base/maintenance/migrations``

where X.Y is the version who want to migrate

.. todo::

    Add a Makefile to create the real folder tree and use ``cp`` to copy files and folders


Contribute
----------

You can fork this repo and create a ticket in Github to indicate in which module you work

and if concern an official module, put it in the official for the version you want to use

other module must be put in extra folder

When you're ready to send them, send us a pull request
