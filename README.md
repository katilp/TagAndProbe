# TagAndProbe
Configuration files for the Tag-and-probe method to be used with the CMS Open Data

This repository contains two configuration files, one to produce a root tree with the desired variables and the selection criteria, the other to do the fitting and to derive the efficiency value(s) for the selection criteria in question.

The producer part `testTagProbeFitTreeProducer_ZMuMu_OpenData.py` is orginally from https://github.com/cms-sw/cmssw/blob/CMSSW_5_3_X/PhysicsTools/TagAndProbe/test/testTagProbeFitTreeProducer_ZMuMu.py with flag `isMC` set as "false" and process `muMcMatch` commented out from the path.

Detailed documentation of the two parts in
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideTagProbeFitTreeProducer
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideTagProbeFitTreeAnalyzer

Run in the CMS Open Data environment (if in the VM, inside the `CMS Shell`) with:

```
cd CMSSW_5_3_32/src
cmsenv       
mkdir WorkDir
cd WorkDir/
git clone git ...
```
