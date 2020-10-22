# Task Manager Project

This project is to create a task manager using MongoDB, Python, Heroku.

# Requirements
`pip3 install flask`
`pip3 install flask-pymongo`
`pip3 install dnspython`

# Styling
Using Materialize - developed by google

## Start app on heroku
heroku ps:scale web=1

# Notes
Task DB fields
        {{ task.task_name }}
        {{ task.category_name }}
        {{ task.task_description }}
        {{ task.is_urgent }}
        {{ task.due_date }}