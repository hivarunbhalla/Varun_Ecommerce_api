# Django REST Framework API Project

## Overview
This Django project showcases advanced use of Django REST Framework (DRF) with implementations for RESTful APIs, file uploads, email handling, automated testing, and JWT-based authentication. The project includes functionalities for shopping cart management, user authentication, image uploads, and more.

DEMO: https://youtu.be/mOJflvE2SKc?si=fKGFunyEadA4gxmM

## Features
- **RESTful APIs**: Efficient API creation and management.
- **File Uploads**: Handling and validation of file uploads, including image management.
- **Email Functionality**: Sending emails with attachments and configuring email backends.
- **Automated Testing**: Comprehensive setup for automated testing, including continuous integration.
- **JWT Authentication**: Secure authentication using JSON Web Tokens (JWT).

## Technologies Used
- **Django**: Web framework for building the application.
- **Django REST Framework**: Toolkit for creating Web APIs.
- **Python**: Programming language used for development.
- **Nested Routers**: Used nested routers for endpoints like 'products/products_pk/reviews/pk'.
- **Database**:Any Database management system supported by django.
- **Simple_JWT**: JWT authentication for DRF (Authentication Backend).
- **Djoser**: Library for handling JWT tokens.

## Installation

### Prerequisites
- Python 3.x
- pip
- pipEnv

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hivarunbhalla/Varun_Ecommerce_api.git
    ```

2. **Navigate to the Project Directory:**:
   ```bash
   cd Varun_Ecommerce_api
   ```
3. **Create, Activate and Install Dependencies using pipenv Virtual Environment:**:
   ```bash
   pip install pipenv
   pipenv install
   pipenv shell
   ```
4. **Apply Migrations:**:
   ```bash
   python manage.py migrate
   ```
5. **Create a Superuser:**:
   ```bash
   python manage.py createsuperuser
   ```
   
5. **Start the Development Server:**:
   ```bash
   python manage.py runserver
   ```

# API Endpoints

## API Root

The base URL for the API is available at `http://127.0.0.1:8000/store/`:

- **GET /store/**

  Response:
  ```json
  {
      "product": "http://127.0.0.1:8000/store/product/",
      "collections": "http://127.0.0.1:8000/store/collections/",
      "cart": "http://127.0.0.1:8000/store/cart/",
      "customers": "http://127.0.0.1:8000/store/customers/",
      "orders": "http://127.0.0.1:8000/store/orders/"
  }

## Shopping Cart API

- **Create Cart**: `POST http://127.0.0.1:8000/store/cart/`
  - Create a new shopping cart.
- **Retrieve Cart**: `GET http://127.0.0.1:8000/store/cart/{cart_id}/`
  - Get details of a specific cart.
- **Add Item**: `POST http://127.0.0.1:8000/store/cart/{cart_id}/items/`
  - Add an item to a specific cart.
- **Update Item**: `PUT http://127.0.0.1:8000/store/cart/{cart_id}/items/{item_id}/`
  - Update an item in a specific cart.
- **Delete Item**: `DELETE http://127.0.0.1:8000/store/cart/{cart_id}/items/{item_id}/`
  - Remove an item from a specific cart.

## JWT Authentication Endpoints

- **Create JWT**: `POST http://127.0.0.1:8000/auth/jwt/create/`
  - Obtain a new JSON Web Token (JWT).
- **Refresh JWT**: `POST http://127.0.0.1:8000/auth/jwt/create//jwt/refresh/`
  - Refresh an existing JWT.
- **Verify JWT**: `POST http://127.0.0.1:8000/auth/jwt/create//jwt/verify/`
  - Verify the validity of a JWT.

## Djoser Auth Endpoints

- **List Users**: `GET http://127.0.0.1:8000/auth/users/`
  - List all users.
- **Retrieve Current User**: `GET http://127.0.0.1:8000/auth/users/me/`
  - Get the current authenticated user's details.
- **Confirm User**: `POST http://127.0.0.1:8000/auth/users/confirm/`
  - Confirm user account.
- **Resend Activation**: `POST http://127.0.0.1:8000/auth/users/resend_activation/`
  - Resend activation email to the user.
- **Set Password**: `POST http://127.0.0.1:8000/auth/users/set_password/`
  - Set or update the user's password.
- **Reset Password**: `POST http://127.0.0.1:8000/auth/users/reset_password/`
  - Initiate password reset process.
- **Confirm Password Reset**: `POST http://127.0.0.1:8000/auth/users/reset_password_confirm/`
  - Confirm the password reset process.
- **Set Username**: `POST http://127.0.0.1:8000/auth/users/set_username/`
  - Set or update the user's username.
- **Reset Username**: `POST http://127.0.0.1:8000/auth/users/reset_username/`
  - Initiate username reset process.
- **Confirm Username Reset**: `POST http://127.0.0.1:8000/auth/users/reset_username_confirm/`
  - Confirm the username reset process.

## File Uploads API

- **Upload Image to a Product**: `POST http://127.0.0.1:8000/store/product/{product_pk}/images/`
  - Upload an image file.
- **Retrieve All Image of a Product**: `GET http://127.0.0.1:8000/store/product/{product_pk}/images/`
  - Retrieve all images by its ID.
- **Retrieve All Image of a Product**: `GET  http://127.0.0.1:8000/store/product/{product_pk}/images/{id}`
  - Retrieve a specific image by its ID.

## File Uploads

- **Managing Media Files**: Configure and handle media file uploads and validations.
- **Image Upload API**: Endpoints for uploading and retrieving images.
- **Admin Integration**: Thumbnail support for uploaded images in the admin panel.

## Automated Testing

- **Introduction**: Overview of automated testing principles and benefits.
- **Running Tests**: How to execute tests and debug issues.
- **Continuous Testing**: Implement continuous integration for ongoing test automation.
- **Debugging in VSCode**: Instructions for running and debugging tests in Visual Studio Code.


## Key Features

- **RESTful API**: Full implementation of REST principles.
- **JWT Authentication**: Secure authentication using JSON Web Tokens.
- **File Handling**: Upload and manage files, including images.
- **Filtering and Sorting**: Advanced query capabilities for searching and organizing data.
- **Automated Testing**: Comprehensive test suite for ensuring code quality and reliability.

# Contributing

1. **Fork the Repository**.
2. **Create a New Branch**: `git checkout -b feature-branch`.
3. **Make Changes and Commit**: `git commit -am 'Add new feature'`.
4. **Push to Your Fork**: `git push origin feature-branch`.
5. **Create a Pull Request**.
