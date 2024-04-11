# Ocean Navigation with Python

Ocean Navigation involves two main areas of focus:
- Calculations within **Voyage Plan**,
- Calculations within **Celestial Navigation**.

Each section comprises various tasks and problems related to marine navigation.

For solving these tasks, you can refer to the Python programs available in this repository. The [Skyfield](https://anaconda.org/conda-forge/skyfield) module is used for celestial navigation computations.

## Voyage Plan

In marine navigation, the Voyage Plan addresses three key tasks:

1. **Mercator Chart Design**: How to design a Mercator chart for navigation purposes.
2. **Rhumb Line (RL) or Loxodrome Problem**: How to compute the course and distance along a rhumb line.
3. **Great Circle (GC) or Orthodrome Problem**: How to compute the shortest path between two points on the Earth's surface.

## Celestial Navigation

Celestial Navigation encompasses several critical tasks:

1. **Star Identification**: How to identify stars for navigation purposes.
2. **Sight Reduction or Intercept Method**: How to compute the position of a celestial body from sextant observations.
3. **Meridian Passage**: How to determine the moment when a celestial body crosses the observer's meridian.
4. **Rise and Set of Celestial Bodies**: How to compute the rising and setting times of celestial bodies.
5. **Compass Deviation**: How to correct compass deviations using celestial bodies.
6. **Calculated Position with Body Height**:
   - With assumed observer position.
   - Without assumed observer position.

## Installation Requirements

The recommended method to use this package is by installing the Jupyter Lab environment from [Miniconda](https://conda.io/miniconda.html).

Ensure that the following packages are installed:
- Numpy
- Skyfield
- Astropy
- Basemap
- LaTeX (required for generating star identification maps)

Install these packages using the **conda** package manager from the conda-forge channel:
```bash
$ conda install --file requirements.txt
```

**Important Note:** Before running any Celestial Navigation programs for the first time, execute the following program (and restart the kernel afterward):

- **nav_tools/refresh_database.ipynb**

This program will download the necessary time frame database. Additionally, running any Celestial Navigation program for the first time will trigger the download of two additional astronomical databases.