from telethon import TelegramClient, events, sync, functions, types

api_id = 1315849
api_hash = 'e61ce3f911e5123e2cd8ec2b4e713935'

client = TelegramClient('lechatonguniverse', api_id, api_hash)
client.start()
message = client.get_messages('@lechatonguniverse', ids=3892)
#result = client(functions.channels.GetMessagesRequest(
#    channel='@lechatonguniverse',
#        id=[3892]
#    ))
print(message)
client.download_media(message=message, )
#client.download_profile_photo('me')
#client.download_file(file='t.me/lechatonguniverse/2034', input_location='D:\FFOutput')
#client(functions.upload.GetWebFileRequest(
#                location=types.InputWebFileLocation(
#                    url='https://t.me/lechatonguniverse/2034',
#                    access_hash=-12398745604826
#                ),
#                offset=42,
#                limit=100
#            ))
#print(client.get_me().stringify())

#client.send_message('me', 'Hello to myself!')