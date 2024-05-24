import json

def get_item_by_id(items, item_wished):
    for item in items:
        if item['id'] == item_wished:
            return item
    return None


f_users = open('tests/users.json')
f_items = open('tests/items.json')

users = json.load(f_users)
items = json.load(f_items)

# create a graph with all the users, linked together based on their wishes
users_items = {}
for item in items:
    if users_items.get(item['user_id']) is None:
        users_items[item['user_id']] = []

    # find all the users wishing to get this item
    wished_by = [user['id'] for user in users if item['id'] in user['items_wishes_id']]

    # link the owner of the item with the interested users, weighted by its value
    users_items[item['user_id']].append({'weight': item['value'], 'wished_by': wished_by})

users_graph = {}
for user in users:
    if len(user['items_wishes_id']) > 0:
        users_graph[user['id']] = []
        for item_wished_id in user['items_wishes_id']:
            item_wished = get_item_by_id(items, item_wished_id)
            users_graph[user['id']].append({
                'owner_id': item_wished['user_id'],
                'weight': item_wished['value'],
                'item_wished_id': item_wished['id']
            })

#
print(users_graph)


f_users.close()
f_items.close()