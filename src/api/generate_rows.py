from random_username import generate
import random
import csv
import pandas as pd

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
        res.append({"id": i, 
            "name": usernames[i],
            "email": emails[i],
            "phone": phones[i]
            })
    
    return res

def spam_groups(n, users):
    group_names = [' Roommates', ' Band', ' Friends', ' Partners in Crime', ' Travel Buddies', ' Booze Buddies', ' Grocerie Splitters']
    group_descriptions = ['We are the best Roommates', 'We are the best Band', 'We are the best Friends', 'We are the best Partners in Crime', 'We are the best Travel Buddies', 'We are the best Booze Buddies', 'We are the best Grocerie Splitters']

    groups = []
    for i in range(n):
        userindex = random.randint(0, len(users)-1)
        groupindex = random.randint(0, len(group_names)-1)

        name = users[userindex]["name"] + "'s" + group_names[groupindex]
        description = group_descriptions[groupindex]
        groups.append(
            {
                "id": i,
                "name": name,
                "description": description
            }
        )
    return groups

def spam_users_in_group(n, groups, users):

    users_per_group = n // len(groups)
    print(users_per_group)
    res = []
    group_lists = [[] for i in range(len(groups))]

    for i in range(n):
        userindex = random.randint(0, len(users)-1)
        groupindex = random.randint(0, len(groups)-1)

        res.append({
            "id": i,
            "user_id": userindex,
            "group_id": groupindex
        })
        group_lists[groupindex].append(userindex)


    return res, group_lists

def spam_transactions(n, groups, group_lists):
    
    descriptions = ['Groceries', 'Furniture', 'Airbnb', 'Thingymabob', 'Rent', 'Plumber']

    transactions = []
    print(group_lists[1000])

    for i in range(n):
        price = random.randint(10, 1000)
        description = descriptions[random.randint(0, len(descriptions)-1)]

        group_l = []
        while len(group_l) < 2:
            index = random.randint(0, len(group_lists)-1)
            group_l = group_lists[index]
        
        #find out which indices to use
        u1 = random.randint(0, len(group_l)-1)
        u2 = random.randint(0, len(group_l)-1)

        transactions.append({
            "id": i,
            "from_user": group_l[u1],
            "to_user": group_l[u2],
            "value": price 
        })

    return transactions



users = spam_users(100000)

groups = spam_groups(50000, users)

users_per_groups, group_lists = spam_users_in_group(250000, groups, users)

transactions = spam_transactions(600000, users_per_groups, group_lists)

def writecsv(filename, data):
    df = pd.DataFrame(data)
    df.to_csv(filename)

print(users[:5])
print(groups[:5])
print(users_per_groups[:5])
print(transactions[:5])

writecsv('csvs/users.csv',  users)
writecsv('csvs/groups.csv',  groups)
writecsv('csvs/users_to_group.csv',  users_per_groups)
writecsv('csvs/transactions.csv',  transactions)