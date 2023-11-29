## 2: Logging Group Purchase Example Flow
### Background
Bart is a 16-year-old who has to make dinner for his two brothers (Phil and Tim) and his parents (Lisa and Chris) once a week. He is a part of a group with his family where Chris is the owner. He just went to the store and got the ingredients to make a scrumptious lasagna. Fortunately, he remembered to keep the receipt and is now sitting at his kitchen counter needing to log a purchase with his family. Unfortunately, he overdrafted his bank account and is going to ask his brothers to resolve their balances, which they will need to agree to.

### User Goal
Bart wants to log a purchase with his family. 

### API Calls
Family Group Id: 3
Bart User Id: 4, Phil User Id: 5, Tim User Id: 6, Chris User Id: 2
Bart calls POST /groups/3/user/4/purchases with the total value of the receipt passed in as the body.
then Bart calls GET /users/4/balances/5 to get the Balance between him and Phil
then Bart sees that he is still in the red so he does not resolve the transaction.
then Bart calls GET /users/4/balances/6 to get the Balance between him and Tim
then Bart sees that is is likewise still in the red with Tim.
Bart is sad.
then Bat calls GET /users/4/balances/2 to get the Balance between him and Chris
and sees that there is a positive balance! He then asks to resolve the balance
then Bart calls POST users/4/balances/2 with an amount of 18.23 to resolve the balance
and Bart waits for Christ to pay.


# Testing results
1. curl -X POST --location 'http://better-mo.onrender.com/groups/3/user/4/purchases' \
--header 'Content-Type: application/json' \
--data-raw '{
    "description": "Ingredients from the store",
    "price": 65.98
}'
result: "200 OK"

2. curl -X GET --location 'http://better-mo.onrender.com/users/4/balances/5' \
--header 'Content-Type: application/json''
result: {"Balance": -3.85}

3. curl --location 'http://better-mo.onrender.com/users/4/balances/6' \
--header 'Content-Type: application/json''
result: {"Balance": -15.00}

4. curl --location 'http://better-mo.onrender.com/users/4/balances/2' \
--header 'Content-Type: application/json''
result: {"Balance": 18.23}

1. curl -X POST --location 'http://better-mo.onrender.com/users/3/balance/2' \
--header 'Content-Type: application/json' \
--data-raw '{
    "amount": 18.23
}'
result: "200 OK"


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
Jimmy calls POST /users/2/balances/1 to make an attempt to settle his debt with Jerry.


# Testing results
1. curl --location 'http://better-mo.onrender.com/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Jimmy",
    "email": "jimmy@gmail.com",
    "phone": "11111"
}'
result: {"new_user_id":10}

2. curl --location 'http://better-mo.onrender.com/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Jerry",
    "email": "jerry@gmail.com",
    "phone": "222222"
}'
result: {"new_user_id":11}


3. curl --location 'http://better-mo.onrender.com/groups'
--header 'Content-Type: application/json'
--data '{
      "name": "JimmyJerryBFFS",
       "description": "Friends 4ever <3"
   }'
result: {"new_group_id":3}

4. curl --location --request POST 'better-mo.onrender.com/groups/3/addUser/10'
result: {"id":5}

5. curl --location --request POST 'better-mo.onrender.com/groups/3/addUser/11'
result: {"id":6}

6. curl -X POST --location 'http://better-mo.onrender.com/groups/3/user/10/purchases' \
--header 'Content-Type: application/json' \
--data-raw '{
    "description": "Dinner Jimmy Jerry",
    "price": 28.00
}'
result: "200 OK"

7. curl --location 'http://better-mo.onrender.com/users/4/balances/2' \
--header 'Content-Type: application/json''
result: {"Balance": -14.00}

8. curl -X POST --location 'http://better-mo.onrender.com/users/10/balance/11' \
--header 'Content-Type: application/json' \
--data-raw '{
    "amount": 14.00
}'
result: "200 OK"


