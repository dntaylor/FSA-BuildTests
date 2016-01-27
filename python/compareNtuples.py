#!/usr/bin/env python
'''
compareNtuples.py

Script to compare two histograms.

Usage:
    ./compareNtuples [-h] new_ntuple.root old_ntuple.root

Author: Devin N. Taylor, UW-Madison
'''

import os
import sys
import errno
import argparse
import shutil
import re

import ROOT as rt

rt.gROOT.SetBatch(rt.kTRUE)
rt.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
rt.gROOT.SetStyle("Plain")
rt.gStyle.SetOptStat(0)


from variableParameters import *

mapVariables = {
  'e': electronVariables,
  'm': muonVariables,
  't': tauVariables,
  'g': photonVariables,
  'j': jetVariables,
}

def getParameters(variable):
    '''Function to match variable to available parameters'''
    # first check event
    if variable in eventVariables: return eventVariables[variable]
    # next check for candidates
    v = re.sub('[emtgj]\d?','object',variable,1)
    if v in candidateVariables: return candidateVariables[v]
    if variable[0] in 'emtgj':
        if v in mapVariables[variable[0]]: return mapVariables[variable[0]][v]
        if v in extraJetVariables: return extraJetVariables[v]
    # finally, dicandidate variables
    vs = variable.split('_')
    if len(vs)>2:
        vs[0] = 'object1'
        vs[1] = 'object2'
        v = '_'.join(vs)
        if v in dicandidateVariables: return dicandidateVariables[v]
    # not there
    return []

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
        savedir       string (DQM)     directory to save output histograms
    '''
    savedir = kwargs.pop('savedir','DQM')
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
        python_mkdir(savedir)
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
            binning = getParameters(variable)
            if len(binning)==3:
                newDrawString = '%s>>%s(%s)' % (variable,newName,','.join(str(x) for x in binning))
                oldDrawString = '%s>>%s(%s)' % (variable,oldName,','.join(str(x) for x in binning))
            else:
                newDrawString = '%s>>%s' % (variable,newName)
                oldDrawString = '%s>>%s' % (variable,oldName)
            newTree.Draw(newDrawString)
            newHist = rt.gDirectory.Get(newName)
            oldTree.Draw(oldDrawString)
            oldHist = rt.gDirectory.Get(oldName)
            pValue = newHist.Chi2Test(oldHist)
            chi2 = newHist.Chi2Test(oldHist,'CHI2')
            plot_hist(newHist,oldHist,'%s/%s_%s.png' % (savedir,chan,variable))
            if not chi2:
                os.system('rm %s/%s_%s.png' % (savedir,chan,variable))
            else:
                print '%s:%s: p-value = %0.3f, chi2 = %0.3f' % (chan, variable, pValue, chi2)

def plot_hist(newHist,oldHist,savename):
    '''Plot a histogram with ratios.'''

    canvasname = 'c_' + savename.replace('.','_')

    rt.gStyle.SetOptTitle(0)

    canvas = rt.TCanvas(canvasname, canvasname, 800, 600)
    canvas.SetGrid()
    canvas.SetTopMargin(0.12)
    canvas.SetLeftMargin(0.06)
    canvas.SetRightMargin(0.01)
    canvas.SetBottomMargin(0.06)

    #ratio = newHist.Clone('%sRatio' % newHist.GetTitle())
    #ratio.Sumw2()
    #ratio.SetMarkerSize(0.8)
    #ratio.Divide(newHist,oldHist,1.,1.,'')

    #histpad = rt.TPad('histPad', 'top pad', 0.0, 0.21, 1.0, 1.0)
    #histpad.SetLeftMargin(0.06)
    #histpad.SetRightMargin(0.01)
    #histpad.SetTopMargin(0.0875)
    #histpad.SetBottomMargin(0.06)
    #histpad.SetTickx(1)
    #histpad.SetTicky(1)
    #histpad.Draw()
    #ratiopad = rt.TPad('ratiopad', 'bottom pad', 0.0, 0.0, 1.0, 0.21)
    #ratiopad.SetTopMargin(0.)
    #ratiopad.SetBottomMargin(0.5)
    #ratiopad.SetLeftMargin(0.06)
    #ratiopad.SetRightMargin(0.01)
    #ratiopad.SetFillColor(0)
    #ratiopad.SetTickx(1)
    #ratiopad.SetTicky(1)
    #ratiopad.Draw()

    #histpad.cd()

    oldHist.SetLineColor(1)
    oldHist.Draw('hist')
    newHist.SetLineColor(2)
    newHist.Draw('hist same')

    legend = rt.TLegend(0.72,0.89,0.99,0.93)
    legend.SetNColumns(2)
    legend.AddEntry(oldHist,'Ref.','l')
    legend.AddEntry(newHist,'New','l')
    legend.Draw()

    #ratiopad.cd()

    #ratiounity = rt.TLine(oldHist.GetXaxis().GetXmin(),1,oldHist.GetXaxis().GetXmax(),1)
    #ratiounity.SetLineStyle(2)
    #ratio.Draw('e')
    #ratiounity.Draw('same')

    canvas.cd()

    canvas.Print(savename)

    

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Compare two ntuples')

    parser.add_argument('newNtuple', type=str, help='New ntuple for comparison.')
    parser.add_argument('oldNtuple', type=str, help='Old ntuple for comparison.')
    parser.add_argument('-d','--directory',nargs='?',type=str,const='',help='Output save directory')

    args = parser.parse_args(argv)
    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_command_line(argv)

    compare_ntuples(args.newNtuple,args.oldNtuple,savedir=args.directory)

    return 0

if __name__ == "__main__":
    main()
