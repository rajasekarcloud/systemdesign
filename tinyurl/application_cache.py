# -------------------------
# Simple in‑process application cache
# -------------------------

# Store the key in a variable
# Update the store time in another variable
# The key cached with TTL of 25 sec
# If application requests the key within 25 sec, it works - Cache Hit
# If application requests the key after 25 sec, it fails - Cache Miss
import time
import datetime
app_cache = {}          # stores key → value
cache_expiry = {}       # stores key → expiry timestamp
TTL = 25                # seconds

def set_cache(input_id,input_name):
    app_cache[input_name] = input_id
    cache_expiry[input_name] = time.time() + TTL # Setting TTL for the record currnet time + TTL
    print(app_cache,cache_expiry)

def get_cache(input_name):
    # Check if the element is within in the TTL comparing with current time
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if cache_expiry[input_name] > time.time():
        if app_cache[input_name]:
            print(f'Item -> {app_cache[input_name]},Date -> {current_time}')
        else:
            print("Not Key Exist In Cache.")
    else:
        print("TTL Expired. Item Not Found In Cache.")


input_name="Sam"
input_id=100
set_cache(input_id,input_name)
for x in range(1,50,5):
    get_cache(input_name)
    time.sleep(5)
