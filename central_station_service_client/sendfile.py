import asyncio
import os.path


async def send_to_preparer(ip, port, table_file):
    reader, writer = await asyncio.open_connection(
        ip, port)

    print(f'Send: {table_file!r}')
    writer.write(table_file)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def send_to_cleaner(ip, port, table_file, key_file):
    reader, writer = await asyncio.open_connection(
        ip, port)
    writer.write(len(key_file).to_bytes(2, byteorder='big'))
    writer.write(key_file)
    await writer.drain()
    writer.write(table_file)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    input_string = ''
    while input_string != '1' and input_string != '2':
        input_string = input(f"Do you want to send to the data preparer (1) or data cleaner (2)? (1,2)")
    if input_string == '1':
        table_path = os.path.abspath(input(f"Please provide the absolute path to the table to be cleaned!"))
        f = open(table_path, 'rb')
        table_file = f.read()
        f.close()
        asyncio.run(send_to_preparer('127.0.0.1', 5555, table_file))
    if input_string == '2':
        encrypt_flags_input: str = ''
        key_path = os.path.abspath(
            input(f"Please provide the absolute path to the private key of the central service!"))
        f = open(key_path, 'rb')
        key_file = f.read()
        f.close()
        table_path = os.path.abspath(input(f"Please provide the absolute path to the table to be anonymized!"))
        f = open(table_path, 'rb')
        table_file = f.read()
        f.close()
        asyncio.run(send_to_cleaner('127.0.0.1', 5557, table_file, key_file))
