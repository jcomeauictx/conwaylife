DRYRUN ?= --dry-run
SERVER ?= www
export
run:
	chromium life.html 2>/dev/null
test:
	@echo click to set squares, then '"r"' to start
	firefox "life.html?CHANCE=&DEBUGGING=1" 2>/dev/null
pyrun:
	./life.py &
upload:
	rsync -avuz $(DRYRUN) \
	 --exclude='*.pyc' \
	 . $(SERVER):src/conwaylife
deploy: Info.plist icon.png
	rsync -avuz $(DRYRUN) \
	 --exclude='*.pyc' \
	 . mobile@wanderer:rentacoder/jcomeau/conwaylife/
	rsync -avuz $(DRYRUN) \
	 $+ \
	 mobile@wanderer:Library/WebClips/com.jcomeau.conwaylife.webclip/
icon.png:
	convert -size 60x60 xc:green $@
