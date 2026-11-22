# Django CRM

Use Python 3.12 and a supported PostgreSQL server. Create a virtual environment
with `python3.12 -m venv .venv`, activate it, then run
`python -m pip install -r requirements.txt`.

Set the variables shown in `.env.example` through your shell or hosting
platform. Django reads the process environment, so copying the example file
alone will not configure the application. Use a unique random Django
`SECRET_KEY` for each environment and keep it and the database password in
your password manager or hosting platform's secret store. Keep `DEBUG=False`
and set `ALLOWED_HOSTS` to explicit hostnames. For local use, include
`localhost,127.0.0.1`.

## Owner access

When bringing up an existing CRM, point the application at the existing
database so your Django user accounts and password hashes are preserved.
Take a database backup and verify the owner can sign in on a restored test
copy before deployment.

For a new database, run `python manage.py migrate`, then
`python manage.py createsuperuser`. Django prompts privately for the password.
Visit `/admin/` for account management or `/login/` for the CRM. To recover an
existing Django login, run `python manage.py changepassword YOUR_USERNAME`
against the intended database. This changes only that account's Django
password. It is separate from the PostgreSQL password and GitHub login.

Create staff users through Django admin. Assign the **Can view costumer**
permission for the CRM list and record pages, and grant add, change or delete
permissions as needed. Superusers have all model permissions.

Before using a network-facing deployment, run
`python manage.py check --deploy` with the actual deployment settings and
resolve HTTPS, cookie and other deployment warnings. Never reuse the signing
key or database password from the repository's older commits.

Run `python manage.py test` against a disposable PostgreSQL test setup.
Django needs permission to create and drop its test database.
