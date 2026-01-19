# RESTful API Design – News Application

## 1. Overview

The News Application exposes a RESTful API that allows third-party
clients to retrieve published news articles. The API supports filtering
articles by publisher and journalist.

## 2. API Architecture

- Protocol: HTTP/HTTPS
- Data Format: JSON
- Authentication: Token-based authentication
- Base URL: /api/

## 3. API Endpoints

### Retrieve all approved articles

**GET** `/api/articles/`

Description:
Returns a list of all approved articles.

### Retrieve articles by publisher

**GET** `/api/articles/?publisher_id={id}`

Description:
Returns approved articles associated with a specific publisher.

### Retrieve articles by journalist

**GET** `/api/articles/?journalist_id={id}`

Description:
Returns approved articles written by a specific journalist.

### Retrieve a single article

**GET** `/api/articles/{id}/`

Description:
Returns details of a single approved article.

## 4. Example API Response

```json
{
  "id": 1,
  "title": "Breaking News",
  "content": "Article content goes here",
  "journalist": "Jane Doe",
  "publisher": "Daily Times",
  "category": "Politics",
  "published_date": "2026-01-12"
}


