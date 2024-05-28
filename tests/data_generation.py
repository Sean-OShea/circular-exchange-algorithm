from faker import Faker
import json
import conf.global_settings as env

fake = Faker()
# use a seed to generate the same data set everytime
Faker.seed(500)

# open the files where the test data will be dumped
f_users = open(env.TESTS['users_file_name'], 'w')
f_items = open(env.TESTS['items_file_name'], 'w')

users = []
items = []


def generate_item(user_id):
    return {
        "id": fake.uuid4(),
        "user_id": user_id,
        "name": fake.random_element(['pool stick', 'toe ring', 'USB drive', 'cup', 'twister', 'purse', 'lip gloss',
                                     'white out', 'bracelet', 'outlet', 'sun glasses', 'rubber duck', 'bow',
                                     'ice cube tray', 'rubber band', 'knife', 'camera', 'shovel', 'washing machine',
                                     'house', 'wallet', 'blouse', 'fork', 'phone', 'clothes', 'desk', 'pants', 'money',
                                     'lotion', 'grid paper', 'bookmark', 'floor', 'nail file', 'shoes', 'model car',
                                     'hair tie', 'vase', 'leg warmers', 'headphones', 'shawl', 'tv', 'lace',
                                     'candy wrapper', 'greeting card', 'glasses', 'scotch tape', 'puddle', 'cork',
                                     'clay pot', 'mouse pad', 'tree', 'window', 'plastic fork', 'bottle cap', 'beef',
                                     'sand paper', 'video games', 'stop sign', 'face wash', 'sketch pad', 'eye liner',
                                     'piano', 'air freshener', 'playing card', 'tire swing', 'bottle', 'mp3 player',
                                     'truck', 'thermometer', 'twezzers', 'nail clippers', 'soap', 'credit card', 'food',
                                     'hanger', 'charger', 'glass', 'helmet', 'apple', 'monitor', 'pencil', 'toothpaste',
                                     'soy sauce packet', 'bananas', 'spoon', 'box', 'balloon', 'tooth picks',
                                     'sailboat', 'drill press', 'cookie jar', 'tissue box', 'hair brush', 'bread',
                                     'thread', 'seat belt', 'rusty nail', 'sticky note', 'controller', 'shoe lace',
                                     'fake flowers', 'chalk', 'computer', 'canvas', 'chocolate', 'flowers',
                                     'paint brush', 'car', 'towel', 'keyboard', 'glow stick', 'cinder block', 'CD',
                                     'brocolli', 'photo album', 'deodorant', 'fridge', 'bag', 'book', 'spring',
                                     'soda can', 'stockings', 'sidewalk', 'key chain', 'door', 'sofa',
                                     'packing peanuts', 'boom box', 'lamp', 'carrots', 'mirror', 'picture frame',
                                     'buckle', 'newspaper', 'remote', 'chapter book', 'flag', 'street lights', 'doll',
                                     'ipod', 'water bottle', 'milk', 'radio', 'toilet', 'checkbook', 'television',
                                     'watch', 'keys', 'sharpie', 'candle', 'blanket', 'screw', 'speakers', 'perfume',
                                     'shirt', 'pillow', 'thermostat', 'ring', 'table', 'clock', 'cat', 'magnet',
                                     'sandal', 'cell phone', 'pen', 'coasters', 'bed', 'lamp shade', 'slipper', 'socks',
                                     'mop', 'zipper', 'toothbrush', 'tomato', 'clamp', 'conditioner', 'wagon',
                                     'teddies', 'plate', 'rug', 'shampoo', 'paper', 'sponge', 'drawer', 'needle',
                                     'bowl', 'couch', 'eraser']),
        "value": fake.random_int(env.ITEMS['min_value'], env.ITEMS['max_value'], env.ITEMS['value_step'])
    }


def generate_user(items_number):
    user_id = fake.uuid4()
    for _ in range(items_number):
        items.append(generate_item(user_id))
    return {
        "id": user_id,
        "name": fake.name(),
        "items_wishes_id": []
    }

for _ in range(env.TESTS['users_to_generate']):
    users.append(generate_user(env.TESTS['items_per_user']))

for user in users:
    user['items_wishes_id'] = list(fake.random_elements([item['id']
                                                         for item in items
                                                         if item['user_id'] != user['id']]
                                                        , env.TESTS['items_wished_per_user']))

json.dump(users, f_users)
json.dump(items, f_items)
