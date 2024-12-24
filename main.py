import os
import random

from atproto import Client
from dotenv import load_dotenv
from setup_logging import logger


def poster(text_list):
    retlist = []
    client = Client()
    client.login(bsky_url, bsky_pwd)
    type_field = "py_type"
    type_value = "com.atproto.repo.strongRef"
    input_type = "dict"
    if len(text_list) < 1:
        raise ValueError
    if len(text_list) == 1:
        return [client.send_post(text_list[0])]
    if len(text_list) > 1:
        post = client.send_post(text_list[0])
        retlist.append(post)
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
    return retlist


def treer():
    decorations = [
        'tinsel', 'candle', 'apple', 'finial', 'snowflake', 'icicle'
    ]
    client = Client()
    client.login(bsky_url, bsky_pwd)
    type_field = "py_type"
    type_value = "com.atproto.repo.strongRef"
    input_type = "dict"
    root_post = client.send_post(
        "My present to the Bsky community is a script-generated perfect binary tree of 4 levels-- with ornaments!"
    )
    parents = [root_post]
    root_dict = {
        "root": {
            "cid": root_post.cid,
            type_field: type_value,
            "uri": root_post.uri,
            "input_type": input_type
        }
    }
    # create parent, add to parents, set root = this post
    level = 2
    while level <= 4:
        newparents = []
        for parent in parents:
            parent_dict = {
                'parent': {
                    "cid": parent.cid,
                    type_field: type_value,
                    "uri": parent.uri,
                    "input_type": input_type
                }
            }
            reply_ref_var = {
                "parent": parent_dict["parent"],
                "root": root_dict["root"]
            }
            new_post = random.choice(decorations)
            newparent = client.send_post(new_post, reply_to=reply_ref_var)
            newparents.append(newparent)
            newparent = client.send_post(new_post, reply_to=reply_ref_var)
            newparents.append(newparent)
        parents = newparents
        level += 1
    return True


def threader(text):
    orig = text
    newtext = ''
    message_character_limit = 300
    result = []
    if len(text) > 300 or text.count('\n') > 0:
        message_character_limit = message_character_limit - len(" 100/100") - 1
        total_messages = 0
        if text.count('\n') > 0:
            subtexts = text.split('\n')
        else:
            subtexts = [text]
        for subtext in subtexts:
            total_messages += len(subtext) // message_character_limit
            if len(text) % message_character_limit > 0:
                total_messages += 1
    msgs = 0
    while len(text) > message_character_limit or '\n' in text:
        remainder = text[message_character_limit:]
        text = text[:message_character_limit]
        if '\n' in text:
            text, newremainder = text.split('\n', 1)
            remainder = newremainder + remainder
        elif text[len(text)-1] != ' ':
            newremainder = text[text.rfind(' '):]
            text = text[:text.rfind(' ')]
            remainder = newremainder + remainder
        msgs += 1
        logger.info(f"msgs: {msgs}, {text} msg {msgs}/{total_messages}")
        result.append(f"{text} msg {msgs}/{total_messages}")
        text = remainder

    if msgs > 0 and text:
        msgs += 1
        logger.info(f"msgs: {msgs} {text} msg {msgs}/{total_messages}")
        result.append(f"{text} msg {msgs}/{total_messages}")
        newtext = newtext + text
        logger.info(f"equals? {len(newtext)} and {len(orig)}")
    else:
        logger.info(f"msg {text}")
        result.append(text)
    return result


if __name__ == '__main__':

    load_dotenv()
    bsky_url = os.getenv('BSKY_URL')
    bsky_pwd = os.getenv('BSKY_PWD')
    '''
    for x in threader('this is a very long string'*20):
        print(x)
    for x in threader('this is a very long string'*1):
        print(x)
    for x in threader(''):
        print(x)
    longmsg = (
        "TEST MSG ONLY: What I'm testing out now is a forced split \n1. imagine you "
        "want to write several points, but you don't want a post to contain each "
        "distinct point"
        "\n2. this helps in post clarity\n3. allowing a splitter routine to split "
        "by post length and a forced split would permit greater control "
        "over how your posts are presented when they are dropped into Bluesky, even "
        "if some of the force splits are actually longer than the Bluesky post limit.")
    print(len(longmsg))
    for x in threader(longmsg):
        print(f"{len(x)}: {x}")
    # do this with a new message than any previously posted message
    # poster(threader(longmsg))
    '''
    treer()
