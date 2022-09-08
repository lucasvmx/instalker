from threading import Lock
from multiprocessing import Pipe

read_channel, write_channel = Pipe(duplex=False)

def on_code_received(code: str):
    write_channel.send(str(code))

def get_two_factor_code() -> str:
    c = ''
    c = read_channel.recv()
    return str(c)
