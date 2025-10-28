# Zomiggy: Food Delivery Web Application (Backend)
> **This backend is handling data of **5000+ restaurants** and their **2 lakh+ menu items** currently.**

Welcome to the backend of my full stack web application made in **Python** using ***Django Framework***. This repository contains database design, integration logic, external service management, environment management, and core logic of all RestAPIs that are used by *Frontend React Web Application*.

- **Live Demo**: https://food-delivery-frontend-lake.vercel.app/ 
- **Frontend Github Repo Link:** https://github.com/GreyHatStyle/Food-Delivery-frontend


## Table of Contents
1. [Why Django is Used?](#why-django-is-used)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [External Services Used](#external-services-used)
5. [About Deployment](#about-deployment)
6. [API Endpoints Documentation](#api-endpoints-documentation)
7. [Feedback](#feedback)
8. [Author](#author)


## Why Django is Used?
Django is a *batteries included framework*, meaning it comes with a comprehensive set of built-in tools and features that are commonly needed in development, hence results in faster development. 

Django features and libraries used are:
1. **Django REST Framework**: This is the main library used for building this REST API architecture, as it provides support for all basic features like *serializers*, *filters*, *ordering*, *searching*, *authentication*, *pagination*, *caching*, etc.

2. **Django Object Relational-Mapping (ORM)**: This default Django feature allows developers to define database schema and simplify CRUD (Create, Read, Update, Delete) operations using Python code, instead of SQL queries.

3. **Organised Directory Structure**: Django follows an organised default structure, like 
    - Database schema will be defined in `models` or `models.py`.
    - End point logic will be written in `views` or `views.py`.
    - End point configuration for serving will be written in `urls.py`
    - etc.

    Hence, it's easier to manage whenthe  project code increases.


## Features
- **Json Web Token Authentication**: Supports JWT authentication system for **login process**, the tokens are then sent to the client, which shall be used in all the **request header of Authorization key**, to access *authorized APIs*, like ordering food.
- **Supports URL Params**:  APIs for restaurant filter supports URL querying to get **dynamic results** based on client preferences **via a single endpoint**.
-   **CORS policy** has been applied, so that only "allowed" frontend URLs can access the api endpoints.


## Technology stack
Technology used in this project.

### Database
1. **PostgreSQL**: 
    - For Structured relational database models/tables, like *User accounts*, *Restaurants*, *Cart*, *Order* etc.
    - Django ORM directly supports PostgreSQL, with its functionalities.

2. **MongoDB**: 
    - For Unstructured relational database documents, like *Restaurant Menu* and *Restaurant Category*.
    - Since Django ORM doesn't directly supports MongoDB, an external library **mongoengine** is used to define schemas.
    - For CRUD operations, API logics are defined in *serializer classes*, with **aggregation pipelines** to let MongoDB Atlas take the maximum percentage of load for a request.  

3. **Redis**: For *caching*, *ratelimiting*, *user session management*, etc. 

### API Docs
1. **Scalar**: For modern look Api documentation, and displaying all required information about body input type, different response status, errors, etc.

## External Services Used
For serving this backend on the open web, the following services (some of them provided by the GitHub Education pack) are used:

1. **Supabase**: 
  - Supabase is an open-source **Backend-as-a-service platform**. 
  - Its free-tier hosted **PostgreSQL** database is used in this project to manage structured relational type data like user accounts and **5000+** restaurants, as shown below.

<img width="1912" height="623" alt="image" src="https://github.com/user-attachments/assets/a48a5e38-44d1-4968-9c83-245478f58fa9" />


2. **MongoDB Atlas**: MongoDB Atlas is a cloud-based database service, so in a hosted server, it helped to maintain the unstructured data like **2 lakh+** restaurant menu items, as shown below.
<img width="740" height="348" alt="image" src="https://github.com/user-attachments/assets/879e4243-67c5-43ef-8484-7ec453bd4fb3" />

3. **Appwrite**:
   - Appwrite is also a self-hosted backend server; however, only its *bucket feature* was used in this project, **to store images** of Menu items.
   - A Python script was run to extract downloadable images from Google and save them to the Appwrite bucket, **for 8 days** in one of Digital Ocean's droplets.
   - A few of them were unsuccessful and were replaced by a placeholder image.

<img width="1532" height="635" alt="image" src="https://github.com/user-attachments/assets/92894193-1d37-4fd9-8988-d57ba6fb41e5" />


4. **Digital Ocean**:
   - Digital Ocean is also a cloud infrastructure provider, which provided the **virtual machine** droplets for this project to host.
   - It also played a great role in running a Python script to extract images of 2 lakh+ Menu items for 8 days.

<img width="1299" height="804" alt="image" src="https://github.com/user-attachments/assets/babc621d-2274-4fbe-8800-54ac51fb0d0b" />


5. **Namecheap**: Namecheap is used for getting the domain "manasbishtsecond.me" and its DNS management to forward the requests to Digital Ocean's droplet **IPv4 address**.

## About Deployment:
1. **Apache2**: 
    - Apache2 is used for deploying the Django server on **, which was later deployed to **port 443** for a secure HTTPS connection.
    - It mainly takes the request and forwards it to Django using **Web Server Gateway Interface (WSGI)**, via the mod_wsgi library.

2. **CertBot**: 
    - It is a free, open-source software tool that automated the process of obtaining the **SSL/TLS certificates** for the domain.
    - Because of this, the backend server is now taking HTTPS-encrypted secure requests.
    
3. **Namecheap**: As mentioned above, the droplet's IPV4 address is provided to its DNS management system to forward the request to the droplet running this Django backend.

## API Endpoints Documentation
This is the scalar style documentation link for this backend: https://manasbishtsecond.me/docs

## Feedback
If you have any feedback, please reach me at manasbisht1142004@gmail.com.


## Author
- [@GreyHatStyle(Manas Bisht)](https://github.com/GreyHatStyle)