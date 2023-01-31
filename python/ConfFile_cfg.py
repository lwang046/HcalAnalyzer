import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from Configuration.StandardSequences.Eras import eras
process = cms.Process('Hcal4DQMAnalyzer',eras.Run3)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.load('Configuration.EventContent.EventContent_cff')
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("RecoLocalCalo.Configuration.hcalLocalReco_cff")
process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load("RecoLuminosity.LumiProducer.bunchSpacingProducer_cfi")

#process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
	'/store/data/Run2022C/ZeroBias/RAW/v1/000/356/381/00000/c264b6cf-ece5-4d64-a2ce-277fd45c45a2.root'
        )
)

process.options = cms.untracked.PSet(
#	SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = autoCond['run3_hlt']

process.Hcal4DQMAnalyzer = cms.EDAnalyzer('Hcal4DQMAnalyzer',
	tagQIE11 = cms.untracked.InputTag("hcalDigis"),
)

process.TFileService = cms.Service("TFileService",
      fileName = cms.string("output.root"),
      closeFileFast = cms.untracked.bool(True)
)


process.p = cms.Path(
        process.hcalDigis*
#	process.hcalLocalRecoSequence*
	process.Hcal4DQMAnalyzer
)

#process.outpath = cms.EndPath(process.out)
