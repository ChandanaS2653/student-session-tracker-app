# 🎓 Student Session Tracker App

This is a serverless web application built using AWS services that enables students to register, log in, and track their login/logout sessions. The app calculates total session time and optionally sends notifications.

## 🚀 Technologies Used
- **AWS Lambda** – backend logic (Python)
- **Amazon API Gateway** – RESTful API interface
- **Amazon DynamoDB** – stores user and session data
- **Amazon S3** – hosts the frontend HTML pages
- **CloudFormation** – infrastructure as code
- **JavaScript, HTML, CSS** – frontend interface

## 🧩 Features
- Student registration with hashed password storage
- Secure login/logout tracking
- Session duration calculation
- Notification endpoint (optional)
- Fully deployed via AWS CloudFormation
- S3-hosted static website frontend

## 🛠 Lambda Functions
- `register` – register a new user
- `login` – authenticate user and start session
- `logout` – end session and store duration
- `session` – view current session state
- `notify` – optional alerts or messages

## 📁 Folder Structure
session-tracking-app/
├── register_lambda/
├── login_lambda/
├── logout_lambda/
├── session_lambda/
├── notify_lambda/
├── frontend/ ← index.html, dashboard.html
├── student-session-template.yaml


## 📦 Deployment
Deploy the full stack using AWS CLI:
```bash
aws cloudformation deploy \
  --template-file student-session-template.yaml \
  --stack-name StudentSessionStack \
  --capabilities CAPABILITY_NAMED_IAM
