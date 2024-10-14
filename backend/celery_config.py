# broker and result backend settings
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
broker_connection_retry_on_startup = True
timezone = 'UTC'
enable_utc = True