from logging import log
from flask import Flask, request
import multiprocessing as mp
import time

app = Flask(__name__)
orig_mac = dict()
sub_proc = mp.Manager()


@app.route('/fake', methods=['POST'])  # Returned from fake server
def receive_hack_data() -> str:
    data = request.get_json(force=True)
    return str(data)


@app.route('/arp', methods=['GET'])
def arp() -> None:
    if sub_proc["hack"] == None:
        p = mp.Process(target=do_hack)
        sub_proc["hack"] = p
        sub_proc["hack"].start()


def do_hack() -> None:
    while True:
        set_arp("true_server", orig_mac["fake"])
        time.sleep(0.3)


@app.route('/recover', methods=['GET'])
def recover() -> None:
    if sub_proc["hack"] != None:
        sub_proc["hack"].terminate()
        sub_proc["hack"] = None


@app.route('/', methods=['GET'])
def home_page() -> None:
    # TODO: rander home page
    pass


def get_mac_addr(hostname: str) -> str:
    # TODO: get mac addr
    return hostname


def set_arp(hostname: str, mac: str) -> None:
    pass


def record_mac_addr() -> bool:
    orig_mac["true"] = get_mac_addr("true_server")
    orig_mac["fake"] = get_mac_addr("fake_server")
    print(orig_mac)
    return len(orig_mac["true"]) + len(orig_mac["fake"]) == 34


def main() -> int:
    if record_mac_addr() == False:
        return -1
    app.run(port=80)
    return 0


if __name__ == '__main__':
    main()
