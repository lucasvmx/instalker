from threading import Lock

TWO_FACTOR_AUTH = ''
mx = Lock()

def on_code_received(code: str):
    print("[INFO] Two factor auth received: {}".format(code))
    mx.acquire()
    TWO_FACTOR_AUTH = code
    mx.release()

def get_two_factor_code() -> str:
    c = ''
    mx.acquire()
    if len(TWO_FACTOR_AUTH) > 0:
        c = TWO_FACTOR_AUTH
    mx.release()
    return c
