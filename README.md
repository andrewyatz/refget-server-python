# Refget Server - Python

An implementation of the Refget v2.0.0 standard using Python. This tool uses:

- Poetry
- Flask
- SQLAlchemy
- ga4gh.vrs
- biopython

## Running the example server

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

### Running in dev mode

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

### Example server contents

This will give you access to the server locally on port 5000 and has four sequences loaded

- `NC_001422.1` (Escherichia phage phiX174): `ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF` & MD5 `3332ed720ac7eaa9b3655c06f6b9e196`
- `BK006935.2` (Saccharomyces cerevisiae S288C chromosome I): `ga4gh:SQ.lZyxiD_ByprhOUzrR1o1bq0ezO_1gkrn` & MD5 `6681ac2f62509cfc220d78751b8dc524`
- `BK006940.2` (Saccharomyces cerevisiae S288C chromosome VI): `ga4gh:SQ.z-qJgWoacRBV77zcMgZN9E_utrdzmQsH` & MD5 `b7ebc601f9a7df2e1ec5863deeae88a3`
- `ACGT`: `ga4gh:SQ.aKF498dAxcJAqme6QYQ7EZ07-fiw8Kw2` & MD5 `f1f8f4bf413b16ad135722aa4591043e`

These are held in the `db.sqlite` database. You can retrieve these sequences with the following types of comamnds:

```bash
$ curl -s -H"Accept: application/json" "http://0.0.0.0:5000/sequence/ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF/metadata"
{"metadata":{"aliases":[{"alias":"NC_001422.1","naming_authority":"insdc"}],"ga4gh":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","id":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","length":5386,"md5":"3332ed720ac7eaa9b3655c06f6b9e196"}}

$ curl -s -H"Accept: application/json" "http://0.0.0.0:5000/sequence/3332ed720ac7eaa9b3655c06f6b9e196/metadata"
{"metadata":{"aliases":[{"alias":"NC_001422.1","naming_authority":"insdc"}],"ga4gh":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","id":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","length":5386,"md5":"3332ed720ac7eaa9b3655c06f6b9e196"}}

$ curl -s -H"Accept: application/json" "http://0.0.0.0:5000/sequence/insdc:NC_001422.1/metadata"
{"metadata":{"aliases":[{"alias":"NC_001422.1","naming_authority":"insdc"}],"ga4gh":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","id":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","length":5386,"md5":"3332ed720ac7eaa9b3655c06f6b9e196"}}
```

## Unofficial extensions to refget

The server has a number of extensions to the standard refget spec detailed below.

_You can turn on these extensions using the configuration variable `UNOFFICIAL_EXTENSIONS` and setting it to `True`._

### Requesting multiple metadata payloads

The server can provide multiple payloads of metadata through the POST endpoint `/sequence/metadata`.

```bash
$ curl -X POST -s -H"Accept: application/json" "http://0.0.0.0:5000/sequence/metadata
   -H 'Content-Type: application/json'
   -d '{"ids":["ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","insdc:NC_001422.1",bogus"]}'
{"metadata":{"ids":["id1","id2",id3"],"metadata":[{"aliases":[{"alias":"NC_001422.1","naming_authority":"insdc"}],"ga4gh":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","id":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","length":5386,"md5":"3332ed720ac7eaa9b3655c06f6b9e196"},{"aliases":[{"alias":"NC_001422.1","naming_authority":"insdc"}],"ga4gh":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","id":"ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF","length":5386,"md5":"3332ed720ac7eaa9b3655c06f6b9e196"},null]}}
```

The request is structured as follows:

```json
{
    "ids" : ["ga4gh:SQ.aKF498dAxcJAqme6QYQ7EZ07-fiw8Kw2","bogus"]
}
```

The response is structured as follows:

```json
{
    "ids" : ["ga4gh:SQ.aKF498dAxcJAqme6QYQ7EZ07-fiw8Kw2","bogus"],
    "metadata" : [
        { "aliases" : [], "ga4gh":"ga4gh:SQ.aKF498dAxcJAqme6QYQ7EZ07-fiw8Kw2", "length": 4, "md5" : "f1f8f4bf413b16ad135722aa4591043e" },
        null
    ]
}
```

Where an ID cannot be resolved, we return a null value. The order of IDs processed will be returned in the `ids` array in the JSON response.

## Customising the instance

### Injecting new configuration

The application's default configuration is held in `app/config.py`. You can provide another configuration file to override the existing values using the `REFGET_SETTINGS` environment variable.

### Special config variables

#### `SQLALCHEMY_DATABASE_URI`

Change the datbase connection settings

#### `SERVICE_INFO`

Configure the service info returned from the code. Best to just duplicate and edit as you see fit

#### `STREAMED_CHUNKING_SIZE`

Set to a value greater than 0 to enable streaming of sequences. Note doing this will result in executing substrings

#### `SQLALCHEMY_ECHO`

Set to `True` to have SQLAlchemy emit the SQL it is generating. Useful to understand what's going on under the hood. Default is `False`.

#### `ADMIN_INTERFACE`

Set to `True` to enable the internal admin interface. Currently admin has only one endpoint `/admin/stats` which reports counts of the sequences and molecules available. Default is `False`.

#### `UNOFFICIAL_EXTENSIONS`

Set to `True` to enable the unofficial extensions. Default is `True`.

### Moving to a new database

