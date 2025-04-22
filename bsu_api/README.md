## Requirements

In order to run the api you need

- Python 3.12 or > since latest features possible will be used

## Installation

> Create a virtual environment using your preferred tool (I.E. virtualenv, pyenv, ...)

```bash
python3.12 -m venv venv

# unix
source venv/bin/activate

# windows (cmd/powershell)
.\venv\Scripts\activate
```

> Install the necessary requirements

```bash
(venv) > pip install -r requirements.txt
```

> Run the server

All the environment variables are listed inside the `.env.example` file, you can load them by creating a `.env` file and push them into that file.

With Docker for now it is possible specify them when running the container (`OVERRIDE_SYSTEM` needs to be set to "false").

```bash
(venv) > uvicorn main:app --reload
```

This is useful when running in development mode, since we can have the auto-reload feature. However when building/testing as if the serveer was in production mode it is better to

```bash
(venv) > uvicorn main:app --workers 4
```

These are the numbers of processes that uvicorn will spawn for you. It is recommended that this number is equal to the number of CPU cores.

There are other flags you can use (--host, --port, etc.) but I think there is no need for an explanation, moeover you can read the `Dockerfile` which already implements a working architecture.

## What about the routes?

How can I see which routes are available and what kind of data do they request and return? That is easy you just need to go to

```
/doc
/redoc
```

![Docs URL](images/image.png)

These two routes contain metadata about our application and can be also used to test that. They are based off the OpenAPI Swagger standard.

## QRCodes

You can both encode/decode qrcodes via file path or base64 string. By doing so you have two choices when constructing your logic and adjust it based on your needs.

In order to decode qrcodes you need to install (besides the usual dependencies) `pyzbar` on your machine unless when using Windows.

## Connection with the database
Prisma requires a client. The client is a auto-generated and type-safe query builder that's tailored to your data.(As stated in the [documentation](https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/introduction))

the Prisma client requires a schema file (usually : schema.prisma) which is a file that defines: 
- the "models" (tables in your DB) , 
- your datasource (your URL where your DB is located)
- and your generator (which is your DB provider, the one that allows you to send SQL statements to your DB) 

Once the prisma file is made and Prisma is INSTALLED you  can run "prisma generate" in the root of the project. \ 
Afterwards, you can also run "prisma studio" which offers a GUI to the database for developement.

![Prisma Studio](./images/Prisma_studio.png)

## Aruco Markers

The same applies to aruco markers, they will be used to reference the zone and can be generated/decoded using both the file path or base64 in case you don't want to store them on the disk.

```bash
# macos
brew install pyzbar

# linux
sudo apt-get install libzbar0
```

## Testing

When building a production app, it is important to implement tests to mock HTTP Requests, analyze utilities functions, etc.

For this reason the directory `tests` will contain all the necessary tests. In order to run them type

```bash
(venv) > pytest
```

Pytest will load all the files that contains the keyword `test` and run all the functions that contain `test`. If you want to debug you just need to add:

```bash
(venv) > pytest -s
```