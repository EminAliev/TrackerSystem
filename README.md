# Tracker System
Development team workflow support system
The purpose of the system is to provide the necessary tools for managing the team's work processes. 
Such as task tracker, version control subsystems, messaging, employees, control and verification, business processes.

# Building
It is best to use the python virtualenv tool to build locally:

```python
$ virtualenv-2.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ DEVELOPMENT=1 python manage.py runserver
```
Then visit http://localhost:8000 to view the app. 
