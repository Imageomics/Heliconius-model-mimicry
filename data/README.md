# Mimic Acuity Species Classification Data

The images used for training this model were sourced from the [Heliconius Collection (Cambridge Butterfly)](#heliconius-collection-(cambridge-butterfly)).

## [Heliconius Collection (Cambridge Butterfly)](https://huggingface.co/datasets/imageomics/Heliconius-Collection_Cambridge-Butterfly)

3,822 dorsal images of Heliconius butterflies were sourced from this subset of Chris Jiggins' research group's collection from the University of Cambridge. They are all subspecies of either _Heliconius melpomene_ or _Heliconius erato_.

### How to Access

Install the [cautious-robot](https://github.com/Imageomics/cautious-robot) package.

Run
```bash
cautious-robot -i <path/to>/heliconius_classification_images.csv -o <path/to/output-directory> -s label -v "md5"
```

This will download all images into subfolders based on their label (the taxonomic name of the specimen in the image: _Heliconius <species> ssp. <subspecies>_). It will then verify a match of all the full-sized image MD5s using the [sum-buddy package](https://github.com/Imageomics/sum-buddy).

### Citation
Full bibtex citations are provided in [Heliconius_collection_cambridge.bib](/heliconius_collection_cambridge.bib): these are for both the compilation and all original image sources from the Butterfly Genetics Group at University of Cambridge.


## Acuity Views

