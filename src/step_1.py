'''

Notarization and Proof for Geo based Games

(Infineon Hackathon 2019)

(C) 2019 - Christian Baumann - baumann.at
https://www4.baumann.at

Uses the following library:
https://github.com/Infineon/BlockchainSecurity2Go-Python-Library


'''
import sys
import json
import argparse
import time
import hashlib
import json
import requests

from blocksec2go import open_pyscard, CardError
from blocksec2go import select_app, get_key_info, generate_signature

key_id = 1

print('-------------------------------------------------------------')
print('Step 1: Read Card ID and public key and send it to blockchain');
print('-------------------------------------------------------------')
print('Trying to read card ...')

for x in range(1):
  try:
    reader = open_pyscard()
    print(reader)

    (pin_active, card_id, version) = select_app(reader)
    print(pin_active)
    print('Card ID: ' + card_id.hex())
    print(version)

    (global_counter, counter, key) = get_key_info(reader, key_id)
    print('Public key: ' + key.hex())

    if (key.hex() == ''):
      print('Card not initialized yet! run blocksec2go generate_keypair')
      sys.exit()

  except Exception as e:
    print(str(e))
    print('==> PUT CARD ON READER AND TRY AGAIN')
    sys.exit()

  except KeyboardInterrupt:
    sys.exit()

  try:
    print('')
    print('SENDING DATA TO BLOCKCHAIN ...');

    url = 'https://_REMOVED_CB_/ih19/blocksec2go-receiver.php'
    payload = {'Card': card_id.hex(), 'PubKey': key.hex()}
    r = requests.post(url, data=json.dumps(payload))
    print('RESULT: ' + r.text)

  except Exception as e:
    print(str(e))
    print('==> ERROR UPLOADING')
    sys.exit()
