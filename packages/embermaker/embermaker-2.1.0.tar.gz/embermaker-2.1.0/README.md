# EmberMaker

## Purpose

EmberMaker is a scientific graphic library aimed at (re)producing "burning ember" diagrams 
of the style used in IPCC (Intergovernmental Panel on Climate Change) reports. 
All graphics elements are in vector form, including color gradients (this implies specific drawing code).

EmberMaker was formerly a part of the EmberFactory project: https://pypi.org/project/EmberFactory/. 
If you need to produce ember diagrams from your data, **first consider using the online [EmberFactory](https://pypi.org/project/EmberFactory/)**. 
This package is intended to meet more specific needs, by drawing embers from your own code.

In addition to 'burning embers', EmberMaker can also draw common x-y plots which share the
same vertical axis as a set of embers.

While EmberMaker is a Python package, it is quite easy to use within [R](https://www.r-project.org),
as shown in the last example below.

## Installation

`pip install embermaker`

Only Python >= 3.10 is supported.

## Basic usage
Creating embers only needs calling a few functions, as in this basic example:

```
from embermaker.embergraph import EmberGraph
from embermaker.ember import Ember

# Create ember
be = Ember(name='What this ember is about', haz_valid=[0, 5])

# Add two transitions to this ember
be.trans_create(name='undetectable to moderate', min=0.6, median=1.1, max=1.4, confidence='very high')
be.trans_create(name='moderate to high', min=1.7, median=2.2, max=2.5, confidence='high')

# Create an ember graph (available native image formats are PDF and SVG)
egr = EmberGraph("output_file_name", grformat="PDF")

# Change a parameter (list of parameters: https://climrisk.org/emberfactory/doc/parameters )
egr.gp['haz_axis_top'] = 5.0  # max value on axis 

# Add ember to graph (a list would work as well; more advanced uses define ember groups)
egr.add(be)

# Actually produce the diagram
outfile = egr.draw()
```

## Usage examples

Examples are provided on [FramaGit](https://framagit.org/marbaix/embermaker/-/tree/master/examples) (a GitLab instance)

### Access within python (/examples/python): 
- 'create_and_draw_embers.py' is the shorter and simpler. It illustrates a few functions constructing embers from data.
- 'draw_embers_from_file.py' reads 'traditional' ember Excel sheets and shows how an x-y plot can be added.
- 'test_error_reporting.py' illustrates a few cases which produce warning or error messages and how to access these.
### Access from R (/examples/R):
- 'create_and_draw_embers.R' illustrates functions constructing embers, within an R script and using data produced in R.

As this is the first "standalone" version, the API functions may be improved in the future, as well as more documented.
We are interested in learning how you use this and any difficult you might face, to steer future development - thanks!

## Development history
The EmberFactory software was created by philippe.marbaix -at- uclouvain.be at the end of 2019.
The first objective was to produce figure 3 of Zommers et al. 2020 ([doi.org/10/gg985p](https://doi.org/10/gg985p)).
