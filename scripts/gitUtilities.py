# general utilities to produce github api commands
import os
import sys
import subprocess

from github import Github

#######################################
### Available environment variables ###
#######################################
token             = os.environ.get('GITTOKEN')                     # custom variable for git token
pullId            = os.environ.get('ghprbPullId')                  # the pull request number
buildUrl          = os.environ.get('BUILD_URL')                    # jenkins url for build information
pullUrl           = os.environ.get('ghprbPullLink')                # url to pull request
branchSource      = os.environ.get('ghprbSourceBranch')            # branch that wants to merge
commitAutherEmail = os.environ.get('ghprbActualCommitAuthorEmail') # email address of commit
mergeCommitId     = os.environ.get('GIT_COMMIT')                   # git commit (not the actualy one, the merge)
branchTest        = os.environ.get('sha1')                         # the branch to test name, the merge of the pr with the target
jenkinsUrl        = os.environ.get('JENKINS_URL')                  # jenkins url
commitId          = os.environ.get('ghprbActualCommit')            # the actual commit
gitUrl            = os.environ.get('GIT_URL')                      # url to git
commitAuthor      = os.environ.get('ghprbActualCommitAuthor')      # the real commit author
branchTarget      = os.environ.get('ghprbTargetBranch')            # the branch you want to merge into
buildNumber       = os.environ.get('BUILD_NUMBER')                 # the number of the build

username, reponame = gitUrl.split(':')[1].split('.')[0].split('/')

######################
### Github objects ###
######################
g = Github(token)
user = g.get_user(username)
repo = user.get_repo(reponame)
pull = repo.get_pull(pullId)
issue = repo.get_issue(pullId)
commit = repo.get_commit(commitId)

##################
### Parameters ###
##################
statuses = {
    'In Progress': 'ffcc00',
    'Successful': '009900',
    'Failed': 'cc0000',
    'Changes': 'ffcc00',
}
dqmtests = ['Basic']
dqmtestcontent = {}
dqmcomment = ''

#########################
### General utilities ###
#########################
def post_label(labelName,color='333333'):
    '''Post a label (check if exists first)'''
    labelNames = [l.name for l in repo.get_labels()]
    if labelName not in labelNames:
        label = repo.create_label(labelName,color)
    else:
        label = repo.get_label(labelName)
    label.edit(labelName,color) # in case color changes
    issue.add_to_labels(label)

def remove_label(*labelNames):
    '''Remove a label (check if exists first)'''
    for label in issue.get_labels():
        if label.name in labelNames:
            issue.remove_from_labels(label)

############################
### Build status updates ###
############################
def begin_build():
    remove_label('Build: Failed','Build: Successful')
    post_label('Build: In Progress',statuses['In Progress'])

def end_build_successful():
    remove_label('Build: In Progress','Build: Failed')
    post_label('Build: Successful',statuses['Successful'])
    content = 'The build was successful.'

def end_build_failure():
    remove_label('Build: Successful','Build: In Progress')
    post_label('Build: Failure',statuses['Failure'])
    content = 'The build failed.'

##########################
### DQM status updates ###
##########################
def make_dqm_content(content):
    '''Generate the content for a dqm result comment'''
    comment = content + '\n==============\n\n'
    for key,value in dqmtestcontent.iteritems():
        comment += '%s\n-------------\n\n' % key
        comment += '%s\n\n' % value
    return comment

def begin_dqm():
    remove_label('DQM: Successful','DQM: Failure','DQM: Changes')
    post_label('DQM: In Progress',statuses['In Progress'])
    content = 'DQM tests are now running.'
    for dqmtest in dqmtests:
        dqmtestcontent[dqmtest] = 'In progress.'
    content = make_dqm_content(content)
    dqmcomment = issue.create_comment(content) # new test, new comment

def update_dqm(testname,results):
    content = 'DQM tests are now running.'
    dqmtestcontent[testname] = '%s' % results
    content = make_dqm_content(content)
    if dqmcomment:
        dqmcomment.edit(content)
    else:
        dqmcomment = issue.create_comment(content)

def end_dqm_successful():
    remove_label('DQM: In Progress','DQM: Failure','DQM: Changes')
    post_label('DQM: Successful',statuses['Successful'])
    content = 'DQM tests have completed successfully.'
    content = make_dqm_content(content)
    if dqmcomment:
        dqmcomment.edit(content)
    else:
        dqmcomment = issue.create_comment(content)

def end_dqm_failure():
    remove_label('DQM: Successful','DQM: In Progress','DQM: Changes')
    post_label('DQM: Failure',statuses['Failure'])
    content = 'DQM tests have completed with failures.'
    content = make_dqm_content(content)
    if dqmcomment:
        dqmcomment.edit(content)
    else:
        dqmcomment = issue.create_comment(content)

def end_dqm_changes():
    remove_label('DQM: Successful','DQM: Failure','DQM: In Progress')
    post_label('DQM: Changes',statuses['Changes'])
    content = 'DQM tests have completed with changes.'
    content = make_dqm_content(content)
    if dqmcomment:
        dqmcomment.edit(content)
    else:
        dqmcomment = issue.create_comment(content)

