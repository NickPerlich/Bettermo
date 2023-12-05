# API Specification

## 1. User Creation

### 1.1. New User - `/users/create_user` (POST)

Creates a new user given a name, phone number, and email.

**Request**:

```json
{
  "name": "string",
  "email": "string",
  "phone": "string"
}
```

**Returns**:

```json
{
    "new_user_id": "string" /* This id will be used for future calls */
}
```
## 2. Group Creation

### 2.1. New Group - `/groups/create_group` (POST)

Creates a new group with specified information.

**Request**:

```json
{
  "name": "string"
  "description": "string"
}
```

**Returns**:

```json
{
    "new_group_id": "string" /* This id will be used for future calls */
}
``` 

### 2.2. Add User to Group - `/groups/{group_id}/addUser/{user_id}` (POST)

Adds user with uid user_id to group with gid group_id.

**Returns**:

```json
{
    "id": "int"
}
```

### 2.3 Remove User - `/groups/{group_id}/users/{user_id}` (DELETE)

Deletes user with uid user_id from group with gid group_id by deleting them from the users_to_group table.
**Returns**:

```json
{
    "deleted_user_id": "int",
    "name": "string",
    "email": "string",
    "phone": "string"
}
```

### 2.4 Get Members - `/groups/{group_id}` (GET)

Lists all users in the group with gid group_id.

**Returns**:

```json
[
  {
    "user_id": "int",
    "name": "string",
    "email": "string",
    "phone": "string"
  },
  ...
]
```

## 3. Purchases and Balancing

These API calls are used to post group purchases and solve outstanding balances:
1. `Post Purchase`
2. `Get Balance`
3. `Resolve Balance`

### 3.1. Post Purchase - `/{group_id}/users/{user_id}/purchases` (POST)

Posts a purchase to a group, added the split cost to the balance between this user and all others in the group.

**Request**:

```json
{
    "description": "string",
    "price": "float" /* price in dollars */
}
```

**Returns**:

```json
{
    "ok"
}
```

### 3.2. Get Balance - `/users/{user_id}/balances/{other_user_id}` (GET)

Recieves the outstanding balance between user1 and user2, including balance from all group purchases since last resolution in all shared groups.

**Returns**:
```json
{
    "balance": "integer" /* in dollars */
}
```

### 3.3. Resolve Balance - `/users/{uid1}/pay/{uid2}` (POST)

Adds a transaction between user1 and user2, modifying their current balance.

**Request**:

```json
{
    "amount": "integer", /* the balance change to be posted, in dollars */
    "description": "string"
}
```
**Returns**:

```json
{
    "Amount paid": "float"
}
```

### 3.4. Show Balance Breakdown - `/{user_id}/balance_breakdown` (GET)

Returns a table of every user to whom user_id owes money to or is owed by.

**Returns**:
```json
{
    "Balance Breakdown": [
                            {"user_id": "amount" /* amount is an int */},
                            {"user_id": "amount"},
                            {"user_id": "amount"},
                            ...
                         ]  
}
```

### 3.5. Resolve all Debts - `/{user_id}/resolve_balance` (POST)

Searches all users that user_id owns money to and resolves them.

**Returns**:

```json
{
    "All balances settled"
}
```
