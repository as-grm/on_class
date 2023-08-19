# Ocean Navigation

Ocean Navigation is divided into two sections:
- Calculations in **VoyagePlan**,
- Calculations in **Celestial Navigation**.

Under each section are several different tasks.

You can find different Python programs solving upper calculation problems in this repository. For the Navigation Almanac, we use [Skyfield](https://anaconda.org/conda-forge/skyfield) module. 

## Voyage Plan

In the navigation business, Voyage Plan deals primarily with three tasks:

1. How do we design the **Mercator Chart**?
2. How do we compute the **Rumb Line** (RL) or **Loxodrome** problem?
3. How do we compute the **Great Circle** (GC) or **Orthodrome** problem?

## Celestial Navigation

In Celestial Navigation are a few essential tasks:

1. How do we identify stars or **Star Identification** problem?
2. How do we compute the **Sight Reduction** problem or the **Intercept Method** problem?
3. How do we compute the **Meridian Passage** problem?
4. How do we compute **Rise** and **Set** of celestial bodies?
5. How do we compute **Compass Deviation** or compass correction using celestial bodies?
6. How do we draw or compute our position using celestial bodies?

<hr>

## Installation requirements

The easiest method to run this package is by installing the Jupyter-Lab environment from [Miniconda](https://conda.io/miniconda.html).

It depends on several packages:
- Numpy
- Skyfiled
- Astropy
- Basemap
- LaTeX  (generate star identification map)

Install them via **conda** system, from conda-forge:<br>
$> conda install numpy skyfiled astropy basemap

**!!! Important !!!** 

Before the first start of any *Celestial navigation* programs, you must *first* run the following program:

 - *nav_tools/refresh_database.ipynb*

It will download the time frame database! After running any program for the first time, it will download two additional astronomical databases.

