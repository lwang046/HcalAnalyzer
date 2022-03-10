
runlist = [323487, 323524, 323525, 323526, 323702, 323778, 323940, 323997, 324021, 324022, 324209, 324420, 324571, 324747, 324785, 324841, 324846, 324980, 325001, 325022, 325117, 325170, 323488]
for runid in runlist:
  runid = str(runid)
  psfile = open('Crabjob_Run%s.py'%runid,"w")
  argstr = '''
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'Hcal4DQMAnalyzerNew_Run%s'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'python/ConfFile_cfg.py'
#config.JobType.maxMemoryMB = 4000
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/ZeroBias/Run2018D-v1/RAW'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1000
#config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/DCSOnly/json_DCSONLY.txt'
config.Data.runRange = '%s'
config.Data.outLFNDirBase = '/store/user/lowang/'
config.Data.publication = False
config.Data.outputDatasetTag = 'Hcal4DQMAnalyzerNew_Run%s'

config.Site.storageSite = 'T2_CH_CERN'
  ''' %(runid, runid, runid)

  psfile.write(argstr)
  psfile.close()

