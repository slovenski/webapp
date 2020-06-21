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

    stage ('SCA') {
      steps {
        sh 'rm target/bom.xml || true'
        sh 'mvn -Dmaven.test.skip=true org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom' 
        sh '''
           curl -X 'POST' 'http://10.148.0.68:8888/api/v1/bom' \
                -H 'X-API-Key: tKXwCHetVavKwe91IKuwUM11F4058NIy' \
                -H 'Content-Type: multipart/form-data; charset=utf-8; boundary=__X_CURL_BOUNDARY__' \
                -F 'project=953b7220-4c8d-49da-b2e6-deee140994d5' \
                -F 'bom=target/bom.xml'
        '''      
        sh 'rm dependency-track.json || true'
        sh 'curl -X "GET" --header "Accept: application/json" "http://10.148.0.68:8888/api/v1/finding/project/953b7220-4c8d-49da-b2e6-deee140994d5/export" -o dependency-track.json'
        echo 'Upload Reports to DefectDojo..'
        sh 'python upload-results.py --host 10.148.0.68:8080 --api_key 9599ed3e73e6e266aa693a5892c2231b1ea522f4 --engagement_id 1 --result_file dependency-track.json --username admin --scanner "Dependency Track Finding Packaging Format (FPF) Export"'
      }
    }

    stage ('SAST') {
      steps {
        withSonarQubeEnv('sonar') {
          echo 'Doing Static application security testing process..'
          sh 'mvn sonar:sonar'
          sh 'cat target/sonar/report-task.txt'
        }
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
        echo 'Running DAST with Zed Attack Proxy..'
        sh '''
            rm zap-report.xml || true
            docker run --user root -v $(pwd):/zap/wrk/:rw --rm -v -t owasp/zap2docker-stable zap-baseline.py -t http://10.148.0.88:8080/webapp/?name=test -g gen.conf -x zap_report.xml || true
        '''
        echo 'Upload Reports to DefectDojo..'
        sh '''
            pip install requests
            chmod +x upload-results.py
            python upload-results.py --host 10.148.0.68:8080 --api_key 9599ed3e73e6e266aa693a5892c2231b1ea522f4 --engagement_id 1 --result_file zap_report.xml --username admin --scanner "ZAP Scan"
        '''
      }
    }
    
  }
}
