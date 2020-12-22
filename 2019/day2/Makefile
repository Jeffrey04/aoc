SUBDIRS = $(shell ls -d */)

.PHONY: run

run:
	@for dir in ${SUBDIRS} ; do \
		make -s -C $$dir run; \
	done;