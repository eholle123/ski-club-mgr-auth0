# Ski Club Manager

## What is this project?

This is a web application to manage the distribution of ski passes in a ski club. In this case, a ski club is defined as a group of people who pool money to buy season passes to a ski area, then take turns using the passes.

## Why am I building this project?

I want to replace the current infrastructure used by my ski club: a Google Sheet and email. The current solution has the following problems:

* No system to submit requests for ski passes on specific days. Users simply add their names to the spreadsheet. Organizers must manually edit the spreadsheet to reject unreasonable reservations.
* Limited access control. Any user with access to the spreadsheet can modify or delete the reservations of other users.
* Limited auditing tools. The only history of reservations is stored in the document revision tracker.

## How am I building this project?

### Backend

Web backend using Python and the [FastAPI](https://fastapi.tiangolo.com/) package. Data is persisted in a Postgres database, using the [SQLModel](https://sqlmodel.tiangolo.com/) package for SQLAlchemy, validation, and serialization.

### User Interface and API

Simple multi-page web application. HTML templated using [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/). I used [Bootstrap CSS](https://getbootstrap.com/) for component styling.

A protected REST API is provided at `/api`. Read-only operations (`GET` requests) can be sent without authentication.

### Authorization and Authentication

[Auth0](https://auth0.com/) is used to authenticate access to the API. Requests must include an Authorization header containing a Bearer token signed by Auth0.