DbMigrations Documentation
==========================

Contents:

Purpose
-------

DbMigrations is a DBMS-independent migration system for maintaining database schemas. It maintains a linear progress of database changes and is capable of both creating and applying new migrations.

Subcommands
--------------

DbMigrations is divided into various subcommands each implement a different feature. To obtain a list of subcommands, use `dbmigrations --help`.

### Migration Creation

To create a new migration, `dbmigrations create` can be executed. This will create the file `BASEDIR/DATABASE/DATESTAMP/up` where `BASEDIR` is the migrations base directory (specified with `-b`), `DATABASE` is the name of the database (specified with `-d`), and `DATESTAMP` is a UTC timestamp in the format `yyyyMMddHHmmss` (formed by the python date format `%Y%m%d%H%M%S`).

To specify a specific version name for creation, `-v VERSION` can be supplied. `VERSION` is not required to be a timestamp in the format above, but when using this flag be aware of the [order][application] in which migrations are applied.

Usage:

    usage: dbmigrations create [-d DATABASE] [-a] [-b BASEDIR] [-v VERSION] [--help]

    optional arguments:
      -d DATABASE, -db DATABASE, --database DATABASE
                            Set the database name.
      -a, --advanced        Create an advanced migration.
      -b BASEDIR, --basedir BASEDIR
                            Specify the migrations base directory.
      -v VERSION, --version VERSION
                            Specify the migration version.
      --help                show this help message and exit

### Migration Application

To run migrations, `dbmigrations apply` can be executed. This will apply all migrations in the migrations base directory (specified with `-b`) with the specified database name (specified with `-o database`). It will apply each migration in [Lexicographical order][lexical].

Usage:

    usage: dbmigrations apply [-o KEY VALUE] [-b BASEDIR] [-v VERSION]
                              [--env-prefix PREFIX] [--help]
                              
    optional arguments:
      -o KEY VALUE          Specify migrator options.
      -b BASEDIR, --basedir BASEDIR
                            Specify the migrations base directory.
      -v VERSION, --version VERSION
                            Force application of a specific version.
      --env-prefix PREFIX   Specify the environment prefix.
      --help                show this help message and exit

[application]: #Migration.Application "Migration Application"
[lexical]: http://en.wikipedia.org/wiki/Lexicographical_order "Lecicographical order"