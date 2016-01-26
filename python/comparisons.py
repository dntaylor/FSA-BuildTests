
tests = {
    # Tests to run
    # format must be:
    # 'Unique_key' : {
    #     'category'  : 'Analysis',                                                    # must match watchedVariables keys (otherwise no DQM will be run beyond verify the cmsRun command works)
    #     'name'      : 'CustomNameForTest',
    #     'target'    : ['BranchToWatch'],                                             # ex: miniAOD_dev_74X
    #     'command'   : 'cmsRun',                                                      # unix commmand
    #     'config'    : 'src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py', # location of config file relative to $CMSSW_BASE
    #     'arguments' : {                                                              # arguments for config file
    #         # 'argument' : 'value'
    #         'maxEvents' : 1000,
    #         'inputFiles': '/store/.../file.root',
    #     },
    #     'output'    : 'src/ntuplize.root',                                           # expected output relative to CMSSW_BASE
    # },
    
    # simple dqm
    'DQM_MC_74X' : {
        'category'  : 'DQM',
        'name'      : 'MC',
        'target'    : ['miniAOD_dev_74X'],
        'command'   : 'cmsRun',
        'config'    : 'src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'dqm', 
            'isMC'      : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/mc/RunIISpring15MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v3/60000/00181849-176A-E511-8B11-848F69FD4C94.root',
        },
        'output'    : 'src/ntuplize.root',
    },
    'DQM_Data_74X' : {
        'category'  : 'DQM',
        'name'      : 'Data',
        'target'    : ['miniAOD_dev_74X'],
        'command'   : 'cmsRun',
        'config'    : 'src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'dqm',
            'maxEvents' : 1000,
            'inputFiles': '/store/data/Run2015D/MuonEG/MINIAOD/PromptReco-v4/000/258/159/00000/64914E6C-F26B-E511-B0C8-02163E0142D1.root',
        },
        'output'    : 'src/ntuplize.root',
    },
    'DQM_MC_76X' : {
        'category'  : 'DQM',
        'name'      : 'MC',
        'target'    : ['miniAOD_dev_76X'],
        'command'   : 'cmsRun',
        'config'    : 'src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'dqm',            
            'isMC'      : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/mc/RunIIFall15MiniAODv1/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-scaledown-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/30000/00A5DDAA-7C9B-E511-930A-90B11C064B50.root',
        },
        'output'    : 'src/ntuplize.root',
    },
    'DQM_Data_76X' : {
        'category'  : 'DQM',
        'name'      : 'Data',
        'target'    : ['miniAOD_dev_76X'],
        'command'   : 'cmsRun',
        'config'    : 'src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'dqm',
            'maxEvents' : 1000,
            'inputFiles': '/store/data/Run2015D/MuonEG/MINIAOD/16Dec2015-v1/60000/04DA5209-60AB-E511-ACCD-008CFA0A57E8.root',
        },
        'output'    : 'src/ntuplize.root',
    },



    # wz analysis
    'WZ_MC_74X' : {
        'category'  : 'WZ',
        'name'      : 'MC',
        'target'    : ['miniAOD_dev_74X'],
        'command'   : 'cmsRun',
        'config'    : 'src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'eee,eem,emm,mmm', 
            'nExtraJets': 1, 
            'runWZ'     : 1,
            'isMC'      : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/mc/RunIISpring15MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/023437BD-2D7A-E511-9189-A0369F7FC5BC.root',
        },
        'output'    : 'src/ntuplize.root',
    },
    'WZ_Data_74X' : {
        'category'  : 'WZ',
        'name'      : 'Data',
        'target'    : ['miniAOD_dev_74X'],
        'command'   : 'cmsRun',
        'config'    : 'src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'eee,eem,emm,mmm',
            'nExtraJets': 1, 
            'runWZ'     : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/data/Run2015D/MuonEG/MINIAOD/PromptReco-v4/000/258/159/00000/64914E6C-F26B-E511-B0C8-02163E0142D1.root',
        },
        'output'    : 'src/ntuplize.root',
    },
    'WZ_MC_76X' : {
        'category'  : 'WZ',
        'name'      : 'MC',
        'target'    : ['miniAOD_dev_76X'],
        'command'   : 'cmsRun',
        'config'    : 'src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'eee,eem,emm,mmm',
            'nExtraJets': 1, 
            'runWZ'     : 1,
            'isMC'      : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/mc/RunIIFall15MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/022EC2EB-90B8-E511-AED0-0026B937D37D.root',
        },
        'output'    : 'src/ntuplize.root',
    },
    'WZ_Data_76X' : {
        'category'  : 'WZ',
        'name'      : 'Data',
        'target'    : ['miniAOD_dev_76X'],
        'command'   : 'cmsRun',
        'config'    : 'src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py',
        'arguments' : {
            'channels'  : 'eee,eem,emm,mmm',
            'nExtraJets': 1, 
            'runWZ'     : 1,
            'maxEvents' : 1000,
            'inputFiles': '/store/data/Run2015D/MuonEG/MINIAOD/16Dec2015-v1/60000/04DA5209-60AB-E511-ACCD-008CFA0A57E8.root',
        },
        'output'    : 'src/ntuplize.root',
    },

}


watchedVariables = {
    # list of variables this analysis tracks
    # format:
    # 'Analysis': { # must match 'category' from above
    #     # allowed modes, variables must match a leaf in the root file, unix * allowed, comma separated list
    #     'event' : [ ],       # style: 'varName'
    #     'dicandidate' : [ ], # style: 'object1_object2_varName'
    #     'candidate' : [ ],   # style: 'objectVarName'
    #     'electron' : [ ],    # style: 'objectVarName'
    #     'muon' : [ ],        # style: 'objectVarName'
    #     'tau' : [ ],         # style: 'objectVarName'
    #     'photon' : [ ],      # style: 'objectVarName'
    #     'jet' : [ ],         # style: 'objectVarName'
    #     'extraJet' : [ ],    # style: 'objectVarName'
    
    # dqm variables
    'DQM': {
        'event' : [
            '*',
        ],
        'candidate' : [
            'object*',
        ],
    },


    # wz variables
    'WZ': { 
        'event' : [
            # generator
            'GenDecayW*',
            'GenDecayZ*',
            'GenWeight',
            # event
            'evt',
            'lumi',
            'run',
            'Mass',
            'nTruePU',
            'nvtx',
            # vetos
            'jetVeto30',
            'bjetCISVVeto30Tight',
            'eVetoTrigIso*',
            'eVetoMedium*',
            'eVetoTight*',
            'muVetoMedium*',
            # triggers
            'doubleEPass',
            'doubleMuPass',
            'singleESingleMuPass',
            'singleMuSingleEPass',
            # met
            'type1_pfMetEt',
            'type1_pfMetPhi',
            'type1_pfMet_shifted*_*',
        ],
        'dicandidate': [
            'object1_object2_SS',
        ],
        'candidate' : [
            'objectPt',
            'objectEta',
            'objectPhi',
            'objectPt_*',
            'objectEta_*',
            'objectPhi_*',
        ],
        'electron' : [
            'objectPassWZLooseTrigIso*',
            'objectPassWZMedium*',
            'objectPassWZTight*',
            'objectRelPFIsoRho',
        ],
        'muon' : [
            'objectPassWZMediumTrigIso*',
            'objectPassWZMedium*',
            'objectRelPFIsoDBDefault',
        ],

    },

}

