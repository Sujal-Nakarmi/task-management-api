1. Setup Instruction 

Step 1 : Clone the repository 

Open Terminal and paste the following code. 

For Windows  

git clone git@github.com:Sujal-Nakarmi/task-management-api.git 

For Mac 

git clone git@github.com:Sujal-Nakarmi/task-management-api.git 

 

STEP 2: Prerequisites 

	Check python installation  

	python --version or python3 –version 

	Installation Link  

Python Official Website for Windows 

https://www.python.org/downloads/windows/ 

Python Official Website for Mac

https://www.python.org/downloads/macos/

 

Step 3: Create Virtual Environment and Activate it  

Navigate to the project directory through the following command: 

cd folder-name  

cd task-management-api 

For Windows  

Commad to create = python -m venv taskManagementApi_venv 

Command to activate = taskManagementApi_venv\Scripts\activate 

For Mac 

Command to create = python3 -m venv taskManagementApi_venv 

Command to activate = source taskManagementApi_venv/bin/activate 

 

Step 4: Install Necessary Dependencies  

	Install all the Dependencies at once with the following  

	command = pip install -r requirements.txt or pip3 install -r requirements.txt 



Step 5: Create a .env file in the project root directory and add the following: 

	SECRET_KEY =  "f56ac7f556c4b6d406ac9832683190ab5303fba4908df799807602a245283afb" 

 


2. How to run the Project 

Step 1: Run the server  

Command = uvicorn main:app --reload

 

Step 2: Open Broswer  

Paste Link = http://127.0.0.1:8000/docs#/ 

You will see API Docs will be opend and there will be option for User to register, login, get profile, get all task, create task, get task, update task and delete task. 

 
 

3. Example API Requests 

Register 
POST /users/register

{ 

  "username": "Sam", 

  "email": "sam@gmail.com", 

  "password": "sam123" 

} 

Login  
POST /users/login
Username: Sam 
Password: sam123 

 

Get My Profile 
/users/me
Click Execute Button 

 

Create Task (requires token) 
/tasks/
Click on the Authorize button at the top right, enter only username and password and click on authorize 

{ 

  "title": "My First Task", 

  "description": "This is test task", 

  "completed": false,

  "priority": "high",

  "due_date": "2026-05-15T10:00:00"

} 

 

Get all task  
/tasks/
Click on Execute Button 

 

Get task 
/tasks/{task_id}
Enter Task id =  1 

 

Update Task  
/tasks/{task_id}
{ 

  "title": "My First Task", 

  "description": "This is updated test task", 

  "completed": true,

  "priority": "medium",

  "due_date": "2026-05-20T10:00:00"

} 

 

Delete Task 
/tasks/{task_id}
Enter Task id to delete  

Task id = 1 
