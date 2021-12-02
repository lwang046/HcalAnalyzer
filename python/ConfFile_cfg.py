import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from Configuration.StandardSequences.Eras import eras
process = cms.Process('Hcal4DQMAnalyzer',eras.Run2_2018)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

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
	'/store/data/Run2018D/JetHT/RAW/v1/000/325/170/00000/66A817E1-C153-AB44-B66C-BE10633DA907.root'
        )
)

process.options = cms.untracked.PSet(
#	SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = '101X_dataRun2_v8'


process.Hcal4DQMAnalyzer = cms.EDAnalyzer('Hcal4DQMAnalyzer',
	tagQIE11 = cms.untracked.InputTag("hcalDigis"),
)

process.TFileService = cms.Service("TFileService",
      fileName = cms.string("output.root"),
      closeFileFast = cms.untracked.bool(True)
)


process.p = cms.Path(
	process.bunchSpacingProducer*
        process.hcalDigis*
#	process.hcalLocalRecoSequence*
	process.Hcal4DQMAnalyzer
)

#process.outpath = cms.EndPath(process.out)
