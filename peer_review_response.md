# Schema/API Design Response
## AdamDelRio
### Accepted Resonpses
- [ ] Make ‘user-id’ in ‘users-to-group’ a foreign key.
- [ ] Make ‘group-id’ in ‘users-to-group’ a foreign key.
- [ ] Make ‘user-id’ Non-Nullable 
- [ ] Change "/" in groups.py to "/create_group"
- [ ] Change "/" in users.py to "/create_user"
- [ ] Create GET "/{id}" in group.py to get a list of users in a group
- [ ] Create DELETE "/{user_id}/{group_id}" in users.py to remove a user from a group
- [ ] Rename API Documentation in from 'Central Coast Cauldrons' to 'Better Mo'
- [ ] Update API Spec to match API (do after all changes, or as you change, so it is up to date)
### Debated/Unaccepted Responses
- [ ] Create a table for storing the balances of users between each other
- [ ] Create a unique identifier for each user and group, such as a username or group name that cannot already exist in the database

## Ivan Nghi
### Accepted Resonpses
- [ ] Change FastAPI Setup to not say 'Central Coast Cauldrons' but Bettermo
- [ ] _Add API Key_ (Will add if we have time, not the top priority)
- [ ] Make API Descriptions in Spec more specific (again do this after all other changes)
- [ ] _Update example flows to match spec_
- [ ] Could make schema in users table not accept null values, because a user with null name and etc. does not make sense.
- [ ] _Using the service, I think it would be nice to have a functionality to have a way for all of my outstanding non-zero balances shown in a get._

### Already Addressed Responses
- Removing a user from the group is not implemented like the API spec mentioned. You could implement it for that functionality.
- Some endpoints are coded but not detailed and unsure what they do. Add them to the API spec description.
- Add the other user specs into the API spec file, there is no detail on these.

### Unaccepted Responses
- _Make use of the other fields asked for in the /users endpoint, or get rid of it, makes it seem like extra unused information asked for._ While we understand this, for the completeness of the project, we are going to keep it. If we are simulating a full application, the extra fields help define the domain in which we are working.

### Debated Responses
- [ ] Also some issues when splitting between two people in a group, not sure if the intention is for it to be only split amongst the other people in he group excluding the person who initiated the transaction.
