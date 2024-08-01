import unittest
from rpa_automationanywhere.Vault import Vault

CONTROL_ROOM_URI = 'http://control-room-url.here'
USER_ID = 'domain\\username'
PASSWORD = 'password'
TEST_CREDENTIAL_NAME = 'demo'

VAULT = Vault(control_room_uri=CONTROL_ROOM_URI, username=USER_ID, password=PASSWORD)

class Test_Vault(unittest.TestCase):
    def test_get_credential(self):
        print(VAULT.get_credential(TEST_CREDENTIAL_NAME))
    
    def test_get_token(self):
        print(VAULT.get_token())
