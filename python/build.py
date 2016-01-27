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

from comparisons import tests, watchedVariables

def execute(command):
    process = addProcess(command)
    lines_iterator = iter(process.stdout.readline, b"")
    for line in lines_iterator:
        sys.stdout.write(line)
    out = process.communicate()[0]
    result = process.returncode
    return result

def addProcess(command):
    print command
    process = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return process

def checkout(branch,name='FinalStateAnalysis'):
    command = 'git clone --recursive -b {0} https://github.com/uwcms/FinalStateAnalysis.git {1}'.format(branch,name)
    return execute(command)

def build(fsaDirectory,cmsswRelease,scramArch,name):
    nproc = addProcess('nproc').communicate()[0].strip()
    command = 'printenv;'
    command += 'export SCRAM_ARCH={0}\n'.format(scramArch)
    command += 'scram pro -n {0} CMSSW {1}\n'.format(name,cmsswRelease)
    command += 'pushd {0}/src\n'.format(name)
    command += 'eval `scramv1 runtime -sh`\n'
    command += 'git cms-init\n'
    command += 'cp -r {0} FinalStateAnalysis\n'.format(fsaDirectory)
    command += 'pushd FinalStateAnalysis/recipe\n'
    command += 'source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh\n'
    command += 'HZZ=1 ./recipe.sh\n'
    command += 'popd\n'
    command += 'export USER_CXXFLAGS="-Wno-delete-non-virtual-dtor -Wno-error=unused-but-set-variable -Wno-error=unused-variable -Wno-error=sign-compare -Wno-error=reorder"\n'
    command += 'nice scram b -j {0}\n'.format(int(int(nproc)/2.)+1)
    command += 'popd\n'
    return execute(command)

def cmsenv(cmsswBase):
    command = ''
    command += 'pushd {0}/src\n'.format(cmsswBase)
    command += 'eval `scramv1 runtime -sh`\n'
    return command

def compare(testDirectory,originalCmssw,updatedCmssw,testname,arguments):
    # run tests
    originalCommand = cmsenv(originalCmssw)
    updatedCommand = cmsenv(updatedCmssw)
    originalTest = '{0} {1}/{2} {3}\n'.format(arguments['command'],originalCmssw,arguments['config'],' '.join(['{0}={1}'.format(x,arguments['arguments'][x]) for x in arguments['arguments']]))
    updatedTest = '{0} {1}/{2} {3}\n'.format(arguments['command'],updatedCmssw,arguments['config'],' '.join(['{0}={1}'.format(x,arguments['arguments'][x]) for x in arguments['arguments']]))
    originalCommand += originalTest
    updatedCommand += updatedTest
    originalProcess = addProcess(originalCommand)
    updatedProcess = addProcess(updatedCommand)
    originalOut = originalProcess.communicate()[0]
    print originalCommand
    print originalOut
    updatedOut = updatedProcess.communicate()[0]
    print updatedCommand
    print updatedOut
    originalReturn = originalProcess.returncode
    updatedReturn = updatedProcess.returncode
    #if originalReturn: return originalReturn
    #if updatedReturn: return updatedReturn
    # verify files exist
    print 'verifying file exists'
    originalOutput = '{0}/{1}'.format(originalCmssw,arguments['output'])
    updatedOutput = '{0}/{1}'.format(updatedCmssw,arguments['output'])
    # run dqm comparison
    command = cmsenv(updatedCmssw)
    command += '$WORKSPACE/FSA-BuildTests/python/compareNtuples.py {0} {1} --directory {2}\n'.format(updatedOutput,originalOutput,testDirectory)
    execute(command)
    return 0

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Build FSA in CMSSW release')

    parser.add_argument('cmsswRelease',type=str,help='CMSSW release (CMSSW_X_Y_Z)')
    parser.add_argument('scramArch',type=str,help='SCRAM_ARCH with which to build CMSSW')
    parser.add_argument('--comparisonBranch', nargs='?', type=str, const='', help='Comparison branch to build (for comparison tests)')
    parser.add_argument('--comparisonCmsswRelease', nargs='?', type=str, const='', help='CMSSW release to compare against (if different than default)')
    parser.add_argument('--comparisonScramArch', nargs='?', type=str, const='', help='SCRAM_ARCH for comparison (if different than default)')
    parser.add_argument('--skipBuild',action='store_true',help='Skip the build (assume the builds already exist)')
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
    if not args.skipBuild:
        result = build(updatedFsaDirectory,args.cmsswRelease,args.scramArch,updatedName)

    # set build status

    # build comparison
    if args.comparisonBranch:
       name = 'FinalStateAnalysis_{0}'.format(args.comparisonBranch)
       if not args.skipBuild:
           checkout(args.comparisonBranch,name)
       originalFsaDirectory = '$WORKSPACE/{0}'.format(name)
       originalName = 'original'
       originalCmssw = '$WORKSPACE/{0}'.format(originalName)
       cmsswRelease = args.cmsswRelease if not args.comparisonCmsswRelease else args.comparisonCmsswRelease
       scramArch = args.scramArch if not args.comparisonScramArch else args.comparisonScramArch
       if not args.skipBuild:
           build(originalFsaDirectory,cmsswRelease,scramArch,originalName)

       # run comparisons
       htmlTemplate = '$WORKSPACE/FSA-BuildTests/www'
       htmlDir = '$WORKSPACE/www'
       execute('cp -r {0} $WORKSPACE'.format(htmlTemplate,htmlDir))
       for test in tests:
           testParams = tests[test]
           if args.comparisonBranch not in testParams['target']: continue
           testDir = '{0}/{1}'.format(htmlDir,test)
           compare(testDir,originalCmssw,updatedCmssw,test,testParams)

       # set statuses

if __name__ == "__main__":
    status = main()
    sys.exit(status)

