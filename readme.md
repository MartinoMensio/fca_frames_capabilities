# Info

[FCA](https://en.wikipedia.org/wiki/Formal_concept_analysis) is a technique to derive a lattice, by manipulating objects and properties. The python library https://github.com/xflr6/concepts is being used.

## The problem

We want to apply FCA to analyse the requirements for user intents (frames) in terms of robot capabilities.

The FCA is applied in the following way:
- Objects: frames
- properties: capabilities

# Approach

The initial step is to consider the [table frames-capabilities](table.csv) and build the lattice. A more useful lattice, instead of the frames-capabilities, is the frame-uncapabilities: in this way it is easier to navigate towards the Infimum (objects with less requirements) and find frames that have less capabilities required.

Look at [this jupyter notebook](3_explaination.ipynb) to a better description.
