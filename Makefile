SITE=eu.egi.sec

SPECFILE=grid-monitoring-probes-${SITE}.spec
PROBES=src/probes
WNPROBES=src/WN-probes
ARC=src/ARC/50-secmon.ini
CREAM=src/CREAM
FILES=CHANGES

NOOP    = true

rpmtopdir := $(shell rpm --eval %_topdir)
rpmbuild  := $(shell [ -x /usr/bin/rpmbuild ] && echo rpmbuild || echo rpm)

PKGNAME = $(shell grep -s '^Name:'    $(SPECFILE) | sed -e 's/Name: *//')
PKGVERS = $(shell grep -s '^Version:' $(SPECFILE) | sed -e 's/Version: *//')

distdir = dist/$(PKGNAME)-$(PKGVERS)

dist: $(SPECFILE) $(PROBES) $(WNPROBES) $(ARC) $(CREAM) $(FILES)
	mkdir -p $(distdir)/usr/libexec/grid-monitoring/probes/$(SITE)
	mkdir -p $(distdir)/etc/arc/nagios
	cp -rpf $(PROBES) $(distdir)/usr/libexec/grid-monitoring/probes/$(SITE)
	cp -rpf $(WNPROBES) $(distdir)/usr/libexec/grid-monitoring/probes/$(SITE)
	cp -rpf $(ARC) $(distdir)/etc/arc/nagios
	cp -rpf $(CREAM) $(distdir)/usr/libexec/grid-monitoring/probes/$(SITE)
	cp -f $(FILES) $(distdir)
	find $(distdir) -path '*svn*' -prune -exec rm -rf {} \;
	find $(distdir) -path '.*swp' -prune -exec rm -rf {} \;

bldprep: dist $(SPECFILE)
	@mkdir -p $(rpmtopdir)/{SOURCES,SPECS,BUILD,SRPMS,RPMS}
	@cd dist && tar cvfz $(rpmtopdir)/SOURCES/$(PKGNAME)-$(PKGVERS).tgz $(PKGNAME)-$(PKGVERS)/*
	@cp -f $(SPECFILE) $(rpmtopdir)/SPECS/$(SPECFILE)

rpmsrc: bldprep dist $(SPECFILE)
	$(rpmbuild) -bs $(SPECFILE)

rpmsrcel6: bldprep dist $(SPECFILE)
	$(rpmbuild) -bs --define 'dist .el6' $(SPECFILE)

rpmsrcel7: bldprep dist $(SPECFILE)
	$(rpmbuild) -bs --define 'dist .el7' $(SPECFILE)

rpmsrcs: rpmsrcel6 rpmsrcel7

rpmel6: bldprep dist $(SPECFILE)
	$(rpmbuild) --define 'dist .el6' -ba $(SPECFILE)	

rpmel7: bldprep dist $(SPECFILE)
	$(rpmbuild) --define 'dist .el7' -ba $(SPECFILE)

rpm: rpmel6 rpmel7

clean:
	rm -rf dist

sources: dist $(SPECFILE)
	cd dist && tar cvfz ../$(PKGNAME)-$(PKGVERS).tgz $(PKGNAME)-$(PKGVERS)/*
