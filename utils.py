import time

SLEEP_PAUSE_SECONDS = 1.0/10_000

def sleep_ms(ms):
    initial_timestamp = ms_timestamp()
    while True:
        duration = ms_timestamp() - initial_timestamp
        if duration > ms:
            break
        time.sleep(SLEEP_PAUSE_SECONDS)

def ms_timestamp():
    return round(time.monotonic() * 1000)