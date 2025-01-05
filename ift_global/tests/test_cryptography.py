from ift_global.utils.encryption import (
    EncryptDecrypt,
    HashingTool,
    create_ash_key,
    create_ash_salt
)
from collections import namedtuple
import pytest

@pytest.fixture
def my_salt_key():        
        MySaltKey = namedtuple(
            'MySaltKey',
            ['key',
            'salt',
            'key_another'
        ])
        return MySaltKey(
             create_ash_key(64),
             create_ash_salt(32),
             create_ash_key(64)
        )


def test_ashing_value(my_salt_key):
    hash_one = HashingTool(key = my_salt_key.key, salt=my_salt_key.salt, data='my_message')
    hash_two = HashingTool(key = my_salt_key.key, salt=my_salt_key.salt, data='my_message')
    hash_three = HashingTool(key = my_salt_key.key_another, salt=my_salt_key.salt, data='my_message')
    assert hash_one.hashed == hash_two.hashed
    assert hash_one == hash_two
    assert hash_one != hash_three

def test_encryption_decryption_value(my_salt_key):
    class_dec = EncryptDecrypt(internal_key=my_salt_key.key)
    enc_message = class_dec.encrypt('hello')
    assert 'hello' == class_dec.decrypt(enc_message)
    assert class_dec.encrypt('goodbye') != class_dec.encrypt('hello')