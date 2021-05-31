package com.libs

def deinstVm(remote_ip, deplId, ssh_cfy) {
string r_ip = remote_ip

def remote = [:]
remote.name = r_ip
remote.host = r_ip
remote.allowAnyHosts = true

  withCredentials([sshUserPrivateKey(credentialsId: ssh_cfy, keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName'),
]) {
        remote.user = userName
        remote.identityFile = identity
sshCommand remote: remote, command: "cfy uninstall -f ${params.depl_id} -p 'ignore_failure=true' || true"
sshCommand remote: remote, command: "rm -rf ${params.depl_id}.IP"
}}
return this