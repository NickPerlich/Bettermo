Example from Lucas:
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
