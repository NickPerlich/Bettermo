from random_username import generate
import random

def spam_users(n):
    usernames = generate.generate_username(n)
    email_terminations = ['@gmail.com', '@yahoo.com', '@example.com', '@fake.com', '@outlook.com']
    emails = []
    phones = []

    for user in usernames:
        emails.append(str(user) + email_terminations[random.randint(0,len(email_terminations)-1)])
        phones.append(random.randint(1000000000, 9999999999))

    res = []
    for i in range(n):
        res.append([usernames[i], emails[i], phones[i]])
    
    return res

def spam_groups(n, users):
    group_names = [' Roommates', ' Band', ' Friends', ' Partners in Crime', ' Travel Buddies', ' Booze Buddies', ' Grocerie Splitters']
    group_descriptions = ['We are the best Roommates', 'We are the best Band', 'We are the best Friends', 'We are the best Partners in Crime', 'We are the best Travel Buddies', 'We are the best Booze Buddies', 'We are the best Grocerie Splitters']

    groups = []
    for i in range(n):
        userindex = random.randint(0, len(users)-1)
        groupindex = random.randint(0, len(group_names)-1)

        name = users[userindex][0] + "'s" + group_names[groupindex]
        description = group_descriptions[groupindex]
        groups.append([name, description, userindex])
    return groups

def spam_users_in_group(n, groups, users):

    users_per_group = n // len(groups)
    print(users_per_group)
    res = []

    for i in range(n):
        userindex = random.randint(0, len(users)-1)
        groupindex = random.randint(0, len(groups)-1)

        res.append([userindex, groupindex])

    return res

def spam_transactions(n, users_per_groups):
    
    descriptions = ['Groceries', 'Furniture', 'Airbnb', 'Thingymabob', 'Rent', 'Plumber']

    transactions = []

    for i in range(n):
        price = random.randint(10, 1000)
        index = random.randint(0, len(users_per_groups)-1)
        description = descriptions[random.randint(0, len(descriptions)-1)]
        transactions.append(users_per_groups[index][1], users_per_groups[index][0], description, price)

    return transactions



users = spam_users(100000)

groups = spam_groups(50000, users)

users_per_groups = spam_users_in_group(250000, groups, users)

transactions = spam_transactions(600000, users_per_groups)

print()