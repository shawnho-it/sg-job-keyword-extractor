pipeline {
  agent any

  environment {
    IMAGE_NAME = "job-scraper"
    CONTAINER_NAME = "job-scraper-container"
  }

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

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $IMAGE_NAME .'
      }
    }

    stage('Run Container') {
      steps {
        sh '''
          docker rm -f $CONTAINER_NAME || true
          docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
        '''
      }
    }
  }
}

