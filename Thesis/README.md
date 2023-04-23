# SEEMOO Thesis Template

[![Pipeline status](https://dev.seemoo.tu-darmstadt.de/templates/seemoo-thesis-template/badges/master/pipeline.svg)](https://dev.seemoo.tu-darmstadt.de/templates/seemoo-thesis-template/-/tree/master)
[![Download latest PDF](https://img.shields.io/badge/download-PDF-informational)](https://dev.seemoo.tu-darmstadt.de/templates/seemoo-thesis-template/-/jobs/artifacts/master/file/Thesis.pdf?job=build)

This is a LaTeX template to be used for all theses written at SEEMOO. It's based on the [`classicthesis`](https://ctan.org/pkg/classicthesis) package but includes some specific adjustments for SEEMOO and TU Darmstadt. This README is supposed to get you started quickly, avoid frustration, and let you spend more time for working on your actual project.

*If you have a bug fix or general improvment, don't keep them to yourself but create a pull request!*

## Structure

This repository has the following main structure:

* `Appendicies/` contains additional chapters that did not make it into the main part of the thesis (e.g., questionnaires, long proofs, ...).
* `Chapters/` contains the main chapters of your thesis.
* `gfx/` include figures such as graphs and other visualizations here.
* `additional-packages.tex` contains custom packages that you might need.
* `AuthorPublications.bib` for a PhD thesis, contains all publications of the author that will appear in a separate chapter at the end.
* `Acronyms.tex` contains--you guessed it--acronym definitions.
* `Bibliography.bib` contains all your bibtex references.
* `classicthesis-config.tex` can be adjusted to your needs (see below).
* `classicthesis-personal-info.tex` must be adjusted (see below).
* `classicthesis.sty` the `classicthesis` style file (no need to adapt).
* `Hyphenation.tex` add custom rules if LaTeX screws up hyphenation.
* `Macros.tex` add custom commands, e.g., symbols or often used expressions.
* `make.bat` and `Makefile` for Windows and UNIX, respectively.
* `Thesis.tex` the main file. Include additional chapters here.

## Configuration

There are several configuration parameters that you need to adjust.

### Meta data

Adjust all the `\my<X>` variables in [`classicthesis-personal-info.tex`](./classicthesis-personal-info.tex) such as your name and title of your thesis.

### Style

You can choose between different styles for your thesis. You can enable them by uncommenting the respective `\toggletrue{<X>}` calls in [`Thesis.tex`](./Thesis.tex) Currently, these are:

* **Less margins.** The `adrianstyle` (called so for historic reasons) will reduce the page margins, effectively increasing the space for text and floats. Don't use margin notes together with this mode.
* **Use parts.** The `parts` toggle will add another layer of structure to your thesis. Only use this if your thesis is particulary long or additional structure makes sense.
* **PhD thesis.** The `phd` toggle adds additional front and back matter pages to the template that are relevant if you write a PhD thesis.

### Drafting mode

To enable a drafting mode (prints date, version number, and git commit hash in footer) set the `drafting` option in [`classicthesis-config.tex`](./classicthesis-config.tex) to `true`.

To display the git commit hash, you have to install and trigger the [`gitinfo2`](https://ctan.org/pkg/gitinfo2) hooks once via
```
make gitinfo2-hooks
git checkout master
```

## Build

Use your IDE of choice or simply call
```
make
```
from the command line which will create the file `Thesis.pdf` in the root directory.
