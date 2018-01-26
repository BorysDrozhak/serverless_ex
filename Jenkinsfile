#!/usr/bin/env groovy

pipeline {
  agent any

  stages {

    stage('check py lambda sripts') {
        steps {
            sh "cd lambda-scrapers; make check"
        }
    }
  }
}