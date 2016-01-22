#!/usr/bin/env python
'''
A script to build a comparison between releases

Author: Devin N. Taylor, UW-Madison
'''

import os
import sys
import argparse
import logging
import subprocess

from comparisons import tests

def execute(command):
    process = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    lines_iterator = iter(process.stdout.readline, b"")
    for line in lines_iterator:
        sys.stdout.write(line)
    out = process.communicate()[0]
    result = process.returncode
    return result

def checkout(branch,name='FinalStateAnalysis'):
    command = 'git clone --recursive -b {0} https://github.com/uwcms/FinalStateAnalysis.git {1}'.format(branch,name)
    return execute(command)

def build(fsaDirectory,cmsswRelease,scramArch,name):
    command = ''
    command += 'export CMS="/cvmfs/cms.cern.ch"\n'
    command += 'export VO_CMS_SW_DIR=$CMS\n'
    command += 'export LCG_GFAL_INFOSYS=exp-bdii.cern.ch:2170\n'
    command += 'export CMSSW_MIRROR=http://mirror.hep.wisc.edu/upstream/cmssw.git/\n'
    command += 'source ${CMS}/cmsset_default.sh\n'
    command += 'alias scram=scramv1\n'
    #command += 'export CMSSW_GIT_REFERENCE=/scratch/jenkins/.cmsgit-cache\n'
    command += 'export CMSSW_GIT_REFERENCE=/nfs_scratch/dntaylor/.cmsgit-cache\n'
    command += 'export SCRAM_ARCH={0}\n'.format(scramArch)
    command += 'scram pro -n {0} CMSSW {1}\n'.format(name,cmsswRelease)
    command += 'pushd {0}/src\n'.format(name)
    command += 'cmsenv\n'
    command += 'git cms-init\n'
    command += 'mv {0} FinalStateAnalysis\n'.format(fsaDirectory)
    command += 'pushd FinalStateAnalysis/recipe\n'
    command += 'source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh\n'
    command += './recipe.sh\n'
    command += 'popd\n'
    command += 'export USER_CXXFLAGS="-Wno-delete-non-virtual-dtor -Wno-error=unused-but-set-variable -Wno-error=unused-variable -Wno-error=sign-compare -Wno-error=reorder"\n'
    command += 'nice scram b -j 16\n'
    command += 'popd\n'
    return execute(command)

def compare(originalCmssw,updatedCmssw,testname,arguments):
    return 0

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Build FSA in CMSSW release')

    parser.add_argument('cmsswRelease',type=str,help='CMSSW release (CMSSW_X_Y_Z)')
    parser.add_argument('scramArch',type=str,help='SCRAM_ARCH with which to build CMSSW')
    parser.add_argument('--comparisonBranch', nargs='?', type=str, const='', help='Comparison branch to build (for comparison tests)')
    parser.add_argument('--comparisonCmsswRelease', nargs='?', type=str, const='', help='CMSSW release to compare against (if different than default)')
    parser.add_argument('--comparisonScramArch', nargs='?', type=str, const='', help='SCRAM_ARCH for comparison (if different than default)')
    parser.add_argument('-l','--log',nargs='?',type=str,const='INFO',default='INFO',choices=['INFO','DEBUG','WARNING','ERROR','CRITICAL'],help='Log level for logger')

    args = parser.parse_args(argv)

    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    loglevel = getattr(logging,args.log)
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', level=loglevel, datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # build release
    updatedFsaDirectory = '$WORKSPACE/FinalStateAnalysis'
    updatedName = 'updated'
    updatedCmssw = '$WORKSPACE/{0}'.format(updatedName)
    result = build(updatedFsaDirectory,args.cmsswRelease,args.scramArch,updatedName)

    # set build status

    # build comparison
    if args.comparisonBranch:
       name = 'FinalStateAnalysis_{0}'.format(args.comparisonBranch)
       checkout(args.comparisonBranch,name)
       originalFsaDirectory = '$WORKSPACE/{0}'.format(name)
       originalName = 'original'
       originalCmssw = '$WORKSPACE/{0}'.format(originalName)
       cmsswRelease = args.cmsswRelease if not args.comparisonCmsswRelease else args.comparisonCmsswRelease
       scramArch = args.scramArch if not args.comparisonScramArch else args.comparisonScramArch
       build(originalFsaDirectory,cmsswRelease,scramArch,originalName)

       # run comparisons
       for test in tests:
           testParams = tests[test]
           compare(originalCmssw,updatedCmssw,test,testParams)

       # set statuses

if __name__ == "__main__":
    status = main()
    sys.exit(status)

