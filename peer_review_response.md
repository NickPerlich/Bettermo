# Schema/API Design Response
## AdamDelRio
### Accepted Resonpses
- [ ] Make ‘user-id’ in ‘users-to-group’ a foreign key.
- [ ] Make ‘group-id’ in ‘users-to-group’ a foreign key.
- [ ] Make ‘user-id’ Non-Nullable 
- [ ] Change "/" in groups.py to "/create_group"
- [ ] Change "/" in users.py to "/create_user"
- [ ] Create GET "/{id}" in group.py to get a list of users in a group
- [ ] Create DELETE "/{user_id}/{group_id}" in users.py to remove a user from a group, perhaps also do this for groups.
- [ ] Rename API Documentation in from 'Central Coast Cauldrons' to 'Better Mo'
- [ ] Update API Spec to match API (do after all changes, or as you change, so it is up to date)
### Debated Responses
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

### Unaccepted Responses
- _Make use of the other fields asked for in the /users endpoint, or get rid of it, makes it seem like extra unused information asked for._ While we understand this, for the completeness of the project, we are going to keep it. If we are simulating a full application, the extra fields help define the domain in which we are working.

### Debated Responses
- [ ] _Also some issues when splitting between two people in a group, not sure if the intention is for it to be only split amongst the other people in he group excluding the person who initiated the transaction._ This is a little vague, but we should look into it, make sure it is behaving correctly.

### Already Addressed Responses
- Removing a user from the group is not implemented like the API spec mentioned. You could implement it for that functionality.
- Some endpoints are coded but not detailed and unsure what they do. Add them to the API spec description.
- Add the other user specs into the API spec file, there is no detail on these.

## Keveh Ghalambor
### Accepted Responses
- [ ] Make the description for api payloads more descriptive
- [ ] _Add default values to inputs_
- [ ] _Be more consistent with how you name variables, some are named with camelBack, while others use underscores_

### Unaccepted Responses
- _There seems to be a lot of tables that are not listed in your ER diagram_. An ER diagram is not supposed to be a 1 to 1 representation of the database. Our uploaded ER diagram should be suffiecient.
- _put descriptions for all of your endpoints to make it more readable_. Ambiguous, but also likely taken care of in previous responses.
- _add more endpoints for sanity checking, getting users, getting groups etc_. Ambiguous, but also heavily dealt with in Adam's feedback.
- _There is no way to edit rows, which would definitely be helpful_. Ambiguous, not sure how to take this. (Which table?)
- _Make an endpoint to delete a row to give you more control over your data_. The user has sufficient control over the data. Delete row's from which table? Also, an awfully powerful ability for a user to have.
- _Based on your ER Diagram, you should try to add more columns to handle the amount of data that your app needs to handle_. Confusing statement. The ER diagram is a simplified version of what is going on. The number of columns is sufficient. We might be able to elaborate on users?

### Debated Responses
- [ ] _Going to your home page reveals a row when it probably shouldn't_. Check if this is the case.

### Already Accepted Responses
 - The docs page says Central Coast Cauldrons

 ## Sebastian Thau
 ### Accepted Responses
- [ ] _For some of your endpoints you guys return a success boolean and for others an id. You may want to return both for all of them just to give more information._
- [ ] Only success booleans are returned, consider adding status codes and error messages
- [ ] Column Constraints - For columns like name, email, and phone, consider adding a max length or other constraints to ensure you are getting the data you want.
- [ ] _Table Descriptions - descriptions for tables and columns can be helpful for understanding the purpose of each component_ 
- [ ] _Update - add an endpoint to update groups or user information. This will be more RESTful_

 ### Unaccepted Responses
 - _You might want to add more columns to capture additional information. For example, you might want to include an amount column in your purchases table or additional details in the users_to_group table._ We understand this. Adding columns will add unnecessary complexity for the data we need to communicate, however. If we add more complex endpoints, we can explore this further for sure.
 - _Data Types - Use varchar instead of text if there's a maximum length for the data._ Not a bad idea, but we don't really have a maximum text length for the description at the moment. The text type is also very performant in PostGres.

 ### Already Accepted Responses
- The explanations are a bit brief for certain endpoints.
- Nullable - Consider making some columns not nullable as a user with no name, phone, or email isn't really a user.
- Add Unique Constraints - Consider adding unique constraints to fields like email in the users table to ensure that there are no duplicate email addresses.
- Delete- add an endpoint to delete groups or users. This will be more RESTful

 ### Debated Responses
 - _Possibly use singular names for your table names, so instead of groups, you might want to use group. This aligns with the convention where table names usually represent a single entity._
