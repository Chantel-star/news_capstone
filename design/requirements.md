# Requirements Specification – News Application

## 1. Introduction

This document outlines the functional and non-functional requirements
for the News Application. The purpose of this application is to allow
journalists and publishers to manage news articles while providing
third-party clients access to articles through a RESTful API.

## 2. Functional Requirements

### User Management

1. The system will allow users to register and log in.
2. The system allows support from different user roles: Reader, Journalist,
   and Publisher.

### Article Management

1. Journalists need to be able to create, edit, and delete articles.
2. Publishers must be able to approve or reject submitted articles.
3. Only approved articles will be visible to the public.

### Article Viewing

1. Readers must be able to view published articles.
2. Articles are all organised by category.

### API Functionality

1. The system will expose a RESTful API for retrieving articles.
2. Third-party API clients shall be able to retrieve articles by:
   - Publisher
   - Journalist
3. The API will return in responses in JSON format.

## 3. Non-Functional Requirements

### Performance

1. The system has to respond to the API requests within an acceptable time
   under normal load.

### Security

1. The system has to restrict sensitive actions using authentication
   and authorisation.
2. API access needs to be protected using token-based authentication.

### Usability

1. The user interface needs to be simple, clear, and easy to navigate.
2. The application has to be responsive across different screen sizes.

### Scalability

1. The system will support the addition of new publishers and
   journalists without requiring major system changes.

### Maintainability

1. The system will follow Django best practices to ensure the code
   is maintainable and readable.

### Reliability

1. The system will use MariaDB as the primary database for data
   persistence.
