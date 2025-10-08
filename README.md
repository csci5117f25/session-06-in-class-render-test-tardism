## What steps do I need to do when I download this repo to get it running?

1. Install dependencies:
   ```
   pipenv install
   ```

2. Set up environment variable for database in .env file:
   ```
   DATABASE_URL=your_database_url
   ```

3. Activate the virtual environment:
   ```
   pipenv shell
   ```

## What commands starts the server?

```
gunicorn server:app
```

## Before render

Before render you will need to set up a more production-grade backend server process. We will do this together in lecture, once that's done you should update the command above for starting the server to be the production grade server.