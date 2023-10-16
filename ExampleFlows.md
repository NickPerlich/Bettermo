# Example from Lucas:
## Potion Site Customer Purchasing Example Flow
### Background
Alice the Oathbreaker Paladin comes to our potion shop because she is in desperate need of both a red healing potion and a blue mana potion after her battle with a powerful dragon. First, Alice requests a catalog to see the latest offerings available at the shop by calling GET /catalog. Alice sees in the catalog that there are 8 red potions available with SKU "RED_POTION" at a reasonable price of 50 gold. There are also 6 blue potions available with SKU "BLUE_POTION" at a price of 55 gold each.

### User Goal
Alice then initiates a purchase of 3 of the red potions and 1 of the blue potions. To do so she:

### API Calls
starts by calling POST /carts to get a new cart with ID 9001.
then Alice calls POST /carts/9001/items/RED_POTION and passes in a quantity of 3.
she makes another call to POST /carts/9001/items/BLUE_POTION and passes in a quantity of 1.
finally, she calls POST /carts/9001/checkout to finish her checkout. The checkout charges her 205 gold and gives her 3 red potions and 1 blue potion.
Alice drinks her potions and is ready to go off on a new adventure.

# Our Example Flows
## 1: Create Group Example Flow
### Background
Jacob is the dungeon master for a DnD group with his friends. He expects to purchase equipment to improve the experience for his friends, and his friends agree they will pay him back. Jacob wants to make a group with our service to log his purchases.

### User Goal
Jacob initiates the process of creating a group with our service.

### API Calls
Starts by calling POST /users with his name to get a new user with ID 420.
then Jacob calls POST /groups with a group name to get a new group with ID 5005.
then Jacob asks all his friends to create accounts. They each call POST /users to get new users with IDs 421, 422, and 423.
then Jacob calls POST /groups/420/users/{user_id} for the following user ids: 420, 421, 422, 423.
Now, Jacob can use this group with our service to post purchases as required.

## 2: Logging Group Purchase Example Flow
### Background

### User Goal


### API Calls

## 3: Resolving Balance Example Flow
### Background

### User Goal


### API Calls
