# Stone Tool Symmetry Analyser

Lithikos is an open-source volumetric morphometric tool which calculates volume data for the artefact model using a synthesised radially symmetrical reference.

This application was initally written to analyse the bilateral and bifacial asymmetry of 3D models of paleolithic stone tools.
Various options are available for artefact orientation and symmetrical reference resolution. Once oriented, the model is divided into quadrants referencing the long axis of the artefact and the volume of each quadrant is recored. The artefact morphology is then sampled at equidistant locations along its length in order to synthesise the largest possible radially symmetrical reference (Endo-Sym) within the topological boundary of each artefact model.
One quarter of the reference mesh volume, in conjunction with the artefact quadrant volumes, can be used to determine coefficients of bilateral and bifacial asymmetry, amonst of others.

## Motivation

There have been a number of 2D and 3D approaches to the analysis of bilateral symmetry in Acheulean handaxes: radial qualification (Marathe, 1980), the Continuous Symmetry Measure (Saragusti et al., 1998), deformable shape analysis (Park et al., 2003), mental folding (McNabb et al., 2004), the Index of Symmetry (Lycett et al., 2008), the Index of Deviation of Symmetry (Feizi et al., 2018, 2020), elliptical Fourier analyses (Saragusti et al., 2005; Hoggard et al., 2019; Iovita et al., 2017), and the Deviation from Bilateral/Bifacial Symmetry (Herzlinger & Goren-Inbar, 2020; Herzlinger et al., 2021a, 2021b; Ravon et al., 2022; García-Medrano et al., 2022a; García-Medrano et al., 2022b; García-Medrano et al., 2023; Ollé et al., 2023). The most prevalent distance-based method for analysing bilateral mirror symmetry has been the Flip Test and its Asymmetry Index (Hardaker & Dunn, 2005; Keen et al., 2006; Lee, 2016; Putt et al., 2014; Shipton, 2018; Underhill, 2007; White & Foulds, 2018). Its popularity still inspires similar approaches, such as AS-check (Hutchence & Debackere, 2019). Archaeologists have traditionally focused on distance-based analyses of plan-view or bilateral mirror symmetry, with occasional investigations of bifacial symmetry in profile view or cross-section. Couzens (2013) introduced a novel unreferenced volumetric analysis of handaxe bilateral symmetry. Unlike previous methods that relied on measures of point to point surface distances, this approach evaluated the entire topological geometry of the 3D models offered by modern digital scanners. Couzens coefficient of symmetry was calculated using Pearson product-moment correlations between volumes of opposing bilateral halves of artefact models bifurcated along the primary axis. Later, Li et al. (2016, 2018) expanded this unreferenced volumetric method to include analyses of bifacial symmetry. All of these methods have their limitations: e.g., Deviation from Bilateral/Bifacial Symmetry appears to invert the direction and magnitude of the relationship between bilateral and bifacial asymmetry. The unreferenced volumetric analysis using Pearson product-moment correlations overlooks the fact that matched halves of a solid bifurcated along its primary axis can occupy equivalent volumes while distributed across infinite asymmetrical geometries. Therefore, Lithikos offers a referenced volumetric analysis of asymmetry to overcome the limitations of tradiation 2D and emerging unreferenced 3D anaylses.

## Installation and Setup

To install the application,

```bash
pip install lithikos
```

## Quickstart Code Example

```bash
lithikos my_handaxe.obj
```

which is equivalent to

```bash
lithikos my_handaxe.obj --orientation-method Tip2CoM --analysis-method Endo-Sym --slice-count 100 --point-count 36 --tip-spacing 0.001 --butt-spacing 0.001
```

Based on the above command Lithikos will produce the following files in the output directory

```text
output/my_handaxe
output/my_handaxe/quadrants
output/my_handaxe/quadrants/my_handaxe_T2C-QIII_DL.obj
output/my_handaxe/quadrants/my_handaxe_T2C-QII_DR.obj
output/my_handaxe/quadrants/my_handaxe_T2C-QIV_VL.obj
output/my_handaxe/quadrants/my_handaxe_T2C-QI_VR.obj
output/my_handaxe/my_handaxe_T2C_3D-model.obj
output/my_handaxe/my_handaxe_T2C_endo-sym_s0100-p0036_ts0.001-bs0.001.obj
output/my_handaxe/my_handaxe_T2C_endo-sym_s0100-p0036_ts0.001-bs0.001_out.html
output/my_handaxe/my_handaxe_T2C_endo-sym_s0100-p0036_ts0.001-bs0.001_out.txt
```

Two csv files will also be produced

```text
reference_data.csv
volume_data.csv
```

## Usage Reference

Roe (1964, 1968) measured a small set of planar metrics and analyzed a large body of Acheulean bifaces gathered from 38 sites in Southern Britain to document the variability in size, shape, and refinement of whole assemblages or groups of assemblages. He employed five ratios based on seven linear (planar) measurements (in millimeters) and the weight (in ounces) of an artefact. The planar measurements included length (tip to butt in plan view), breadth (maximum from side to side in plan view), and thickness (maximum in profile view).

## Recommended citation

## Other Related Tools
