#!/usr/bin/env python
'''
compareNtuples.py

Script to compare two histograms.

Usage:
    ./compareNtuples [-h] new_ntuple.root old_ntuple.roo

Author: Devin N. Taylor, UW-Madison
'''

import os
import sys
import errno
import argparse
import shutil

sys.argv.append('b')
import ROOT as rt
sys.argv.pop()

rt.gROOT.SetStyle("Plain")
rt.gROOT.SetBatch(True)
rt.gStyle.SetOptStat(0)
rt.gErrorIgnoreLevel = rt.kWarning

canvas = rt.TCanvas("asdf", "adsf", 800, 600)

def python_mkdir(dir):
    '''A function to make a unix directory as well as subdirectories'''
    try:
        os.makedirs(dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else: raise

def compare_ntuples(newNtuple,oldNtuple,**kwargs):
    '''
    Compare two ntuples via a chi2 test.
    Create histograms for each entry in the ntuple. Report differences and missing entries.
    arguments:
        Variable      Type (default)   Description
        doBinByBin    bool (False)     Do bin-by-bin comparison
    '''
    newFile = rt.TFile(newNtuple)
    oldFile = rt.TFile(oldNtuple)
    newChannels = [key.GetTitle() for key in newFile.GetListOfKeys()]
    oldChannels = [key.GetTitle() for key in oldFile.GetListOfKeys()]
    channels = []
    for chan in oldChannels:
        if chan not in newChannels:
            print 'Channel %s was not found in new ntuple.' % chan
        else:
            channels.append(chan)
    for chan in newChannels:
        if chan not in oldChannels:
            print 'Channel %s was not found in old ntuple.' % chan
    for chan in channels:
        savedir = 'DQM/all/%s' % chan
        python_mkdir(savedir)
        faildir = 'DQM/fail/%s' % chan
        python_mkdir(faildir)
        newTree = newFile.Get('%s/final/Ntuple' % chan)
        oldTree = oldFile.Get('%s/final/Ntuple' % chan)
        print 'Comparing channel %s' % chan
        newVariables = [leaf.GetName() for leaf in newTree.GetListOfLeaves()]
        oldVariables = [leaf.GetName() for leaf in oldTree.GetListOfLeaves()]
        variables = []
        for variable in oldVariables:
            if variable not in newVariables:
                print 'Variable %s was not found in new ntuple.' % variable
            else:
                variables.append(variable)
        for variable in newVariables:
            if variable not in oldVariables:
                print 'Variable %s was not found in old ntuple.' % variable
        for variable in variables:
            newName = 'hNew%s%s' % (chan, variable)
            oldName = 'hOld%s%s' % (chan, variable)
            newTree.Draw('%s>>%s' % (variable, newName))
            newHist = rt.gDirectory.Get(newName)
            oldTree.Draw('%s>>%s' % (variable, oldName))
            oldHist = rt.gDirectory.Get(oldName)
            pValue = newHist.Chi2Test(oldHist)
            chi2 = newHist.Chi2Test(oldHist,'CHI2')
            plot_hist(newHist,oldHist,'%s/%s.png' % (savedir,variable))
            if chi2:
                print '%s:%s: p-value = %0.3f, chi2 = %0.3f' % (chan, variable, pValue, chi2)
                shutil.copyfile('%s/%s.png' (savedir,variable), '%s/%s.png' % (faildir,variable))

def plot_hist(newHist,oldHist,savename):
    '''Plot a histogram with ratios.'''
    ratio = newHist.Clone('%sRatio' % newHist.GetTitle())
    ratio.Sumw2()
    ratio.SetMarkerSize(0.8)
    ratio.Divide(newHist,oldHist,1.,1.,'')

    histpad = rt.TPad('histPad', 'top pad', 0.0, 0.21, 1.0, 1.0)
    histpad.Draw()
    ratiopad = rt.TPad('ratiopad', 'bottom pad', 0.0, 0.0, 1.0, 0.21)
    ratiopad.SetTopMargin(0.)
    ratiopad.SetBottomMargin(0.5)
    ratiopad.SetFillColor(0)
    ratiopad.Draw()

    histpad.cd()

    oldHist.Draw('hist')
    newHist.Draw('esamex0')

    ratiopad.cd()

    ratiounity = rt.TLine(oldHist.GetXaxis().GetXmin(),1,oldHist.GetXaxis().GetXmax(),1)
    ratiounity.SetLineStyle(2)
    ratio.Draw('e')
    ratiounity.Draw('same')

    canvas.cd()

    canvas.Print(savename)

    

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Compare two ntuples')

    parser.add_argument('newNtuple', type=str, help='New ntuple for comparison.')
    parser.add_argument('oldNtuple', type=str, help='Old ntuple for comparison.')
    parser.add_argument('-db','--doBinByBin',action='store_true',help='Do bin-by-bin comparison')

    args = parser.parse_args(argv)
    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_command_line(argv)

    compare_ntuples(args.newNtuple,args.oldNtuple,doBinByBin=args.doBinByBin)

    return 0

if __name__ == "__main__":
    main()
