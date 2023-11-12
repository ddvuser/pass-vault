# PassVault

PassVault is a simple password manager built with Django, Docker, and PostgreSQL.

## Installation

1. Clone the repository:

    ``` bash
        git clone https://github.com/ddvuser/pass-vault.git
    ```

2. Environment configuration:

    1. `.env.dev`
    2. `.env.db.dev`
    3. `.env.prod`
    4. `.env.db.prod`

    Contents of `.env.dev` and `.env.prod` should look like this:

    ```env
        DEBUG=1
        SECRET_KEY=change_me
        DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
        DB_ENGINE=django.db.backends.postgresql
        DB_NAME=postgres
        DB_USER=postgres
        DB_PASSWORD=postgres
        DB_HOST=db
        DB_PORT=5432
        DATABASE=postgres
        CSRF_TRUSTED_ORIGINS=localhost:1337
    ```

    Contents of `.env.db.dev` and `.env.db.prod` should look like this:

    ```env
        POSTGRES_DB=postgres
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=postgres
    ```

    Adjust the values in these files based on your specific requirements.

3. For development, start the application with Docker Compose:

    ```bash
        docker-compose -f docker-compose.dev.yml up --build
    ```

4. For production, use:

    ```bash
        docker-compose -f docker-compose.prod.yml up --build
    ```

## Usage

1. After setting up the application, access it in your web browser.

2. Create an account to get started.

3. Begin adding your passwords along with additional information such as name, password, email, and notes.

## Contributing

Contributions are welcome! If you would like to contribute to PassVault, feel free to open issues, submit pull requests, or provide feedback.

## License

This project is licensed under the MIT License.
