pipeline {
  agent any

  tools {
    maven 'Maven'
  }

  stages {
    stage ('Initialize') {
      steps {
        sh '''
                echo "PATH = ${PATH}"
                echo "M2_HOME = ${M2_HOME}"
           '''
      }
    }

    stage ('Build') {
      steps {
      sh 'mvn clean package'
       }
    }

    stage ('Deploy') {
            steps {
           sshagent(['tomcat']) {
                sh 'scp -o StrictHostKeyChecking=no target/*.war root@10.148.0.88:/prod/apache-tomcat-8.5.56/webapps/webapp.war'
              }      
           }       
    }

    stage ('DAST') {
      steps {
        sh 'rm zap-report.xml || true'
        sh 'docker run --user root -v $(pwd):/zap/wrk/:rw --rm -v -t owasp/zap2docker-stable zap-baseline.py -t http://10.148.0.88:8080/webapp/?name=test -g gen.conf -x zap_report.xml || true'
      }
    }

  }
}
