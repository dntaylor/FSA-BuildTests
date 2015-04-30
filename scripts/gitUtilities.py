# general utilities to produce github api commands
import os
import sys
import subprocess

apiurl = 'https://api.github.com'
token = os.environ.get('GITTOKEN')

def makeCommand(token,command,data,url):
    '''Create command'''
    if command:
        commandString = 'curl -H "Authorization: token %s" -X %s -d "%s" %s' \
                        % (token, command, data, url)
    else:
        commandString = 'curl -H "Authorization: token %s" -d "%s" %s' \
                        % (token, data, url)
    return commandString

def convertToJson(dictionary):
    '''Convert python dictionary to json for command.'''
    command = '{'
    for key,val in dictionary.iteritems():
        command += '\\"%s\\":\\"%s\\",' % (str(key),str(val))
    command = command[:-1] # strip trailing ,
    command += '}'
    return command
    
def buildLabels():
    '''Create all labels for monitoring progress'''
    user = 'dntaylor'
    repo = 'FinalStateAnalysis'
    statuses = {
        'In Progress': 'ffcc00',
        'Successful': '009900',
        'Failed': 'cc0000',
    }
    modes = ['Build','DQM']
    for m in modes:
        for n,c in statuses.iteritems():
            labelName = '%s: %s' % (m,n)
            labelData = convertToJson({'name':labelName,'color':c})
            url = '%s/repos/%s/%s/labels' % (apiurl, user, repo)
            command = makeCommand(token,'',labelData,url)
            os.system(command)
