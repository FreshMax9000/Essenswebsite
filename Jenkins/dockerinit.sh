#!/bin/bash
cd /home/tobi/Dokumente/Softwareeng/Essenswebsite/Jenkins
case="$1"
sudo chmod 666 /var/run/docker.sock
if [ "$case" = "init" ]; then
	docker build https://github.com/TM-93/T2000.git#master:Jenkinscontainer -t djenkins 
	docker run -v /var/run/docker.sock:/var/run/docker.sock -d -i --name jenkinscontainer --mount source=jenkins-log,target=/var/log/jenkins --mount source=jenkins-data,target=/var/jenkins_home -d djenkins  


elif [ "$case" = "start" ]; then
	if [  "$(docker ps -q -a -f name=jenkinscontainer)"  ]
then
	if [ "$(docker ps  -q -f name=jenkinscontainer)"  ]
	then
	echo "läuft bereits"
	exit 1
	fi
	docker start jenkinscontainer
else 
	docker run -v /var/run/docker.sock:/var/run/docker.sock -d -i --name jenkinscontainer --mount source=jenkins-log,target=/var/log/jenkins --mount source=jenkins-data,target=/var/jenkins_home -d djenkins 
fi
	sudo chmod 666 /var/run/docker.sock
	echo "Jenkins gestartet"

elif [ "$case" = "stop" ]; then
	if [ "$(docker ps -q -f name=jenkinscontainer)"  ]
	then
		docker ps -q   |xargs docker stop
	fi

	
elif [ "$case" = "restart" ]; then
   docker ps -q -f name=jenkinscontainer |xargs docker stop
   sleep 10
   docker start jenkinscontainer



### Entfernen stopt den jenkinscontainer falls einer läuft und entfernt alle nicht benutzten/in Abhängigkeit stehende container und images  
elif [ "$case" = "delete" ]; then
	docker system prune -f 
	echo "all unused images and containers removed ."

elif [ "$case" = "remove" ]; then
	if [  "$(docker ps -q -f name=jenkinscontainer)"  ]
	then
		docker stop jenkinscontainer
	fi
docker rm jenkinscontainer

else 
	echo -e "helpmenu: \n init: neues Dockerfile bauen und Container starten \n start: einen gestoppten container wieder starten  \n stop: stoppen aller aktuellen Container \n restart: neustarten des jenkinscontainers \n remove: stop jenkinscontainer and  remove it \n delete : delete all unused images and contaienrs"
fi

exit 0
