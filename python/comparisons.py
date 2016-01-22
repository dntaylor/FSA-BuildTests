
tests = {

    'WZ_MC_74X' : {
        'category'  : 'WZ',
        'name'      : 'MC',
        'target'    : ['miniAOD_dev_74X'],
        'command'   : 'cmsRun',
        'config'    : 'make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'eee,eem,emm,mmm', 
            'nExtraJets': 1, 
            'runWZ'     : 1,
            'isMC'      : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/mc/RunIISpring15MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/023437BD-2D7A-E511-9189-A0369F7FC5BC.root',
        },
    },
    'WZ_Data_74X' : {
        'category'  : 'WZ',
        'name'      : 'Data',
        'target'    : ['miniAOD_dev_74X'],
        'command'   : 'cmsRun',
        'config'    : 'make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'eee,eem,emm,mmm',
            'nExtraJets': 1, 
            'runWZ'     : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/data/Run2015D/MuonEG/MINIAOD/PromptReco-v4/000/258/159/00000/64914E6C-F26B-E511-B0C8-02163E0142D1.root',
        },
    },
    'WZ_MC_76X' : {
        'category'  : 'WZ',
        'name'      : 'MC',
        'target'    : ['miniAOD_dev_76X'],
        'command'   : 'cmsRun',
        'config'    : 'make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'eee,eem,emm,mmm',
            'nExtraJets': 1, 
            'runWZ'     : 1,
            'isMC'      : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/mc/RunIIFall15MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/022EC2EB-90B8-E511-AED0-0026B937D37D.root',
        },
    },
    'WZ_Data_76X' : {
        'category'  : 'WZ',
        'name'      : 'Data',
        'target'    : ['miniAOD_dev_76X'],
        'command'   : 'cmsRun',
        'config'    : 'make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'eee,eem,emm,mmm',
            'nExtraJets': 1, 
            'runWZ'     : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/data/Run2015D/MuonEG/MINIAOD/16Dec2015-v1/60000/04DA5209-60AB-E511-ACCD-008CFA0A57E8.root',
        },
    },

}
