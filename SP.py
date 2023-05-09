import threading
import time
import ping3


def ping(host, interval, stop_event, num_pings):
    """
    Send ping to the given host with an infinite number of packets and interval between packets.
    """
    sent = 0
    while not stop_event.is_set():
        response_time = ping3.ping(host)
        if response_time is not None:
            print(f"{host} is reachable ({response_time:.3f} ms)")
        else:
            print(f"{host} is not reachable")
        sent += 1
        time.sleep(interval / 1000)
    num_pings.append(sent)


if __name__ == "__main__":
    host = input("Enter the IP address: ")
    interval = float(input("Enter the time interval between packets (in ms): "))
    num_threads = int(input("Enter the number of instances to run: "))

    stop_events = [threading.Event() for _ in range(num_threads)]
    num_pings = []

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=ping, args=(host, interval, stop_events[i], num_pings))
        threads.append(t)
        t.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping ping...")
        for event in stop_events:
            event.set()
        for t in threads:
            t.join()

    total_pings = sum(num_pings)
    print(f"{host} sent {total_pings} pings.")