
## 📌 Project Overview

This Django-based News Application allows readers to view articles published
by journalists and publishers. Editors review and approve articles before
they are published. The system supports subscriptions, notifications, and a
RESTful API for third-party access.

---

## Technologies Used

- Python 3.x
- Django 5.x
- Django REST Framework
- MariaDB
- HTML (Django Templates)
- Requests (external API integration)

---

## User Roles & Permissions used

### Reader

- View approved articles
- Subscribe to publishers
- Subscribe to journalists

### Journalist

- Create, update, delete articles
- Publish independently
- View own content

### Editor

- Review articles
- Approve or reject articles
- Manage published content

Permissions are enforced using Django Groups and Permissions.

---

## Database Design

The database is fully normalised and includes:

- Custom User model with role-based fields
- Publisher model
- Article model with approval workflow
- Subscription relationships

---

## Article Approval Workflow

1. Journalist submits an article
2. Editor reviews the article
3. On approval:
   - Email notifications are sent to subscribed readers
   - The article becomes publicly visible

---



## Testing

Automated unit tests were written using Django’s testing framework to verify:

- Subscription-based filtering
- Approved-only content access
- API response correctness

Tests can be run using:

```bash
python manage.py test
