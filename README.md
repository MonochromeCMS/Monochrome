# Monochrome
 My attempt at a generic manga CMS

## Usage
Monochrome requires (at least for now) a copy of this repository, [docker](https://docs.docker.com/engine/install/) 
and [docker-compose](https://docs.docker.com/compose/install/) to run.

Once those requirementes are fulfilled you need to setup your [.env](#Environment settings) and simply run 
`make install` and the different services will be launched.

## Environment settings
Monochrome uses a `.env` file to take your settings,
an example is provided [here](/D34DPlayer/Monochrome/blob/main/.env.example).

### Variables
*Note: The database should be isolated by docker and only accessible by the Monochrome API, however using 
unique username and password is very recommended.*

* `DB_NAME` Name for the database.
* `DB_USER` User to connect the database with.
* `DB_PASSWORD` Password of that user.
* `SECRET_KEY` Secret used to encrypt the connections, change it asap.

*Note: Those can and are recommended to be completely random, to generate them you can use* `make secret`

## Tools used
* API
  * FastAPI
  * SQLAlchemy
  * Alembic
  * Pydantic
* VueJS

## Progress
* API
  * Creation <span style="color: green">100%</span>
  * Documentation <span style="color: yellow">42%</span>
    * OpenAPI <span style="color: orange">33%</span>
    * Cleaner code <span style="color: yellow">50%</span>
  * Testing <span style="color: red">0%</span>
    * Unit <span style="color: red">0%</span>
    * Integration <span style="color: red">0%</span>
* Frontend 
  * Creation <span style="color: red">0%</span>
    * Latest chapters <span style="color: red">0%</span>
    * Search <span style="color: red">0%</span>
    * Manga page <span style="color: red">0%</span>
      * Chapter list <span style="color: red">0%</span>
    * Chapter reader <span style="color: red">0%</span>
* Reverse proxy 
  * Creation <span style="color: red">0%</span>
    * Serve frontend <span style="color: red">0%</span>
    * Serve media <span style="color: red">0%</span>
    * Reverse proxy the API <span style="color: red">0%</span>
* Find a way to deploy this more easily
  * Heroku?
  * Docker swarm?
  * Kubernetes?
  
Credits:
* Base template: https://github.com/grillazz/fastapi-sqlalchemy-asyncpg
* Logo font: Lemon Milk by [Marsnev](https://marsnev.com/)