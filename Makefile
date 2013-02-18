
VERSION = 6.1
TMPFOLDER = dist
MAINTENANCE = openerp/addons/base/maintenance/migrations

.PHONY: prepare clean

prepare: clean
	@echo "Prepare the files structure for the migration"
	rm -rf $(TMPFOLDER)
	mkdir $(TMPFOLDER)
	cp server/$(VERSION)/openerp-migration $(TMPFOLDER)/
	mkdir -p $(TMPFOLDER)/$(MAINTENANCE)/
	cp -a addons/official/$(VERSION)/* $(TMPFOLDER)/$(MAINTENANCE)/
	echo "Please copy the folder content in the OpenERP server tree" >> $(TMPFOLDER)/README
	echo "and launch this command" >> $(TMPFOLDER)/README
	echo " " >> $(TMPFOLDER)/README
	echo "./openerp-migration -c ./openerp.conf -d your_database_to_migrate" >> $(TMPFOLDER)/README
	echo " " >> $(TMPFOLDER)/README
	echo "and check the log content to see if the migration is successfull" >> $(TMPFOLDER)/README

clean:
	@echo "Delete the $(TMPFOLDER) folder"
	-rm -rf $(TMPFOLDER)
