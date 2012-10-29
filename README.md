DbMigrations Documentation
==========================

Purpose
-------

DbMigrations is a DBMS-independent migration system for maintaining database schemas. It maintains a linear progress of database changes and is capable of both creating and applying new migrations.

Usage
-----

DbMigrations is divided into various subcommands each implement a different feature. To obtain a list of subcommands, use `dbmigrations --help`.

### Migration Creation

To create a new migration, `dbmigrations create` can be executed. This will create the file `BASEDIR/DATABASE/DATESTAMP/up` where `BASEDIR` is the migrations base directory (specified with `-b`, default `.`), `DATABASE` is the name of the database (specified with `-d`), and `DATESTAMP` is a UTC timestamp in the [format](http://docs.oracle.com/javase/6/docs/api/java/text/SimpleDateFormat.html) `yyyyMMddHHmmss`.

To specify a specific version name for creation, `-v VERSION` can be supplied. `VERSION` is not required to be a timestamp in the format above, but when using this flag be aware of the order in which migrations are applied.

Usage:

    usage: dbmigrations create [-a] [-b BASEDIR] [-d DATABASE] [-v VERSION]
                               [--help]

    optional arguments:
      -a, --advanced        Create an advanced migration.
      -b BASEDIR, --basedir BASEDIR
                            Specify the migrations base directory.
      -d DATABASE, --db DATABASE, --database DATABASE
                            Specify the database name.
      -v VERSION, --version VERSION
                            Specify the migration version.
      --help                show this help message and exit

### Migration Application

To run migrations, `dbmigrations apply` can be executed. This will apply all migrations in the migrations base directory (specified with `-b`) with the specified database name (specified with `-o database`). It will apply each migration in Lexicographical order.

Usage:

    usage: dbmigrations apply [-o KEY VALUE] [-b BASEDIR] [-v VERSION]
                              [--env-prefix PREFIX] [-h HOST] [-d DATABASE]
                              [-p PORT] [-U USER] [--help]

    optional arguments:
      -o KEY VALUE          Specify migrator options.
      -b BASEDIR, --basedir BASEDIR
                            Specify the migrations base directory.
      -v VERSION, --version VERSION
                            Force application of a specific version.
      --env-prefix PREFIX   Specify the environment prefix.
      -h HOST               Equivalent to `-o host HOST`.
      -d DATABASE           Equivalent to `-o database DATABASE`.
      -p PORT               Equivalent to `-o port PORT`.
      -U USER               Equivalent to `-o user USER`.
      --help                show this help message and exit

Configuration
-------------
DbMigrations projects often need to specify connection information (e.g. hostname, username) or other information, in order to create a database connection. Since the options required for any particular DBMS vary, DbMigrations needs some way to allow for that variety of configuration options to be passed to the migrator. To accomplish this, DbMigrations allows for arbitrary key/value pairs to be passed to the migrator.

Three different interfaces exist for specifying options for DbMigrations migrators:

 - Command Line Arguments
 - Environment Variables
 - Configuration File

### Command Line Arguments

Key/Value pairs can be passed to the migrator with the `-o KEY VALUE` flag.

Providing passwords through command line arguments is **strongly discouraged**, see the note about [Passwords and Security](#passwords-and-security) for more information.

For example:

    $ dbmigrations print-config -o database testDb -o user testUser -o host my.host 
    Key       Value
    host      my.host
    user      testUser
    database  testDb

#### Shorthands

Since this notation can be unweildy for commonly used options, the following shorthands may be used to set common environment variables:

 - `-d DATABASE` equivalent to `-o database DATABASE`
 - `-h HOST` equivalent to `-o host HOST`
 - `-p PORT` equivalent to `-o port PORT`
 - `-U USER` equivalent to `-o user USER`

No shorthand is provided to set a password because command line arguments is an insecure of providing command line arguments. See the note about [Passwords and Security](#passwords-and-security) for more information.

### Environment Variables

The environment may also be used to pass options to DbMigrations migrators. This method allows options to be specified globally, rather than per-run. However, since DbMigrations shares the environment with many other processes on the system, options that are intended for DbMigrations are prefixed to prevent options meant for other processes to be passed into DbMigrations.

DbMigrations will ignore all environment variables that do not begin with the environment prefix. If an environment variable does begin with the environment prefix, the key of that variable is altered so that the prefix is removed from it and then made lowercase. The modified key and value are then passed into the migrator.

By default, the prefix is "`MIG_`".

For example, using the default prefix:

    $ MIG_DATABASE=dbTest MIG_PASSWORD=wXyZ dbmigrations print-config
    Key       Value
    password  wXyZ
    database  dbTest

    $ DATABASE=dbTest MIG_PASSWORD=wXyZ dbmigrations print-config
    Key       Value
    password  wXyZ

The prefix can be changed with the command line argument `--env-prefix PREFIX`.

### Configuration File

A project settings file may be provided to specify configuration options for a single migrations project. The project configuration file must be named `dbmigrations.conf`. DbMigrations will look in the  migrations base directory for such a file. If the file exists, it is used to specify options for DbMigraitons migrators.

The body of the file is simply a [JSON](http://www.json.org/) object with keys and values for each option.

Providing passwords through configuration files is **strongly discouraged**, see the note about [Passwords and Security](#passwords-and-security) for more information.

### Passwords and Security

For security reasons, providing passwords in plaintext via configuration files or command line arguments is **strongly discouraged**. However, since DbMigrations does not place any restrictions on the content or meanings of options, DbMigrations naively allows providing passwords through all three methods. It is recommended that database passwords only be provided through environment variables.

### Printing Configurations

For debugging purposes, DbMigrations provides a way to print configuration options at the command line. This can be invoked by running `dbmigrations print-config`. For security reasons, this has been disabled by default. Enabling this feature can be done by setting the `PRINT_CONFIG_ENABLED` option to `True` in settings.py.