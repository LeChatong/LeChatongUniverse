# from django.conf import settings
# from telethon.tl.functions.messages import GetDialogsRequest
# from telethon.tl.types import InputPeerEmpty
# from telethon import TelegramClient
# from telethon.errors.rpcerrorlist import SessionPasswordNeededError
#
# # (1) Use your own values here
# api_id = 1315849
# api_hash = 'e61ce3f911e5123e2cd8ec2b4e713935'
#
#
#
# phone = '+237697548444'
# username = 'LeChatong'
#
# # (2) Create the client and connect
# client = TelegramClient(username,api_id,api_hash)
# client.connect()
#
# # Ensure you're authorized
# if not client.is_user_authorized():
#     client.send_code_request(phone)
#     try:
#         client.sign_in(phone, input('Enter the code: '))
#     except SessionPasswordNeededError:
#         client.sign_in(password=input('Password: '))
#     me = client.get_me()
#     print(me)
#
#
# get_dialogs = GetDialogsRequest(
#     offset_date=None,
#     offset_id=0,
#     offset_peer=InputPeerEmpty(),
#     limit=30,)
# dialogs = client(get_dialogs)
# print(dialogs)

from telethon.sync import TelegramClient
from telethon import functions, types


api_id = 1315849
api_hash = 'e61ce3f911e5123e2cd8ec2b4e713935'
with TelegramClient('LeChatong', api_id, api_hash) as client:
    #Info Channel
    #result = client(functions.channels.GetFullChannelRequest(
    #    channel='LeChatongUniverse'
    #))
    #Info User
    result = client(functions.help.GetUserInfoRequest(
        user_id='LeChatong'
    ))
    print(result.stringify())
