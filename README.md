# Zebrafisher🔍🦓🐟

### Quantitative morphological analysis pipeline for microscope images of irradiated zebrafish embryos

This repository is the implementation of the process explained in my B.Sc. thesis work @ University of Szeged

## Required PyPI packages

- numpy
- SciPy
- Scikit-Image
- OpenCV
- circle-fit
- czi-file
- matplotlib
- (Jupyter)

# Manual

Example images are included in ``src/images/examples``

1. Copy the image files into ``src/images/in`` folder
2. Run 'main.py'
3. Wait for the analysing process to run
4. Analysis results are stored in the designated csv file in ``src/images``

Saving and showing the result image is set to True by default, but can be turned off in the calling of the main
executing function.

``` python
"""src/main.py 145:5"""
run_pipeline_for_all_images(save=True, batch_name="", popups=True)
```

The processes are visualised in Jupyter Notebook files in the 'well', 'fish', and 'measure' packages

---
Copyright <2022> <Áron Gimesi>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
