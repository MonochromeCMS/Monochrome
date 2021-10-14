# Monochrome
 My attempt at a generic manga CMS

## Usage
Monochrome requires (at least for now) a copy of this repository, [docker](https://docs.docker.com/engine/install/) 
and [docker-compose](https://docs.docker.com/compose/install/) to run.

Once those requirements are fulfilled you need to set up your [.env](#environment-settings) and simply run 
`make install`, and the different services will be launched.

## Flavors
Two different "flavors" are available:
* `caddy` Includes PWA support, HTTPS (requires a domain name and to be the only web server on the machine),
  and optimisations, the one you most likely want. `make flavor=caddy install`
* `nginx` Same as production but without the HTTPS, in case you have other web servers and
  have a reverse proxy or want to handle the HTTPS yourself (ex. intranet). `make flavor=nginx install`

## Environment settings
Monochrome uses a `.env` file to take your settings,
an example is provided [here](.env.example).

### Variables
*Note: The database should be isolated by docker and only accessible by the Monochrome API, however using 
unique username and password is very recommended.*

* `DB_NAME` Name for the database.
* `DB_USER` User to connect the database with.
* `DB_PWD` Password of that user.
* `SECRET_KEY` Secret used to encrypt the connections, change it asap.
* `SESSION_SECRET_KEY` Secret used to encrypt the session of the client, change it as well.

*Note: Those can and are recommended to be completely random, to generate them you can use* `make secret`

* `PROTOCOL` `http` or `https`, if you use a flavor that doesn't handle HTTPS automatically, you'll still have to set it up on your own.
* `DOMAIN_NAME` The domain the app will be available on, ex: `manga.d34d.one` or `localhost`

* `ACCESS_TOKEN_EXPIRE_MINUTES` Basically after how many minutes a user should be logged out, the default is 6 hours.

* `TITLE` Name of your website, used for stuff like the title of the tab when you open the website.
* `DESCRIPTION` Description of your website.

# Screenshots
## Home page
![Screenshot 1](.github/assets/monochrome_1.png)
## Responsive layout
![Screenshot 2](.github/assets/monochrome_2.png)
## Light and dark themes
![Screenshot 3](.github/assets/monochrome_3.png)
## Chapter upload
![Screenshot 4](.github/assets/monochrome_4.png)
## Website customization
![Screenshot 5](.github/assets/monochrome_5.png)

## Services used
Check those, for more information on the services that make Monochrome:
* [Monochrome WebUI](https://github.com/MonochromeCMS/monochrome-webui)
* [Monochrome API - Postgres](https://github.com/MonochromeCMS/monochrome-api-postgres)
  
Credits:
* Base API template: https://github.com/grillazz/fastapi-sqlalchemy-asyncpg
* Logo font: Lemon Milk by [Marsnev](https://marsnev.com/)
