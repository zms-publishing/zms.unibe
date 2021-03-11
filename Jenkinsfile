pipeline {
    agent any
    stages {
        stage('Build docker images') {
            steps {
                checkout scm
                sh "./build.sh ${BRANCH_NAME}"
            }
        }
        stage('Update docker swarm service') {
            steps {
                script {
                    String stack;
                    switch (env.BRANCH_NAME) {
                        case ~/^release\/(.*)/:
                            stack = "test";
                            break
                        default:
                            stack = "dev";
                    }
                    timeout(5) {
                        milestone 1
                        lock('zms') {
                            ch.unibe.id.workflowlibs.DockerUtil dockerUtil = new ch.unibe.id.workflowlibs.DockerUtil()
                            dockerUtil.updateService(stack + "-unibe-cms_api", "id/unibe-cmsapi")
                        }
                    }
                }
            }
        }
    }
}
