# Refget Server - Python

A reimplementation of the Refget standard using Python. This tool uses 

# Running the example server

```bash
$ poetry install
$ FLASK_APP=run.py poetry run flask run
 * Serving Flask app 'run.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

## Running in dev mode
```bash
$ FLASK_ENV=development FLASK_APP=run.py poetry run flask run
 * Serving Flask app 'run.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 305-952-899
```

## Example server contents

This will give you access to the server locally on port 5000 and has four sequences loaded

- `NC_001422.1` (Escherichia phage phiX174): `ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF` & MD5 `3332ed720ac7eaa9b3655c06f6b9e196`
- `BK006935.2` (Saccharomyces cerevisiae S288C chromosome I): `ga4gh:SQ.lZyxiD_ByprhOUzrR1o1bq0ezO_1gkrn` & MD5 `6681ac2f62509cfc220d78751b8dc524`
- `BK006940.2` (Saccharomyces cerevisiae S288C chromosome VI): `ga4gh:SQ.z-qJgWoacRBV77zcMgZN9E_utrdzmQsH` & MD5 `b7ebc601f9a7df2e1ec5863deeae88a3`
- `ACGT`: `ga4gh:SQ.aKF498dAxcJAqme6QYQ7EZ07-fiw8Kw2` & MD5 `ga4gh:SQ.f1f8f4bf413b16ad135722aa4591043e`

These are held in the `db.sqlite` database. You can retrieve these sequences with the following types of comamnds:

```bash
$ curl -s -H"Accept: application/json" "http://0.0.0.0:5000/sequence/ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF/metadata"
{"metadata":{"aliases":[{"alias":"NC_001422.1","naming_authority":"insdc"}],"ga4gh":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","id":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","length":5386,"md5":"3332ed720ac7eaa9b3655c06f6b9e196"}}

$ curl -s -H"Accept: application/json" "http://0.0.0.0:5000/sequence/3332ed720ac7eaa9b3655c06f6b9e196/metadata"
{"metadata":{"aliases":[{"alias":"NC_001422.1","naming_authority":"insdc"}],"ga4gh":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","id":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","length":5386,"md5":"3332ed720ac7eaa9b3655c06f6b9e196"}}

$ curl -s -H"Accept: application/json" "http://0.0.0.0:5000/sequence/insdc:NC_001422.1/metadata"
{"metadata":{"aliases":[{"alias":"NC_001422.1","naming_authority":"insdc"}],"ga4gh":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","id":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","length":5386,"md5":"3332ed720ac7eaa9b3655c06f6b9e196"}}
```

# Customising the instance

## Injecting new configuration

The application's default configuration is held in `app/config.py`. You can provide another configuration file to override the existing values using the `REFGET_SETTINGS` environment variable.

## Special config variables

### `SQLALCHEMY_DATABASE_URI`

Change the datbase connection settings

### `SERVICE_INFO`

Configure the service info returned from the code. Best to just duplicate and edit as you see fit

### `STREAMED_CHUNKING_SIZE`

Set to a value greater than 0 to enable streaming of sequences. Note doing this will result in executing substrings

### `SQLALCHEMY_ECHO`

Set to `True` to have SQLAlchemy emit the SQL it is generating. Useful to understand what's going on under the hood

## Moving to a new database

We do not recommend using SQLite in production instances. Instead you should use something like MySQL or Postgres. To do this you should:

- Create a database/schema
- Provide a new config value for `SQLALCHEMY_DATABASE_URI` pointing to the new database location & schema
  - Provide a R/O account for added security
- Run the migration scripts (we provide Alembic migrations)
- Populate with data

Alembic can be run with the following command.

```bash
$ REFGET_SETTINGS="path/to/new/config.py" FLASK_APP=run.py flask db upgrade
```

### Populating a database with new records

**Make sure you have created a new database first as noted in the previous section**. Loading is available through the `loader.py` variable. You can give this a FASTA file plus additional options (use `--help` to see all options).

```bash
REFGET_SETTINGS="path/to/new/config.py" poetry run python3 loader.py --fasta FILE --authority insdc --type dna
```

The script writes only the sequence records and molecules to your active database. The script has been tested but not extensively.

# Regengerating the local SQLite compliance database

```bash
rm compliance.sqlite3
poetry run python3 create_compliance_database.py
```

This will use the local application's default settings, which is a file in the current directory called `compliance.sqlite3`.

# Creating sequence reports

Utilities are available to generate a report of the various supported checksums by refget in CSV format using the `fasta-to-report.py` tool. You can provide this a FASTA formatted file (gzipped or uncommpressed) and the code will output a CSV report. Additional command line options are available using `--help`.

```bash
poetry run python3 fasta-to-report.py --fasta INPUT.fa.gz 
```

# Running tests

```bash
$ poetry run python -m unittest tests/*.py
.........
----------------------------------------------------------------------
Ran 9 tests in 0.286s

OK
```
