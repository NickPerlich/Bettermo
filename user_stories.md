## User Stories:

1. As a financially conscious college student, I want to be able to ensure that my roommates will be aware of how much they owe me when I grab groceries for them so that I have an accurate representation of how much money I own in my bank account.
2. As a parent with 4 kids, I want my kids to learn financial responsibility. Having the ability for my kids to offer money to each other in exchange for things between each other could teach them the value of money, services, and things (like toys). (I don't actually condone this behavior)
3. As a partner in a 3-person raid team, I want to keep track of when I buy potions for the team so that I can easily be repaid.
4. As a manager of a McDonald's, I want my employees to document business expenses like private jets so that I can have more tax write-offs.
5. As a 112-year-old airbender, I want to keep track of my usage of the 7 chakras so that I can be sure I have no earthly attachments.
6. As a person with roommates, sometimes I will buy something for the room. I want to be able to easily notify my roommates exactly how much they owe me.
7. As a user, I want to be able to view and settle my outstanding balances with my group members to ensure that I don't owe anyone anything.
8. As a group admin or a group member, I want the ability to manage group settings and invite new members to the group.
9. As a party thrower, I enjoy keeping track of who attended, and, even if we don't clear the debt immediately (someone else might be taking on the expense next time), we can clear the debt at the end of the quarter.
10. As a lazy person, I like to click a single button and have all my debts cleared, and not have to worry about the exact amount or arguing on iMessage with three different people over $2.34.
11. As a bad boyfriend, I like to keep track of how much half of the dates cost and request the exact amount the moment she breaks up with me.


## Exceptions:

1. Accidental Money Transfer: If a user accidentally types in an extra 0 into a money charge, the user can go and edit the most recent charge to fix the charge that was given to the group.
2. Unnecessary transactions: If two users owe each other money, there is no need for them both to send money to the other. The service will determine which of the two owes the other money, and how much they owe after deducting the proper balances.
3. An exception can be raised when there is an issue with creating a new expense, such as missing information or a failure to update balances.
4. An exception can be raised when a user attempts to access a group that doesn't exist or that they are not a member of.
5. Incomplete account: If a user attempts to create an account without wanting to share information such as email, phone-number, etc., there may be an issue. We should allow partial accounts that have a bare minimum needed to identify them, and allow limited use with such accounts, depending on what information is missing. This will allow parts of the application's functionality to be used without a full account.
6. No account: If a non-user wishes to view a user's account or expenses without creating an account themselves, we have no way of knowing whether there may be a bad actor. We should allow group owners to set the visibility of groups to either public or private, so that users without accounts can still view public groups without exposing private groups.
7. Debt clearing: If a user tries to clear their debt, they should be forced to get verification from the person they owe.
8. Error in bookkeeping: the math that converts debt from A to B and from B to C into debt from A to C could be erroneous.
9. Error in a transaction: if the app were to be linked to Paypal or a similar service, the app could remove the debt and then the payment fail.
10. No debt forgiveness: there could be a mistaken debt or debt cleared with cash in person, but the app won't let it be cleared without a payment through it.
