# Our Example Flows
## 1: Create Group Example Flow
### Background
Jacob is the dungeon master for a DnD group with his friends. He expects to purchase equipment to improve the experience for his friends, and his friends agree they will pay him back. Jacob wants to make a group with our service to log his purchases.

### User Goal
Jacob initiates the process of creating a group with our service.

### API Calls
Starts by calling POST /users/create_user with his name to get a new user with ID 420.
then Jacob calls POST /groups/create_group with a group name to get a new group with ID 5005.
then Jacob asks all his friends to create accounts. They each call POST /users/create_user to get new users with IDs 421, 422, and 423.
then Jacob calls POST /groups/420/users/{user_id} for the following user ids: 420, 421, 422, 423.
Now, Jacob can use this group with our service to post purchases as required.

## 2: Logging Group Purchase Example Flow
### Background
Bart is a 16-year-old who has to make dinner for his two brothers (Phil and Tim) and his parents (Lisa and Chris) once a week. He is a part of a group with his family where Chris is the owner. He just went to the store and got the ingredients to make a scrumptious lasagna. Fortunately, he remembered to keep the receipt and is now sitting at his kitchen counter needing to log a purchase with his family. Unfortunately, he overdrafted his account and is going to ask his brothers to resolve their balances, which they will need to agree to.

### User Goal
Bart wants to log a purchase with his family. 

### API Calls
Family Group Id: 3
Bart User Id: 4, Phil User Id: 5, Tim User Id: 6
Bart calls POST /groups/3/user/4/purchases with the total value of the receipt passed in as the body.
then Bart calls GET /users/4/balances/5 to get the Balance between him and Phil
then Bart sees that he is still in the red so he does not resolve the transaction.
then Bart calls GET /users/4/balances/6 to get the Balance between him and Tim
then Bart sees that is is likewise still in the red with Tim.
Bart is sad.

## 3: Resolving Balance Example Flow
### Background
Jimmy and Jerry are roommates and Jimmy wants to pay back Jerry for dinner. Thus, Jimmy attempts to settle his debt with Jerry so that when Jerry checks who has attempted to settle debt he can accept or decline the settlement. 
### User Goal
Jimmy wants to attempt to settle his debt to Jerry. 

### API Calls
Roommate Group Id: 4
Jimmy User Id: 1, Jerry User Id: 2
Jimmy calls GET /users/2/balances/1 to get the Balance between him and Jerry.
Jimmy pays Jerry on Venmo (sponsor us please).
Jimmy calls POST /users/1/pay/2 to make an attempt to settle his debt with Jerry.
