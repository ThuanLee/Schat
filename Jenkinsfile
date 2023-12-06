pipeline {
    agent any
    environment {
        scannerHome = tool 'SonarScanner'
    }
    stages {
        stage('Check operation') { 
            steps {
                echo 'Hello, welcome you to Jenkins'
            }
        }
        stage('Sonar anlysis') {
            steps {
                echo 'Start setup to anlysis'
                withSonarQubeEnv('SonarCloud') {
                    sh "${scannerHome}/bin/sonar-scanner \
                    -Dsonar.projectKey=thuanlee215_schat \
                    -Dsonar.organization=thuanlee215 \
                    -Dsonar.inclusions=backend/** "
                }    
            }
        }
    }
    post {
        always {
            echo 'See you again!!'
        }
        success {
            echo 'Let come https://sonarcloud.io/project/overview?id=thuanlee215_schat to see result'
        }
        failure {
            echo 'I failed :('
        }
    }    
}
