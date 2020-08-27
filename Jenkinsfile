pipeline {
    agent any

    stages {
        stage('Build docker image') {
            steps {
                checkout scm
                sh "./restapi/build.sh ${BRANCH_NAME}"
            }
        }

        stage('Update docker swarm service') {
            steps {
                script {

                    String fullContainerName;
                    String imageName = "id/cmsapi-zms3"
                    boolean isProduction = false;

                    switch (env.BRANCH_NAME) {
                        case 'master':
                            fullContainerName = "prod-cmsapi_zms3"
                            isProduction = true;
                            break
                        case 'develop':
                            fullContainerName = "dev-cmsapi_zms3"
                            break
                        case ~/^release\/(.*)/:
                            fullContainerName = "test-cmsapi_zms3"
                            break
                        default:
                            fullContainerName = "dev-cmsapi_zms3"
                            break
                    }

                    if (fullContainerName != "") {
                        timeout(5) {
                            milestone 1
                            lock('zms') {
                                ch.unibe.id.workflowlibs.DockerUtil dockerUtil = new ch.unibe.id.workflowlibs.DockerUtil()
                                dockerUtil.updateService(fullContainerName, imageName, isProduction)
                            }
                        }
                    } else {
                        echo "Ignoring branch " + env.BRANCH_NAME
                    }

                }
            }
        }
    }
}
