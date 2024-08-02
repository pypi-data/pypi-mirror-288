# Rsyslog Configuration Generator

This Python application generates client-side configuration for rsyslog using RainerScript. The configuration includes defining a ruleset and applying it to monitor log files.

## Overview

This application provides two main functions:

1. **`client_ruleset_config`**: Generates an rsyslog RainerScript configuration string to define a ruleset with disk queue settings.
2. **`apply_ruleset_client`**: Generates an rsyslog RainerScript configuration string to apply a previously defined ruleset to monitor a log file using the imfile module.

## Prerequisites

- Python 3.x
- Basic understanding of rsyslog and RainerScript

## Functions

### `client_ruleset_config(rule_name, server_ip, port, protocol)`

### `apply_ruleset_client(log_file, tag, facility, severity, rule_name)`

Generates a RainerScript configuration string to define a ruleset and apply the rule.

**Arguments:**

- `rule_name` (str): Name of the ruleset.
- `server_ip` (str): IP address or hostname of the rsyslog server.
- `port` (int): Port number to send logs to.
- `protocol` (str): Protocol to use ('tcp' or 'udp').
- `log_file` (str): Log file name where the rule should be applicable.
- `tag` (str): tag of the log events.
- `facility` (str): Facilities of the log events('local0' to 'local6', 'authpriv','mail' etc.).
- `severity` (str): Log criticality('info','warn','crit' etc.).

**Returns:**

- `str`: RainerScript configuration string defining the ruleset.

**Examples:**

```python
config = client_ruleset_config("myRuleset", "192.168.1.100", 514, "tcp")
print(config)
```

```python
apply = apply_ruleset_client("/var/log/message", "message_log", "local3", "info", "myRuleset")
print(apply)
```
