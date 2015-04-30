#!/bin/bash

###########################################################
# Script to extract a previous jenkins build
#
# Usage:
#    ./extract.sh --cmssw-release=CMSSW_X_Y_Z
#
# Author: Devin N. Taylor, UW-Madison
###########################################################

for i in "$@"
do
case $i in
    -c=*|--cmssw-release=*)
    CMSSW_RELEASE="${i#*=}"
    shift
    ;;
    *)
    # unknown option
    ;;
esac
done

export CMS="/cvmfs/cms.cern.ch"
export VO_CMS_SW_DIR=$CMS
export LCG_GFAL_INFOSYS=exp-bdii.cern.ch:2170
export CMSSW_MIRROR=http://mirror.hep.wisc.edu/upstream/cmssw.git/
source ${CMS}/cmsset_default.sh
alias scram=scramv1
export CMSSW_GIT_REFERENCE=/scratch/jenkins/.cmsgit-cache

# setup previous build
tar zxf fsa_build.tar.gz
cd $CMSSW_RELEASE/src
cmsenv
scram b ProjectRename
cmsenv
source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh
export USER_CXXFLAGS="-Wno-delete-non-virtual-dtor -Wno-error=unused-but-set-variable -Wno-error=unused-variable -Wno-error=sign-compare -Wno-error=reorder"
cd $WORKSPACE
