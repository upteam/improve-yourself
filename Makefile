
TMPFOLDER = dist
MAINTENANCE = openerp/addons/base/maintenance/migrations
READMEFILE = README-MIGRATION

.PHONY: prepare clean

help:
	@echo "Available commands :"
	@echo "    prepare-6.0-6.1"
	@echo "    clean"

prepare: clean
	@echo "Prepare the files structure for the migration from $(VERSION_FROM) to $(VERSION_TO)"
	rm -rf $(TMPFOLDER)
	mkdir $(TMPFOLDER)
	cp server/$(VERSION_TO)/openerp-migration* $(TMPFOLDER)/
	mkdir -p $(TMPFOLDER)/$(MAINTENANCE)/
	cp -a addons/official/$(VERSION_FROM)-$(VERSION_TO)/* $(TMPFOLDER)/$(MAINTENANCE)/
	echo "Please copy the folder content in the OpenERP server tree" >> $(TMPFOLDER)/$(READMEFILE)
	echo "and launch this command" >> $(TMPFOLDER)/$(READMEFILE)
	echo " " >> $(TMPFOLDER)/$(READMEFILE)
	echo "./openerp-migration -c ./openerp.conf -d your_database_to_migrate" >> $(TMPFOLDER)/$(READMEFILE)
	echo " " >> $(TMPFOLDER)/$(READMEFILE)
	echo "and check the log content to see if the migration is successfull" >> $(TMPFOLDER)/$(READMEFILE)

prepare-6.0-6.1: VERSION_FROM = 6.0
prepare-6.0-6.1: VERSION_TO = 6.1
prepare-6.0-6.1: prepare

clean:
	@echo "Delete the $(TMPFOLDER) folder"
	-rm -rf $(TMPFOLDER)