We do not recommend using SQLite in production instances. Instead you should use something like MySQL or Postgres. To do this you should:

- Create a database/schema
- Provide a new config value for `SQLALCHEMY_DATABASE_URI` pointing to the new database location & schema
  - Provide a R/O account for added security
- Run the migration scripts (we provide Alembic migrations)
- Populate with data

Alembic can be run with the following command.

```bash
REFGET_SETTINGS="path/to/new/config.py" FLASK_APP=run.py flask db upgrade
```

#### Populating a database with new records

**Make sure you have created a new database first as noted in the previous section**. Loading is available through the `loader.py` variable. You can give this a FASTA file plus additional options (use `--help` to see all options).

```bash
REFGET_SETTINGS="path/to/new/config.py" poetry run python3 loader.py --fasta FILE --authority insdc --type dna
```

The script writes only the sequence records and molecules to your active database. The script has been tested but not extensively.

## Regenerating the local SQLite compliance database

```bash
rm compliance.sqlite3
poetry run python3 create_compliance_database.py
```

This will use the local application's default settings, which is a file in the current directory called `compliance.sqlite3`.

## Creating sequence reports

Utilities are available to generate a report of the various supported checksums by refget in CSV format using the `fasta-to-report.py` tool. You can provide this a FASTA formatted file (gzipped or uncommpressed) and the code will output a CSV report. Additional command line options are available using `--help`.

```bash
$ poetry run python3 fasta-to-report.py --fasta compliance.fa.gz 
id,ga4gh,md5
I,ga4gh:SQ.lZyxiD_ByprhOUzrR1o1bq0ezO_1gkrn,6681ac2f62509cfc220d78751b8dc524
NC_001422.1,ga4gh:SQ.IIXILYBQCpHdC4qpI3sOQ_HAeAm9bmeF,3332ed720ac7eaa9b3655c06f6b9e196
VI,ga4gh:SQ.z-qJgWoacRBV77zcMgZN9E_utrdzmQsH,b7ebc601f9a7df2e1ec5863deeae88a3
```

## Running tests

```bash
$ poetry run python -m unittest tests/*.py
.........
----------------------------------------------------------------------
Ran 9 tests in 0.286s

OK
```

### Test coverage

```bash
poetry run coverage run -m unittest tests/*.py
poetry run coverage html
open htmlcov/index.html
```

## Relationship to refget-server-perl

[refget-server-perl](https://github.com/andrewyatz/refget-server-perl) was the first standalone open source reference implementation of the refget protocol and supports version 1 only. This implementation supports version 2 only. No migration path is offered between refget-server-perl and refget-server-python as their schemas and design differ slightly.  Specifically:

- Sequence storage
  - refget-server-perl allowed customisation of the sequence storage layer allowing metadata to be stored in a RDMBS and sequence held on disk, in a RDBMS or redis
  - refget-server-python stores all sequence in the RDBMS alongside metadata
- Schema
  - refget-server-perl included tables which allowed tracking of release, source species, assembly and sequence synonyms
  - refget-server-python has a much simpler model only covering sequences, instances of those sequences (called molecules), molecule type and authority

In summary this implementation does far less than the refget-server-perl implementation. To migrate data between the versions either re-run sequence loading into the new schema or migrate data as specified below.

| refget-server-perl table | refget-server-python table | Migration notes                                                                                           |
| ------------------------ | -------------------------- | --------------------------------------------------------------------------------------------------------- |
| `raw_seq`                | `raw_seq`                  | Checksum column in python is just the `sha512t24u` checksum                                               |
| `seq`                    | `seq`                      | `trunc512` is replaced by `ga4gh` and this is `sha512t24u` (see above)                                    |
| `molecule`               | `molecule`                 | `source`is now `authority` and `mol_type` is replaced with `seq_type` and no support for release tracking |
| `mol_type`               | `seq_type`                 | One to one replacement                                                                                    |
| `source`                 | `authority`                | One to one replacement                                                                                    |
| `division`               | None                       |                                                                                                           |
| `release`                | None                       |                                                                                                           |
| `synonym`                | None                       |                                                                                                           |

## Creating fly deployments

[Fly.io](https://fly.io/) is an alternative to heroku for Platform as a Service (PaaS). We deploy the [reference deployment of the Python Refget Server v2](https://refgetv2.fly.dev/) on Fly using Docker images. This is controlled by a local [fly.toml](fly.toml) which sets up a basic server and will use the [Dockerfile](Dockerfile) to build the and run the compliance server which is pre-loaded with the following sequences:

- BK006935.2 (md5:6681ac2f62509cfc220d78751b8dc524): _S.cer_ chromosome I
- BK006940.2 (md5:b7ebc601f9a7df2e1ec5863deeae88a3): _S.cer_ chromosome IV
- NC_001422.1 (md5:3332ed720ac7eaa9b3655c06f6b9e196): _Enterobacteria phage phiX174 sensu lato_

The Docker image is built to run a flask server on `0.0.0.0:8080`, which our fly.toml is configured to map external ports to.

### Making a first release

```bash
# Log into Fly
$ flyctl auth login

# Initalise
$ flyctl init

# Finally deploy the application
$ flyctl deploy
```

### Releasing an update

```bash
flyctl deploy
```

### Testing the Docker build process

To initate a local build of the Docker image you can use the following commands

```bash
docker build -t test/refgetv2 .
```

Note it is important to use the root directory context else the image will not build correctly.
