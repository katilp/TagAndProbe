import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

######### EXAMPLE CFG 
###  A simple test of runnning T&P on Zmumu to determine muon isolation and identification efficiencies
###  More a showcase of the tool than an actual physics example

process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/10000/000D143E-9535-E311-B88B-002618943934.root',
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/10000/0020AF81-A835-E311-97DC-00261894398C.root',
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/10000/0062BD79-9235-E311-9320-003048FFCC2C.root',
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/10000/008B0182-5E35-E311-B039-003048FFD71E.root',
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/10000/009A5FA1-0D36-E311-B603-00261894388A.root',
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/10000/00ADCF5D-7435-E311-9347-00261894397A.root'
    )
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )    

## Tags. In a real analysis we should require that the tag muon fires the trigger, 
##       that's easy with PAT muons but not RECO/AOD ones, so we won't do it here
##       (the J/Psi example shows it)
process.tagMuons = cms.EDFilter("MuonRefSelector",
    src = cms.InputTag("muons"),
    cut = cms.string("isGlobalMuon && pt > 20 && abs(eta) < 2"), 
)
## Probes. Now we just use Tracker Muons as probes
process.probeMuons = cms.EDFilter("MuonRefSelector",
    src = cms.InputTag("muons"),
    cut = cms.string("isTrackerMuon && pt > 10"), 
)

## Here we show how to define passing probes with a selector
## although for this case a string cut in the TagProbeFitTreeProducer would be enough
process.probesPassingCal = cms.EDFilter("MuonRefSelector",
    src = cms.InputTag("muons"),
    cut = cms.string(process.probeMuons.cut.value() + " && caloCompatibility > 0.6"),
)

## Here we show how to use a module to compute an external variable
process.drToNearestJet = cms.EDProducer("DeltaRNearestJetComputer",
    probes = cms.InputTag("muons"),
       # ^^--- NOTA BENE: if probes are defined by ref, as in this case, 
       #       this must be the full collection, not the subset by refs.
    objects = cms.InputTag("ak5CaloJets"),
    objectSelection = cms.InputTag("et > 20 && abs(eta) < 3 && n60 > 3 && (.05 < emEnergyFraction < .95)"),
)

## Combine Tags and Probes into Z candidates, applying a mass cut
process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("tagMuons@+ probeMuons@-"), # charge coniugate states are implied
    cut   = cms.string("40 < mass < 200"),
)

## Match muons to MC
process.muMcMatch = cms.EDFilter("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(13),
    src = cms.InputTag("muons"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles")
)

## Make the tree
process.muonEffs = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # pairs
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("OneProbe"),
    # variables to use
    variables = cms.PSet(
        ## methods of reco::Candidate
        eta = cms.string("eta"),
        pt  = cms.string("pt"),
        ## a method of the reco::Muon object (thanks to the 3.4.X StringParser)
        nsegm = cms.string("numberOfMatches"), 
        ## this one is an external variable
        drj = cms.InputTag("drToNearestJet"),
    ),
       # choice of what defines a 'passing' probe
    flags = cms.PSet(
        ## one defined by an external collection of passing probes
        passingCal = cms.InputTag("probesPassingCal"), 
        ## two defined by simple string cuts
        passingGlb = cms.string("isGlobalMuon"),
        passingIso = cms.string("(isolationR03.hadEt+isolationR03.emEt+isolationR03.sumPt) < 0.1 * pt"),
    ),
    # mc-truth info
    isMC = cms.bool(False),
    motherPdgId = cms.vint32(22,23),
    makeMCUnbiasTree = cms.bool(True),
    checkMotherInUnbiasEff = cms.bool(True),
    tagMatches = cms.InputTag("muMcMatch"),
    probeMatches  = cms.InputTag("muMcMatch"),
    allProbes     = cms.InputTag("probeMuons"),
)
##    ____       _   _     
##   |  _ \ __ _| |_| |__  
##   | |_) / _` | __| '_ \ 
##   |  __/ (_| | |_| | | |
##   |_|   \__,_|\__|_| |_|
##                         
process.tagAndProbe = cms.Path( 
    (process.tagMuons + process.probeMuons) *   # 'A*B' means 'B needs output of A'; 
    (process.probesPassingCal +                 # 'A+B' means 'if you want you can re-arrange the order'
     process.drToNearestJet   +
     process.tpPairs) *
#     process.tpPairs +
#     process.muMcMatch) *
    process.muonEffs
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("testTagProbeFitTreeProducer_ZMuMu.root"))


