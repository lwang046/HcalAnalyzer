import subprocess

runlist = [355456, 355680, 355769, 356077, 356381, 356446, 356523, 356578, 356615, 357080, 357081, 357112, 357271, 357329, 357442, 357479, 357612, 357700, 357815, 357899, 359686, 359694, 359764, 360019, 360459, 360820, 360895, 361240, 361957, 362091, 362696, 362760]

for runid in runlist:
  runid = str(runid)

  commandline = 'dasgoclient --query="dataset run=%s dataset=/ZeroBias/Run2022*/RAW"' % runid
  output=subprocess.run(commandline, shell=True, capture_output=True, text=True)


  psfile = open('Crabjob_Run%s.py'%runid,"w")
  argstr = '''
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'Hcal4DQMAnalyzerCut20fC_Run%s'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'python/ConfFile_cfg.py'
#config.JobType.maxMemoryMB = 4000
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '%s'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1000
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json'
config.Data.runRange = '%s'
config.Data.outLFNDirBase = '/store/user/lowang/'
config.Data.publication = False
config.Data.outputDatasetTag = 'Hcal4DQMAnalyzerCut20fC_Run%s'

config.Site.storageSite = 'T2_CH_CERN'
  ''' %(runid, output.stdout.strip(), runid, runid)

  psfile.write(argstr)
  psfile.close()

