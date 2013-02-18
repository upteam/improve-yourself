
VERSION = 6.1
TMPFOLDER = dist
MAINTENANCE = openerp/addons/base/maintenance/migrations
READMEFILE = README-MIGRATION

.PHONY: prepare clean

prepare: clean
	@echo "Prepare the files structure for the migration"
	rm -rf $(TMPFOLDER)
	mkdir $(TMPFOLDER)
	cp server/$(VERSION)/openerp-migration* $(TMPFOLDER)/
	mkdir -p $(TMPFOLDER)/$(MAINTENANCE)/
	cp -a addons/official/$(VERSION)/* $(TMPFOLDER)/$(MAINTENANCE)/
	echo "Please copy the folder content in the OpenERP server tree" >> $(TMPFOLDER)/$(READMEFILE)
	echo "and launch this command" >> $(TMPFOLDER)/$(READMEFILE)
	echo " " >> $(TMPFOLDER)/$(READMEFILE)
	echo "./openerp-migration -c ./openerp.conf -d your_database_to_migrate" >> $(TMPFOLDER)/$(READMEFILE)
	echo " " >> $(TMPFOLDER)/$(READMEFILE)
	echo "and check the log content to see if the migration is successfull" >> $(TMPFOLDER)/$(READMEFILE)

clean:
	@echo "Delete the $(TMPFOLDER) folder"
	-rm -rf $(TMPFOLDER)
