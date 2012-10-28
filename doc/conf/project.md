DbMigrations Project Configuration
==================================

Up: [DbMigrations Documentation Main][up]

Purpose
-------
DbMigrations projects often need to specify connection information (e.g. hostname, username) or other information, in order to create a database connection. Since the options required for any particular DBMS vary, DbMigrations needs some way to allow for that variety of configuration options to be passed to the migrator. To accomplish this, DbMigrations allows for arbitrary key/value pairs to be passed to the migrator.

Three different interfaces exist for specifying options for DbMigrations migrators:

 - [Command Line Arguments][commandArgs]
 - [Environment Variables][envVars]
 - [Configuration File][confFile]

Command Line Arguments
----------------------

Key/Value pairs can be passed to the migrator with the `-o KEY VALUE` flag (`o` for option).

Providing passwords through command line arguments is **strongly discouraged**, see the note about [security][security] for more information.

For example:

`dbmigrations apply -o database testDb -o user testUser -o host my.host`


`dbmigrations apply -o db testDb`

Environment Variables
---------------------

The environment may also be used to pass options to DbMigrations migrators. This method allows options to be specified globally, rather than per-run. However, since DbMigrations shares the environment with many other processes on the system, options that are intended for DbMigrations are prefixed to prevent options meant for other processes to be passed into DbMigrations.

DbMigrations will ignore all environment variables that do not begin with the environment prefix. If an environment variable does begin with the environment prefix, the key of that variable is altered so that the prefix is removed from it and then made lowercase. The modified key and value are then passed into the migrator.

By default, the prefix is "`MIG_`".

Providing passwords through environment variables is **strongly discouraged**, see the note about [security][security] for more information.

For example, using the default prefix:

`MIG_DATABASE=dbTest MIG_PASSWORD=wXyZ dbmigrations`

produces the configuration:
<table>
    <tr><th>Key</th><th>Value</th></tr>
    <tr><td><code>database</code></td><td>dbTest</td></tr>
    <tr><td><code>password</code></td><td>wXyZ</td></tr>
</table>

`DATABASE=dbTest MIG_PASSWORD=wXyZ dbmigrations`

produces the configuration:
<table>
    <tr><th>Key</th><th>Value</th></tr>
    <tr><td><code>password</code></td><td>wXyZ</td></tr>
</table>

The prefix can be changed with the command line argument `--env-prefix PREFIX`.

Configuration File
------------------

A project settings file may be provided to specify configuration options for a single migrations project. The project configuration file must be named `dbmigrations.conf`. DbMigrations will look in the  migrations base directory for such a file. If the file exists, it is used to specify options for DbMigraitons migrators.

The body of the file is simply a [JSON][json] object with keys and values for each option.

Passwords and Security
----------------------

For security reasons, providing passwords via configuration files or via command line arguments is **strongly discouraged**. However, since DbMigrations does not place any restrictions on the content or meanings of the options, DbMigrations will stupidly allow providing passwords through all three methods.

It is recommended that database passwords only be provided through environment variables.


[up]: http://zealjagannatha.com/DbMigrations/main.md "DbMigrations Documentation"
[security]: #Passwords.and.Security "Passwords and Security"
[confFile]: #Configuration.File "Configuration File"
[envVars]: #Environment.Variables "Environment Variables"
[commandArgs]: #Command.Line.Arguments "Command Line Arguments"
[json]: http://www.json.org/ "JSON"