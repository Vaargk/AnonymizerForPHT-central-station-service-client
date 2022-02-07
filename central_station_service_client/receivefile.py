import asyncio


async def send_to_anonymizer_and_receive(ip, port, file):
    reader, writer = await asyncio.open_connection(
        ip, port)

    print(f'Send: {file!r}')
    writer.write(file)
    await writer.drain()

    data = await reader.read()
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()
    f = open('received.csv', 'wb')
    f.write(data)
    f.close()


if __name__ == '__main__':
    # just for future uses
    f = bytes(1)
    input_string = ''
    while input_string != '1' and input_string != '2':
        input_string = input('Do you want to receive from data preparer (1) or data cleaner (2)? (1|2)')
    if input_string == '1':
        asyncio.run(send_to_anonymizer_and_receive('127.0.0.1', 5556, f))
    elif input_string == '2':
        asyncio.run(send_to_anonymizer_and_receive('127.0.0.1', 5558, f))
