package com.libs

def remoteBuild(d_dirp, s_dirp, component_name, ci_branch_repo, git_branch_repo, ssh_creds, remote_ip) {

string r_ip = remote_ip
string d_dir = d_dirp
string s_dir = s_dirp
string cmpt_id = component_name
string ci_rep = ci_branch_repo
string git_rep = git_branch_repo

def remote = [:]
remote.name = r_ip
remote.host = r_ip
remote.allowAnyHosts = true

  withCredentials([sshUserPrivateKey(credentialsId: ssh_creds, keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName'),
      usernamePassword(credentialsId: '5gt-ci', usernameVariable: 'u5g', passwordVariable: 'p5g')]) {
        remote.user = userName
        remote.identityFile = identity

    sh 'rm -rf repo'
    sshCommand remote: remote, command: "rm -rf $d_dir || true"
    sshCommand remote: remote, command: "sudo docker rm -f \$(sudo docker ps -a | grep $cmpt_id | awk '{ print \$1}')  || true"
    sshCommand remote: remote, command: "mkdir -p -m 0777 $d_dir"

    git(
       branch: "${params.ci_branch_mon}",
       url: 'https://github.com/5growth/5gr-ci/',
       credentialsId: '5gt-ci',
    )
    sh "mkdir -p repo"
    sh "mv containerization repo/"

    def  FILES_LIST = sh (script: "ls   $s_dir", returnStdout: true).trim()
    for(String item : FILES_LIST.split("\\r?\\n")){ 
    sshPut remote: remote, from: "$s_dir/$item", into: "$d_dir", override: true
    }

    sshCommand remote: remote, command: "chmod -R +x /home/ubuntu/$d_dir || true"

    sshCommand remote: remote, command: "sed -i 's/GIT_BRANCH=.*/GIT_BRANCH=$git_rep/' $d_dir/${cmpt_id}build_docker.sh"
    sshCommand remote: remote, command: "chmod +x $d_dir/${cmpt_id}build_docker.sh"
}}
return this
