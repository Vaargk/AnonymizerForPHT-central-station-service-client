import asyncio
import os.path


async def send_to_anonymizer_and_receive(ip, port, table_file):
    reader, writer = await asyncio.open_connection(
        ip, port)

    print(f'Send: {table_file!r}')
    writer.write(table_file)
    await writer.drain()

    # data = await reader.read()
    # print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


if __name__ == '__main__':
    table_path = os.path.abspath(input(f"Please provide the absolute path to the table to be anonymized!"))
    f = open(table_path, 'rb')
    table_file = f.read()
    f.close()
    asyncio.run(send_to_anonymizer_and_receive('127.0.0.1', 5555, table_file))
