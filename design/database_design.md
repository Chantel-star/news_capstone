# Database Design and Normalisation – News Application

## 1. Overview

The News Application uses a relational database to store user, article,
publisher, and category information. The database design follows
normalisation principles to reduce redundancy and improve data integrity.

---

## 2. Entities and Attributes

### User

- id (Primary Key)
- username
- email
- password
- role (Reader, Journalist, Publisher)

### Publisher

- id (Primary Key)
- name

### Category

- id (Primary Key)
- name

### Article

- id (Primary Key)
- title
- content
- created_at
- status (Pending, Approved, Rejected)
- journalist_id (Foreign Key → User)
- publisher_id (Foreign Key → Publisher)
- category_id (Foreign Key → Category)

---

## 3. Relationships

- One Journalist can write many Articles
- One Publisher can approve many Articles
- One Category can contain many Articles
- Each Article belongs to one Journalist, one Publisher, and one Category

---

## 4. Normalisation

### First Normal Form (1NF)

- All tables contain atomic values
- No repeating groups exist

### Second Normal Form (2NF)

- All non-key attributes fully depend on the primary key
- No partial dependencies exist

### Third Normal Form (3NF)

- No transitive dependencies exist
- Non-key attributes depend only on the primary key

The database schema is therefore normalised to Third Normal Form (3NF).

---

## 5. Database Technology

The application uses MariaDB as the database management system to ensure
scalability, reliability, and compatibility with production environments.
