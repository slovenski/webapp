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
        echo 'Building..'
        sh 'mvn clean package'
      }
    }

    stage ('Deploy') {
      steps {
        sshagent(['tomcat']) {
          echo 'Deploying To Tomcat Server..'
          sh 'scp -o StrictHostKeyChecking=no target/*.war root@10.148.0.88:/prod/apache-tomcat-8.5.56/webapps/webapp.war'
        }      
      }       
    }

    stage ('DAST') {
      steps {
        echo 'Running DAST with Zed Attack Proxy (ZAP)'
        sh 'rm zap-report.xml || true'
        sh 'docker run --user root -v $(pwd):/zap/wrk/:rw --rm -v -t owasp/zap2docker-stable zap-baseline.py -t http://10.148.0.88:8080/webapp/?name=test -g gen.conf -x zap_report.xml || true'
        echo 'Upload Reports to DefectDojo'
        sh 'pip install requests'
        sh 'chmod +x upload-results.py'
   			sh 'python upload-results.py --host 10.148.0.89:8000 --api_key 1f564cd7b410b82868d90147eb4a0145ef975e0e --engagement_id 1 --result_file zap_report.xml --username admin --scanner "ZAP Scan"'
      }
    }

  }
}
