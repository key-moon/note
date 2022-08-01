SHELL				=/bin/bash
.SHELLFLAGS			= -O globstar -c 

REPO_PATH			= ${PWD}
DOCS_PATH			= ${REPO_PATH}/docs
THEME_PATH			= ${REPO_PATH}/theme
WRITEUPS_PATH		= ${REPO_PATH}/writeups
WRITEUPS_DEST_PATH	= ${DOCS_PATH}/writeups

all:	build

build: build-docs
	cd "${DOCS_PATH}"; bundle install
	cd "${DOCS_PATH}"; bundle exec jekyll build

build-release: build-docs
	cd "${DOCS_PATH}"; bundle install
	cd "${DOCS_PATH}"; JEKYLL_ENV=production bundle exec jekyll build

serve: build-docs
	cd "${DOCS_PATH}"; bundle install
	cd "${DOCS_PATH}"; bundle exec jekyll serve

serve-release: build-docs
	cd "${DOCS_PATH}"; bundle install
	cd "${DOCS_PATH}"; JEKYLL_ENV=production bundle exec jekyll serve

build-docs: clean
	cp -r "${THEME_PATH}" "${DOCS_PATH}"
	cp -r "${WRITEUPS_PATH}" "${WRITEUPS_DEST_PATH}"

	for template in ${WRITEUPS_DEST_PATH}/**/_template; do \
		if [ -d $${template} ]; then \
			echo "  rm -r $${template}"; \
			rm -r "$${template}"; \
		fi; \
	done

	for md in ${WRITEUPS_DEST_PATH}/**/index.md; do \
		echo "  process_extensions $${md}"; \
		python scripts/process_extensions.py "$${md}"; \
	done

clean:
	-rm -r ${DOCS_PATH}

	
