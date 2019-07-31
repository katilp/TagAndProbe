# TagAndProbe
Configuration files for the Tag-and-probe method to be used with CMS Open Data

This repository contains two configuration files, one to produce a root tree with the desired variables and the selection criteria, the other to do the fitting and to derive the efficiency value(s) for the selection criteria in question

Detailed documentation of the two parts in
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideTagProbeFitTreeProducer
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideTagProbeFitTreeAnalyzer

Run in the CMS Open Data environment (if in with within the `CMS Shell`) with:

```
cd CMSSW_5_3_32/src
cmsenv       
mkdir WorkDir
cd WorkDir/
mkdir tnp
cd tnp
```
