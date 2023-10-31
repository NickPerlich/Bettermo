# Example workflow
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


# Testing results
1. curl --location 'http://localhost:3000/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "jacob",
    "email": "dndmasters@gmail.com",
    "phone": "1234"
}'
result: {"new_user_id":7}
2. curl --location 'http://localhost:3000/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Nick",
    "email": "doxme@gmail.com",
    "phone": "1234"
}'
result: {"new_user_id":8}
3. curl --location 'http://localhost:3000/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Jannet",
    "email": "PlanetJannet@gmail.com",
    "phone": "4321"
}'
result: {"new_user_id":9}
4. curl --location 'http://localhost:3000/groups' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Dunjons and Dwagons",
    "description": "Meets on Wednesdays"
}'
result: {"new_group_id":2}
5. curl --location --request POST 'http://localhost:3000/groups/2/addUser/7'
result: {"id":2}
6. curl --location --request POST 'http://localhost:3000/groups/2/addUser/8'
result: {"id":3}
7. curl --location --request POST 'http://localhost:3000/groups/2/addUser/9'
result: {"id":4}