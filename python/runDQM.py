#!/usr/bin/env python

import argparse
import subprocess
from multiprocessing import Pool
from gitUtilities import *

def run_dqm(job):
    '''Run a job for a given DQM path'''
    failed = False
    if job=='Basic':
        makeNtuples = subprocess.call('cmsRun $fsa/NtupleTools/test/make_ntuples_cfg.py channels="dqm,mm" isMC=1 inputFiles=root://cmsxrootd.fnal.gov//store/mc/Phys14DR/ZZTo4L_Tune4C_13TeV-powheg-pythia8/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/04CD96C9-E269-E411-9D64-00266CF9ADA0.root maxEvents=1000', shell=True)
        if not makeNtuples:
            # now compareNtuples with last good ntuplize.root
            pass
            # and now check for same output
        else:
            failed = True

    if failed: return 'Failed'

    return 'Successful'

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="Run DQM")

    args = parser.parse_args(argv)
    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    begin_dqm()

    # multiprocessing jobs
    p = Pool(4)
    results = p.map(run_dqm,dqmtests)

    if all([x=='Successful' for x in results]):
        end_dqm_successful()
    elif any([x=='Failed' for x in results]):
        end_dqm_failure()
    else:
        end_dqm_changes()

    return 0

if __name__ == "__main__":
    main()
