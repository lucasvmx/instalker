from multiprocessing import Pipe
from logging import info

def setup_pipe():
    global read_channel, write_channel
    read_channel, write_channel = Pipe(duplex=False)
    info("pipe configured successfully")

def on_code_received(code: str):
    write_channel.send(str(code))
    info("code written to channel")

def get_two_factor_code() -> str:
    c = ''
    c = read_channel.recv()
    return str(c)
