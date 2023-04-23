DOCUMENT := Thesis
# max_repeat=6 is needed to make the reference numbering for author publication work
LATEXMK := latexmk -e '$$max_repeat=6' -pdf -bibtex -synctex=1

.PHONY: document sort-acronyms clean

default: document

sort-acronyms:
	sort Acronyms.tex -o Acronyms.tex

document:
	@echo "Build document"
	$(LATEXMK) $(DOCUMENT)

gitinfo2-hooks: gitinfo2_post-xxx.sample
	cp gitinfo2_post-xxx.sample .git/hooks/post-checkout
	cp gitinfo2_post-xxx.sample .git/hooks/post-commit
	cp gitinfo2_post-xxx.sample .git/hooks/post-merge

clean:
	@ echo "Clean up"
	$(LATEXMK) -C
	rm -f pdfa.xmpi
	rm -f $(DOCUMENT)-blx.bib
	rm -f gfxcompiled/*
