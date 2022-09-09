from multiprocessing import Pipe
from logging import info

read_channel, write_channel = Pipe(duplex=False)

def on_code_received(code: str):
    write_channel.send(str(code))
    info("code written to channel")

def get_two_factor_code() -> str:
    c = ''
    c = read_channel.recv()
    return str(c)
