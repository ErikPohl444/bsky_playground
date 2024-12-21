import os
from atproto import Client
from dotenv import load_dotenv


def varstate(varname):
    print(varname, locals())
    if varname in locals():
        print(locals()[varname])


def poster(text_list):
    client = Client()
    client.login(bsky_url, bsky_pwd)
    type_field = "py_type"
    type_value = "com.atproto.repo.strongRef"
    input_type = "dict"
    if len(text_list) < 1:
        raise ValueError
    if len(text_list) == 1:
        client.send_post(text_list[0])
    if len(text_list) > 1:
        post = client.send_post(text_list[0])
        root_dict = {
            "root": {
                "cid": post.cid,
                type_field: type_value,
                "uri": post.uri,
                "input_type": input_type
            }
        }
        parent_dict = {
            "parent": {
                "cid": post.cid,
                type_field: type_value,
                "uri": post.uri,
                "input_type": input_type
            }
        }
        for new_post in text_list[1:]:
            reply_ref_var = {
                "parent": parent_dict["parent"],
                "root": root_dict["root"]
            }
            new_post = client.send_post(new_post, reply_to=reply_ref_var)
            post = new_post
            parent_dict = {
                "parent": {
                    "cid": post.cid,
                    type_field: type_value,
                    "uri": post.uri,
                    "input_type": input_type
                }
            }


def threader(text):
    orig = text
    newtext = ''
    limit = 200
    result = []
    if len(text) > 200:
        limit = limit - len(" 100/100") - 1
        tot_msgs = len(text) // limit
        if len(text) % limit > 0:
            tot_msgs += 1
    msgs = 0
    while len(text) > limit:
        remainder = text[limit:]
        text = text[:limit]
        if text[len(text)-1] != ' ':
            newremainder = text[text.rfind(' '):]
            text = text[:text.rfind(' ')]
            remainder = newremainder + remainder
        msgs += 1
        print("msgs", msgs, f"{text} msg {msgs}/{tot_msgs}")
        result.append(f"{text} msg {msgs}/{tot_msgs}")
        newtext = newtext + text
        text = remainder

    if msgs > 0 and text:
        msgs += 1
        print("msgs", msgs, f"{text} msg {msgs}/{tot_msgs}")
        result.append(f"{text} msg {msgs}/{tot_msgs}")
        newtext = newtext + text
        print("equals?", len(newtext), len(orig))
    else:
        print("msg", text)
        result.append(text)
    return result


if __name__ == '__main__':

    load_dotenv()
    bsky_url = os.getenv('BSKY_URL')
    bsky_pwd = os.getenv('BSKY_PWD')
    for x in threader('this is a very long string'*20):
        print(x)
    for x in threader('this is a very long string'*1):
        print(x)
    for x in threader(''):
        print(x)
    longmsg = ("TEST MSG ONLY: This is a test of some simple functionality I wrote "
               "to split a message into units which fit within the Bluesky post limit.  "
               "It is trying to do multiple things at one time, so bear with me if it "
               "doesn't work this time!  Here are some things it is trying to do: split "
               "a long message into multiple messages with msg count indicators - this "
               "has mostly been tested, and i'm satisfied with it for now 2 post message "
               "thread as a thread including reply to.  this is untested, so what you are "
               "seeing _is_ the test.  first time use of reply_to, so fingers crossed!")
    print(len(longmsg))
    for x in threader(longmsg):
        print(x)
    # do this with a new message than the one above only
    # poster(threader(longmsg))
