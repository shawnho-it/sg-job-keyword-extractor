pipeline {
  agent any

  stages {
    stage('Clone Repo') {
      steps {
        checkout([$class: 'GitSCM',
          branches: [[name: '*/reorg']],
          userRemoteConfigs: [[
            url: 'https://github.com/shawnho-it/sg-job-keyword-extractor.git',
          ]]
        ])
      }
    }

    stage('Install Requirements') {
      steps {
        sh '''
          python3 -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
        '''
      }
    }

    stage('Restart Gunicorn') {
      steps {
        sh '''
          pkill gunicorn || true
          nohup gunicorn --bind 0.0.0.0:5000 app:app &
        '''
      }
    }
  }
}

