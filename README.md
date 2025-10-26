# Zomiggy: Food Delivery Web Application (Backend)

Welcome to the backend of my full stack web application made in **Python** using ***Django Framework***. This repository contains database design, integration logic, external service management, environment management, and core logic of all RestAPIs that are used by *Frontend React Web Application*.

## Table of Contents
1. [Why Django is Used?](#why-django-is-used?)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [External Services Used](#external-services-used)
5. [About Deployment](#about-deployment)
6. [API Endpoints Documentation](#api-endpoints-documentation)
7. [Feedback](#feedback)
8. [Author](#author)


## Why Django is Used?
Django is a *batteries included framework*, meaning it comes with a comprehensive set of built-in tools and features, that are commonly needed in development, hence results in faster development. 

Django features and libraries used are:
1. **Django REST Framework**: This is the main library used for building this RestAPI architecture, as it provides support of all basic features like *serializers*, *filters*, *ordering*, *searching*, *authentication*, *pagination*, *caching* etc.

2. **Django Object Relational-Mapping (ORM)**: This default Django feature allows developer to define database schema and simplify CRUD (Create, Read, Update, Delete) operations using python code, instead of SQL queries.

3. **Organized Directory Structure**: Django follows an organized default structure, like 
    - Database schema will be defined in `models` or `models.py`.
    - End point logic will be written in `views` or `views.py`.
    - End point configuration for serving will be written in `urls.py`
    - etc.

    Hence it's easier to manage when project code increases.


## Features
- **Json Web Token Authentication**: Supports JWT authentication system for login (write it when okay)


## Technology stack
Technology used in this project.

### Database
1. **PostgreSQL**: 
2. **MongoDB**:

### Backend Server:
1. **Django**
2. **Redis**

### API Docs
1. **Scalar**


## External Services Used
For serving this backend in open web, following services are used:
1. **Supabase**
2. **MongoDB Atlas**
3. **Appwrite**
4. **Digital Ocean**
5. **Namecheap**

## About Deployment:
1. Apache2
2. CertBot
3. Namecheap

## API Endpoints Documentation
https://manasbishtsecond.me/docs

## Feedback
If you have any feedback, please reach me at manasbisht1142004@gmail.com.


## Author
- [@GreyHatStyle(Manas Bisht)](https://github.com/GreyHatStyle)