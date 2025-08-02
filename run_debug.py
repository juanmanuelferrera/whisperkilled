#!/usr/bin/env python3

import sys
import time
import signal
from yap_gui import main

def signal_handler(sig, frame):
    print(f'Signal {sig} received, exiting gracefully...', file=sys.stderr)
    sys.exit(0)

# Capture common signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print("Starting Whisper Killer debug run...", file=sys.stderr)

try:
    main()
except KeyboardInterrupt:
    print("KeyboardInterrupt received", file=sys.stderr)
except Exception as e:
    print(f"Exception in main: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()

print("Debug run completed", file=sys.stderr)