"""DbMigrations global settings.

Modifying this file will alter all DbMigrations applied or created on this system.
"""

# DbMigrations version.
# This is used by the installer to determine the version number,
# and printed by `dbmigrations version`
VERSION = '1.0.0'

# The prefix for environment variables.
ENVIRONMENT_PREFIX = 'MIG_'

# Allows printing the configuration options on the command line.
# Disabled by default for security reasons.
# Do not enable in production environments.
PRINT_CONFIG_ENABLED = False

# Used to control the logging level for all of DbMigrations
DEFAULT_LOG_LEVEL = 'INFO'

# Used to set which database adapter is the default.
DEFAULT_ADAPTER = 'postgresql'
