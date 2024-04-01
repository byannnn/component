import trio
from pynng import Push0


async def main():
    count = 0

    with Push0(
        dial=f"tcp://127.0.0.1:12000", 
        block_on_dial=False,
    ) as broadcaster:
        while True:
            try:
                await broadcaster.asend(f"test_{count}".encode())
                print("sent message")
            except Exception as e:
                print("unable to send message")
                print(e)
            
            count += 1


if __name__ == "__main__":
    trio.run(main)
