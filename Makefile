SITE=org.sam.sec

SPECFILE=grid-monitoring-probes-${SITE}.spec
PROBES=src/wnjob
FILES=CHANGES

rpmtopdir := $(shell rpm --eval %_topdir)
rpmbuild  := $(shell [ -x /usr/bin/rpmbuild ] && echo rpmbuild || echo rpm)

PKGNAME = $(shell grep -s '^Name:'    $(SPECFILE) | sed -e 's/Name: *//')
PKGVERS = $(shell grep -s '^Version:' $(SPECFILE) | sed -e 's/Version: *//')

distdir = dist/$(PKGNAME)-$(PKGVERS)

dist: $(SPECFILE) $(PROBES) $(FILES)
	mkdir -p $(distdir)/usr/libexec/grid-monitoring/probes/$(SITE)
	cp -rpf $(PROBES) $(distdir)/usr/libexec/grid-monitoring/probes/$(SITE)
	cp -f $(FILES) $(distdir)
	find $(distdir) -path '*svn*' -prune -exec rm -rf {} \;
	find $(distdir) -path '.*swp' -prune -exec rm -rf {} \;

bldprep: dist $(SPECFILE)
	@mkdir -p $(rpmtopdir)/{SOURCES,SPECS,BUILD,SRPMS,RPMS}
	@cd dist && tar cvfz $(rpmtopdir)/SOURCES/$(PKGNAME)-$(PKGVERS).tgz $(PKGNAME)-$(PKGVERS)/*
	@cp -f $(SPECFILE) $(rpmtopdir)/SPECS/$(SPECFILE)

rpmsrc: bldprep dist $(SPECFILE)
	$(rpmbuild) -bs $(SPECFILE)

rpmsrcel4: bldprep dist $(SPECFILE)
	$(rpmbuild) -bs --define 'dist .el4' $(SPECFILE)

rpmsrcel5: bldprep dist $(SPECFILE)
	$(rpmbuild) -bs --define 'dist .el5' $(SPECFILE)

rpmsrcs: rpmsrcel4 rpmsrcel5

rpmel4: bldprep dist $(SPECFILE)
	$(rpmbuild) --define 'dist .el4' -ba $(SPECFILE)	

rpmel5: bldprep dist $(SPECFILE)
	$(rpmbuild) --define 'dist .el5' -ba $(SPECFILE)

rpm: rpmel4 rpmel5 

clean:
	rm -rf dist
