"""
    Application: Generate client side configuration.
    Language: Python
    OS: any
    Author: Titas Majumder
"""

# Create ruleset
def client_ruleset_config(rule_name, server_ip, port, protocol):
    """
    Generate an rsyslog RainerScript configuration string with a ruleset and disk queue settings based on the provided parameters.

    Args:
    - server_ip (str): IP address or hostname of the rsyslog server
    - port (int): Port number to send logs to
    - protocol (str): Protocol to use ('tcp' or 'udp')

    Returns:
    - str: RainerScript configuration string
    """
    if protocol.lower() not in ['tcp', 'udp']:
        raise ValueError("Protocol must be 'tcp' or 'udp'")

    protocol_upper = protocol.upper()

    config_content = f"""# Generated rsyslog configuration file using RainerScript with ruleset and disk queue

# Define the ruleset
ruleset(name="{rule_name}") {{
    action(
        type="omfwd"
        Target="{server_ip}"
        Port="{port}"
        Protocol="{protocol_upper}"
        Template="RSYSLOG_SyslogProtocol23Format"
        QueueMode="disk"
        QueueFileName="main_queue"
        QueueSize="1g"
        Action.ResumeRetryCount="-1" # Infinite retry
    )
}}"""

    return config_content

# Create ruleset end


# Use rule

def apply_ruleset_client(log_file, tag, facility, severity, rule_name):
    """
    Generate an rsyslog RainerScript configuration string that applies a previously defined ruleset
    using the imfile module to monitor a log file.

    Args:
    - log_file (str): Path to the log file to be monitored.
    - tag (str): Tag to be associated with the log entries.
    - facility (str): Facility to be used (e.g., 'local3').
    - severity (str): Severity level to be used (e.g., 'info').
    - rule_name (str): Applicable rule to forward.

    Returns:
    - str: RainerScript configuration string that applies the ruleset with imfile module.
    """
    config_content = f"""# Monitor the log file and apply the ruleset

input(type="imfile"
      File="{log_file}"
      Tag="{tag}"
      StateFile="{tag.replace('/', '_')}_state"
      Severity="{severity}"
      Facility="{facility}"
      freshStartTail="on"
      RunFileMonitor
      ruleset="{rule_name}")
"""

    return config_content

# Use rule end 

# TLS template

def client_tls_template(cert_file, target_host, protocol, port, rule_name):
    """
    Generates an rsyslog configuration template with TLS settings.

    Args:
        cert_file (str): Path to the CA certificate file.
        target_host (str): Target host IP address or hostname.
        protocol (str): Protocol to use (e.g., 'tcp').
        port (str): Port number to use.
        rule_name (str): Name of the ruleset.

    Returns:
        str: The rsyslog configuration template.
    """
    template = f"""
# /etc/rsyslog.conf or /etc/rsyslog.d/01-tls-forward.conf

# Global configuration for TLS
global(
  DefaultNetstreamDriver="gtls"
  DefaultNetstreamDriverCAFile="{cert_file}"
)

# Define the ruleset
ruleset(name="{rule_name}") {{
  # Define the action for the ruleset
  action(
    type="omfwd"
    target="{target_host}"  # Target host IP address or hostname
    protocol="{protocol}"    # Use TCP or other protocol
    port="{port}"            # Port number on the remote server
    StreamDriver="gtls"      # Use TLS for the stream driver
    StreamDriverMode="1"     # Mode 1 enables encryption
    StreamDriverAuthMode="anon"  # Authentication mode
    QueueMode="disk"
    QueueFileName="main_queue"
    QueueSize="1g"
    Action.ResumeRetryCount="-1" # Infinite retry
  )
}}
"""

    return template.strip()

# # Example usage
# cert_file = "/etc/ssl/ca.pem"
# target_host = "192.168.x.1"
# protocol = "tcp"
# port = "514"
# rule_name = "testRule"

# config_template = client_tls_template(cert_file, target_host, protocol, port, rule_name)
# print(config_template)

