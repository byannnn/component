import argparse
from collections import deque

import trio
from pynng import Pull0
from pynng import Push0
from setproctitle import setproctitle


class Component:
    def __init__(
        self,
        name: str,
        listen,
        broadcasts,
        logger=None,
        sleep: float = 0.005,
    ):
        """
        name: name of component, will determine process and thread names too, best be unique
        listens: list of socket urls to listen to, stored inside self.listeners
        broadcasts: list of socket urls to broadcast to, stored inside self.broadcasters
        logger: re-use pre-defined logger, else create own
        sleep: sleep duration for async operations
        """

        self.name = name

        # listener
        try:
            self.listener = Pull0(
                listen=listen,
            )
        except Exception as e:
            print("cannot spawn listener")
            print(e)

        # broadcasters
        self.broadcasters = []
        for b in broadcasts:
            try:
                push = Push0(
                    dial=b,
                    block_on_dial=False,
                )
                self.broadcasters.append(push)
            except Exception as e:
                print("cannot spawn broadcaster")
                print(e)

        # others (optional params)
        self.logger = logger
        self.sleep = sleep

        # static built-ins, do not touch
        self.queue = deque(maxlen=30)
        self.go = True

    async def run(self):
        async with trio.open_nursery() as n:
            n.start_soon(self._receive)
            n.start_soon(self._handle)

    async def stop(self):
        self.go = False

    async def start(self):
        self.go = True

    async def _receive(self):
        while self.go:
            try:
                msg = await self.listener.arecv_msg()

                self.queue.append(msg)

                print("message enqueued")
            except Exception as e:
                print("unable to receive message")
                print(e)

            await trio.sleep(self.sleep)

    async def _handle(self):
        while self.go or len(self.queue) > 0:
            try:
                msg = self.queue.popleft()
                await self.handle(msg)
            except:
                pass

            await trio.sleep(self.sleep)

    async def publish(self, msg):
        for b in self.broadcasters:
            await b.asend(msg)

    async def handle(self, message):
        return message


async def main(name: str, listen: str, broadcasts: list):
    component = Component(
        name=name,
        listen=listen,
        broadcasts=broadcasts,
    )
    await component.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=name)
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name of the component",
    )
    parser.add_argument(
        "--listen",
        type=str,
        required=True,
        help="Listen address and port",
    )
    parser.add_argument(
        "--broadcasts",
        nargs="*",
        required=False,
        help="Broadcast addresses and ports",
    )
    args = parser.parse_args()

    # set process name
    setproctitle(args.name)

    trio.run(
        async_fn=main,
        args=[args.name, args.listen, args.broadcasts],
    )
