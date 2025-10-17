import asyncio
import time
import os
from dotenv import load_dotenv
from config_loader import load_config
from interaction_store import prune_older_than

load_dotenv()

RUN_INTERVAL_SECONDS = 3600  # hourly

async def retention_loop():
    while True:
        # Check if auto cleanup is enabled
        auto_cleanup_enabled = os.getenv('AUTO_CLEANUP_ENABLED', 'true').lower() == 'true'
        
        if auto_cleanup_enabled:
            # Get retention days from environment or config fallback
            retention_days = int(os.getenv('RETENTION_DAYS', '30'))
            prune_seconds = retention_days * 86400
            prune_older_than(prune_seconds)
        
        await asyncio.sleep(RUN_INTERVAL_SECONDS)
