
![Logo](https://www.paulthetall.com/wp-content/uploads/2017/04/arma-3-banner.jpg)


## Authors
- [@ttsiapras](https://github.com/ttsiapras)

Inspired by [@cloftus96](https://github.com/cloftus96)

# Using Arma 3 to Generate Synthetic Data

This README details how python and Arma 3 script(s) are used to
generate data for a Neural Network using the editor from the
game Arma 3. It also gives system requirements and many 
other changes that must be made by the user in order for the
python script to run.

## Description
The intention of this projec is to aid the development of Neural Networks
by providing synthetic data that can be used in the initial development phases
and evaluation of architectures and trainingstrategies. The inspiration for this
project was limited on the position of the camera that captured the vehicles.
This projects comes to add the ability to dynamically select camera location and poses that produce positive samples. Additionally many sidetools were developed to make 
manual jobs  much more time efficient.

In comparisson to the initial concept, the two part of the project (SQF/PYTHON) are kept mostly separate. The sqf scipts are mostly static with a few parameters customizable by  the user. On teh other hand, Python sripta are used to ptoduce positions on the map, and when the data are produces, move them to apropriate locations and produce detaction metadata.


## Examples
Here are some examples of the data that this script creates:
![example](https://github.com/ttsiapras/Arma3DatasetGen/blob/5fb228f1064fd3adf18aaeaba4f670e53ee9711c/readme_images/result.png)
