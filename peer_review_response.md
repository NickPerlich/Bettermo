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
