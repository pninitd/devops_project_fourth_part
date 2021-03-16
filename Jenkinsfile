pipeline {
	agent any
	options {
		buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
	}
	environment {
        registry = "pninit/devops_project_fourth_part"
        registryCredential = 'docker_hub'
        dockerImage = ''
    }
	stages {
		stage('checkout') {
			steps {
				script {
					properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
				}
                // checkout from the url that defined in the jenkins job (git 'https://github.com/pninitd/devops_project_fourth_part.git')
				checkout scm
			}
		}
		stage('install missing dependencies') {
			steps {
				script {
					if (isUnix()) {
						sh 'pip install flask werkzeug requests pymysql -t ./'
					} else {
						bat 'pip install flask werkzeug requests pymysql -t ./'
					}
				}
			}
		}
		stage('run backend server') {
			steps {
				script {
					runPythonFileBackground('rest_app.py')
				}
			}
		}
		stage('run backend testing') {
			steps {
				script {
					runPythonFile('backend_testing.py test')
				}
			}
		}
		stage('run clean environment') {
			steps {
				script {
					runPythonFile('clean_environment.py')
				}
			}
		}
		stage('Build and push Docker image') {
			steps {
				script {
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                    }
				}
			}
		}
		stage('Set image version') {
			steps {
				script {
					sh "echo IMAGE_TAG=${BUILD_NUMBER} > .env"
				}
			}
		}
		stage('Start docker container') {
			steps {
				script {
					sh "docker-compose up -d"
				}
			}
		}
		stage('Test container') {
			steps {
				script {
					runPythonFile('docker_backend_testing.py')
				}
			}
		}
	}
	post {
	    always {
	        script {
	            sh "docker-compose down"
                sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }
        // 	Extra: send email in case of failure
// 	    failure {
// 	        mail body: "Jenkins-${JOB_NAME}-${BUILD_NUMBER} FAILED Check what is the issue: $env.JOB_URL",
// 	        bcc: '', cc: '', from: 'Jenkins@gmail.com', replyTo: 'no-reply@gmail.com',
// 	        subject: "Jenkins-${JOB_NAME}-${BUILD_NUMBER} FAILED", to: 'pninit.dvir@gmail.com'
// 	    }
	}
}

def runPythonFile(pyfilename){
// run python file, used for the testing files and fail the build in case of error
	try{
		if (isUnix()) {
			sh "python ${pyfilename}"
		} else {
			bat "python ${pyfilename}"
		}
	} catch (Throwable e) {
		echo "Caught in runPythonFile for ${pyfilename}, ${e.toString()}"
		// mark the job as failed
		currentBuild.result = "FAILURE"
	}
}

def runPythonFileBackground(pyfilename){
// run python file in the background, used for the apps
	try{
		if (isUnix()) {
			sh "nohup python ${pyfilename} &"
		} else {
			bat "start /min python ${pyfilename}"
		}
	}
	catch (Throwable e) {
		echo "Caught in runPythonFileBackground for ${pyfilename} ${e.toString()}"
	}
}