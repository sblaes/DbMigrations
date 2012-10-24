DbMigrations
============

Usage
-----

    Usage: dbmigration.py [action] [options]
    
    Options:
      Actions:
        Exactly one action must be provided.
        
        -c, --create        Create a migration.
        -a, --apply         Apply migrations.
        -w CONFIG_FILE, --write-config=CONFIG_FILE
                            Write configuration options to file and exit.
        --help              Show this help message and exit.
        
      Connection Options:
        These options can be specified from a configuration file. Command line
        options override configuration files.
        
        -h HOSTNAME, --host=HOSTNAME, --hostname=HOSTNAME
                            Specify the database hostname. Default localhost.
        -p PORT, --port=PORT
                            Specify the database port. Default 5432.
        -U USER, --user=USER
                            Specify the database user. Required.
        -d DATABASE, --db=DATABASE, --database=DATABASE
                            Specify the database name. Required.
                            
      Other Options:
        -b BASEDIR, --basedir=BASEDIR
                            Specify the migration base directory. The migrator
                            will look here for the connection config file.