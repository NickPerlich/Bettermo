# Initil Profiling
## /users endpoints

### PUT /{user_id}/update_user
Run 1: 0.427 ms

Run 2: 0.479 ms

Run 3: 0.479 ms

Avg: __0.461__ ms


### POST /create_user
Run 1: 0.491 ms

Run 2: 0.505 ms

Run 3: 0.502 ms

Avg: __0.499__ ms


### GET /users/{user_id}/balances/{other_user_id}
Run 1: 113.153 ms

Run 2: 110.575 ms

Run 3: 111.299 ms

Avg: __111.676__ ms


### POST /users/{user_id}/pay/{other_user_id}
Run 1: 1.728 ms

Run 2: 1.810 ms

Run 3: 1.713 ms

Avg: __1.75__ ms


### GET /users/{user_id}/balance_breakdown
Run 1: 108.793 ms

Run 2: 111.263 ms

Run 3: 112.493 ms

Avg: __110.849__ ms


## /groups endpoints

### PUT /groups/{group_id}/update_group
Run 1: 0.432 ms

Run 2: 0.439 ms

Run 3: 0.549 ms

Avg: __0.473__ ms


### POST /groups/create_group
Run 1: 0.619 ms

Run 2: 0.565 ms

Run 3: 0.566 ms

Avg: __0.583__ ms


### GET /groups/{group_id}
Run 1: 25.062 ms

Run 2: 25.294 ms

Run 3: 24.819 ms

Avg: __25.058__ ms


### DELETE /groups/{group_id}/users/{user_id}
Run 1: 30.274 ms

Run 2: 26.538 ms

Run 3: 25.095 ms

Avg: __27.302__ ms


### POST /groups/{group_id}/users/{user_id}
Run 1: 1.860 ms

Run 2: 1.741 ms

Run 3: 1.932 ms

Avg: __1.844__ ms


### POST /groups/{group_id}/users/{user_id}/purchases
Run 1: 1.597 ms

Run 2: 1.566 ms

Run 3: 1.533 ms

Avg: __1.565__ ms

