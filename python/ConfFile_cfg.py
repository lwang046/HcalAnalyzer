import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from Configuration.StandardSequences.Eras import eras
process = cms.Process('Hcal4DQMAnalyzer',eras.Run2_2018)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(500)

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
        '/store/data/Run2018D/ZeroBias/RAW/v1/000/325/169/00000/A9C40B8C-593C-A940-9DFC-D4B841D70C9C.root',
	'/store/data/Run2018D/ZeroBias/RAW/v1/000/325/169/00000/3E1AA73B-205F-A84C-8E55-A4BECA86399F.root',
	'/store/data/Run2018D/ZeroBias/RAW/v1/000/325/169/00000/758FA122-5717-C541-AB1E-1432CA535C9C.root',
	'/store/data/Run2018D/ZeroBias/RAW/v1/000/325/169/00000/05B70CF9-46C3-3446-B757-B6BEF1C49C61.root',
	'/store/data/Run2018D/ZeroBias/RAW/v1/000/325/169/00000/08326CEE-FC91-D741-888C-E37FFF32A79C.root',
	'/store/data/Run2018D/ZeroBias/RAW/v1/000/325/169/00000/FF7B77A6-996D-1B40-AE72-1AEAC4164E40.root'
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
      fileName = cms.string("QIE11DigiOccupancy.root"),
      closeFileFast = cms.untracked.bool(True)
)


process.p = cms.Path(
	process.bunchSpacingProducer*
        process.hcalDigis*
#	process.hcalLocalRecoSequence*
	process.Hcal4DQMAnalyzer
)

#process.outpath = cms.EndPath(process.out)
