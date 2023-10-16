# API Specification

## 1. User Creation

The API calls are made in this sequence when making a user account:
1. `Make User`

### 1.1. New User - `/users/` (POST)

Creates a new user account with specified information.

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
    "user_id": "string" /* This id will be used for future calls */
}
```
## 2. Group Creation

The API calls can be made when making and viewing a group:
1. `Make Group`
2. `Add User`, or
3. `Remove User`
4. `Get Members`

### 2.1. New Group - `/groups/` (POST)

Creates a new group with specified information.

**Request**:

```json
{
  "name": "string"
}
```

**Returns**:

```json
{
    "group_id": "string" /* This id will be used for future calls */
}
``` 

### 2.2. Add User to Group - `/groups/{group_id}/users/` (POST)

Adds the requested user to the specified group 

**Request**:

```json
{
  "user_id": "string"
}
```

**Returns**:

```json
{
    "success": "boolean"
}
```

### 2.3 Remove User - `/groups/{group_id}/users/{user_id}` (DELETE)

Removes the specified user from the group, failing if they are not paid up.

**Returns**:

```json
{
    "success": "boolean"
}
```

### 2.4 Get Members - `/groups/{group_id}/users/` (GET)

Lists all users in the specified group.

**Returns**:

```json
[
  {
      "name": "string",
      "user_id": "string"
  }
]
```

## 3. Purchases and Balancing

These API calls are used to post group purchases and solve outstanding balances:
1. `Post Purchase`
2. `Get Balance`
3. `Resolve Balance`

### 3.1. Post Purchase - `/groups/{group_id}/purchases/{user_id}` (POST)

Posts a purchase to a group, added the split cost to the balance between this user and all others in the group.

**Request**:

```json
{
    "price": "integer" /* price in cents */
}
```

**Returns**:

```json
{
    "success": "boolean"
}
```

### 3.2. Get Balance - `/users/{user_id1}/balances/{user_id2}` (GET)

Recieves the outstanding balance between user1 and user2, including balance from all group purchases since last resolution in all shared groups.

**Returns**:
```json
{
    "balance": "integer" /* in cents */
}
```

### 3.3. Resolve Balance - `/users/{user_id1}/balances/{user_id2}` (POST)

Adds a transaction between user1 and user2, modifying their current balance.

**Request**:

```json
{
    "amount": "integer" /* the balance change to be posted, in cents */
}
```
