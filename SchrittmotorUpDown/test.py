import time

i = ""
while True:
    i += "-"
    print(f"\rLaden: {i}", end="", flush=True)
    time.sleep(1)