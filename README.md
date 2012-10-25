DbMigrations
============

Usage
-----

    usage: dbmigrations [-h] {apply,create} ...
    
    optional arguments:
      -h, --help      show this help message and exit
    
    subcommands:
      {apply,create}

    usage: dbmigrations apply [-d DATABASE] [-h HOSTNAME] [-p PORT] [-U USERNAME]
                              [--help]
    
    optional arguments:
      -d DATABASE, --db DATABASE, --database DATABASE
                            Specify the database name.
      -h HOSTNAME, --host HOSTNAME, --hostname HOSTNAME
                            Specify the database hostname.
      -p PORT, --port PORT  Specify the database port.
      -U USERNAME, --user USERNAME, --username USERNAME
                            Specify the database username.
      --help                show this help message and exit

    usage: dbmigrations create [-d DATABASE] [-a] [-b BASEDIR] [--help]
    
    optional arguments:
      -d DATABASE, -db DATABASE, --database DATABASE
                            Set the database name.
      -a, --advanced        Create an advanced migration.
      -b BASEDIR, --basedir BASEDIR
                            Specify the migraitons base directory.
      --help                show this help message and exit