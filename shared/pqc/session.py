
# shared/pqc/session.py

# Stores active PQC-derived session keys.
#
# session_id -> session_key
#
# Thisuitable for your current Dockerized demo.
# In a production distributed system, this would normally
# be replaced with shared/expiring session storage.

SESSIONS = {}
