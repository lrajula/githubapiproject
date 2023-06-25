## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is about providing summary of last week open and closed PR's from the given github repository And also sends an summary of PR's email at a schedule intervel.
It also sends an email if the repository has not any PR's. 

Summary report includes: 
    - Open PR's
    - Open PR details 
    - Closed PR's
    - Closed PR details
	
## Technologies
Project is created with:
* Python Version: 3.10
* Docker version: 24.0.2
* GitHub API: https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/pulls?state=all&sort=created&direction=desc
	
## Install Steps
# Prerequistes:
* Install Python3.10
* Install any Docker version 


## Replace Below ENV Vars

* GITHUB_TOKEN=<GITHUB API TOKEN>
    Please follow this link to generate token https://github.com/settings/tokens
* GITHUB_USERNAME=<github repo username>
* GITHUB_REPO=<github repo name>


* SENDER_EMAIL=<provide sender gmail adress>
* RECEIVER_EMAIL=<receiver gmail address>
* SMTP_SERVER="smtp.gmail.com" <replace gmail server here>
* SMTP_PORT=587 <Replace gmail port>
* SMTP_USERNAME=<provide gmail sender address >
* SMTP_PASSWORD=<generated app gmail api token>
    Please follow api token generation here https://support.google.com/accounts/answer/185833?visit_id=638232731515859823-2397466037&p=InvalidSecondFactor&rd=1


To run this project, with Docker 

```
$ cd ../githubapipr_project
$ docker build -t <provide your any tag name as your wish> .
$ docker run -d --name <provide container name> <image tag name mentioned above>
```
To run this project, with Shell Script

```
$ cd ../githubapipr_project
$ sh start.sh
```
