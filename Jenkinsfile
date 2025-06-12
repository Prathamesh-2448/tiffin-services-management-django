@Library("My-Shared") _
pipeline{
    agent { label 'vinod' }
    
    stages {
        stage('Hello'){
            steps{
                script{
                    hello()
                }
            }
        }
        stage('Code'){
            steps{
                script{
                 clone("https://github.com/Prathamesh-2448/tiffin-services-management-django.git", "main")   
                }
            }
        }
        stage('Build'){
            steps{
                script{
                    docker_build("tiffin-app","latest")
                }
            }
        }
        stage('Push to DockerHub'){
            steps{
                script{
                    push_dockerHub("tiffin-app", "latest")
                }
            }
        }
        stage('Deploy'){
            steps{
                echo 'Deploying the code'
                sh 'docker run -d -p 8000:8000 tiffin-app:latest'
            }
        }
        }
    }
