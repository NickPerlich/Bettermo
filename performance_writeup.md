# Performance Writeup

## 1. Fake Data Modeling

1. We decided to generate rows in the following proportions:

   users = 1                 => 100,000
   
   group = 0.5               =>  50,000
   
   users_in_groups = 2.5     => 250,000
   
   transactions = 6          => 600,000
   
   TOTAL                      1,000,000
   
This means that there will be half as many groups as users, meaning that each user will be in 2.5 groups on average. Each group will have 5 users, and each user will have paid someone 6 times on average.

We expect our service to scale in this way, because after a group is formed, we expect users to be paying others that are in at least one group with them. Also, we make more transactions than users or groups, because we expect a group to be used many times.

Link of the Python script used to generate the data:
src/api/generate_rows.py 







## 2. Performance of each Endpoint

# Initial Profiling
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



# Three Slowest Queries

## GET /users/{user_id}/balances/{other_user_id} - __111.676__ ms

First Run:
| QUERY PLAN                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nested Loop  (cost=21412.53..21412.59 rows=1 width=32) (actual time=112.679..112.823 rows=1 loops=1)                                                |
|   ->  Aggregate  (cost=10706.27..10706.28 rows=1 width=32) (actual time=62.188..62.290 rows=1 loops=1)                                              |
|         ->  Gather  (cost=1000.00..10706.26 rows=1 width=5) (actual time=62.183..62.284 rows=0 loops=1)                                             |
|               Workers Planned: 1                                                                                                                    |
|               Workers Launched: 0                                                                                                                   |
|               ->  Parallel Seq Scan on transactions  (cost=0.00..9706.16 rows=1 width=5) (actual time=61.898..61.899 rows=0 loops=1)                |
|                     Filter: ((to_user = 7) AND (from_user = 8))                                                                                     |
|                     Rows Removed by Filter: 600005                                                                                                  |
|   ->  Aggregate  (cost=10706.27..10706.28 rows=1 width=32) (actual time=50.484..50.525 rows=1 loops=1)                                              |
|         ->  Gather  (cost=1000.00..10706.26 rows=1 width=5) (actual time=50.467..50.510 rows=1 loops=1)                                             |
|               Workers Planned: 1                                                                                                                    |
|               Workers Launched: 0                                                                                                                   |
|               ->  Parallel Seq Scan on transactions transactions_1  (cost=0.00..9706.16 rows=1 width=5) (actual time=50.210..50.212 rows=1 loops=1) |
|                     Filter: ((from_user = 7) AND (to_user = 8))                                                                                     |
|                     Rows Removed by Filter: 600004                                                                                                  |
| Planning Time: 0.563 ms                                                                                                                             |
| Execution Time: 112.928 ms                                                                                                                          |

This is about what I expected. at every stage where we need to select, we are filtering based on both users, so if both from_user and to_user in the transactions table are indexed, the speed should dramatically increase.

```CREATE INDEX idx_from_user ON public.transactions (from_user);

CREATE INDEX idx_to_user ON public.transactions (to_user);```

| QUERY PLAN                                                                                                                              |
| --------------------------------------------------------------------------------------------------------------------------------------- |
| Nested Loop  (cost=9.11..9.16 rows=1 width=32) (actual time=0.145..0.146 rows=1 loops=1)                                                |
|   ->  Aggregate  (cost=4.56..4.57 rows=1 width=32) (actual time=0.078..0.078 rows=1 loops=1)                                            |
|         ->  Bitmap Heap Scan on transactions  (cost=3.44..4.55 rows=1 width=5) (actual time=0.074..0.075 rows=0 loops=1)                |
|               Recheck Cond: ((to_user = 7) AND (from_user = 8))                                                                         |
|               ->  BitmapAnd  (cost=3.44..3.44 rows=1 width=0) (actual time=0.072..0.073 rows=0 loops=1)                                 |
|                     ->  Bitmap Index Scan on idx_to_user  (cost=0.00..1.59 rows=9 width=0) (actual time=0.047..0.047 rows=3 loops=1)    |
|                           Index Cond: (to_user = 7)                                                                                     |
|                     ->  Bitmap Index Scan on idx_from_user  (cost=0.00..1.59 rows=9 width=0) (actual time=0.024..0.024 rows=5 loops=1)  |
|                           Index Cond: (from_user = 8)                                                                                   |
|   ->  Aggregate  (cost=4.56..4.57 rows=1 width=32) (actual time=0.062..0.063 rows=1 loops=1)                                            |
|         ->  Bitmap Heap Scan on transactions transactions_1  (cost=3.44..4.55 rows=1 width=5) (actual time=0.056..0.057 rows=1 loops=1) |
|               Recheck Cond: ((to_user = 8) AND (from_user = 7))                                                                         |
|               Heap Blocks: exact=1                                                                                                      |
|               ->  BitmapAnd  (cost=3.44..3.44 rows=1 width=0) (actual time=0.005..0.005 rows=0 loops=1)                                 |
|                     ->  Bitmap Index Scan on idx_to_user  (cost=0.00..1.59 rows=9 width=0) (actual time=0.003..0.003 rows=8 loops=1)    |
|                           Index Cond: (to_user = 8)                                                                                     |
|                     ->  Bitmap Index Scan on idx_from_user  (cost=0.00..1.59 rows=9 width=0) (actual time=0.001..0.001 rows=1 loops=1)  |
|                           Index Cond: (from_user = 7)                                                                                   |
| Planning Time: 0.843 ms                                                                                                                 |
| Execution Time: 0.347 ms                                                                                                                |

Now we see the index conditions being used instead of filtering and the execution time was __0.347ms__!! Great success.



## GET /users/{user_id}/balance_breakdown - __110.849__ ms

First Run:
| QUERY PLAN                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------- |
| Nested Loop  (cost=3.65..6.99 rows=1 width=54) (actual time=0.202..0.204 rows=1 loops=1)                                        |
|   ->  Bitmap Heap Scan on users_to_group  (cost=3.36..4.47 rows=1 width=4) (actual time=0.112..0.113 rows=1 loops=1)            |
|         Recheck Cond: ((user_id = 33881) AND (group_id = 1))                                                                    |
|         Heap Blocks: exact=1                                                                                                    |
|         ->  BitmapAnd  (cost=3.36..3.36 rows=1 width=0) (actual time=0.067..0.068 rows=0 loops=1)                               |
|               ->  Bitmap Index Scan on idx_user_id  (cost=0.00..1.54 rows=3 width=0) (actual time=0.026..0.027 rows=2 loops=1)  |
|                     Index Cond: (user_id = 33881)                                                                               |
|               ->  Bitmap Index Scan on idx_group_id  (cost=0.00..1.56 rows=6 width=0) (actual time=0.039..0.039 rows=5 loops=1) |
|                     Index Cond: (group_id = 1)                                                                                  |
|   ->  Index Scan using users_pkey on users  (cost=0.29..2.51 rows=1 width=54) (actual time=0.087..0.088 rows=1 loops=1)         |
|         Index Cond: (id = 33881)                                                                                                |
| Planning Time: 0.770 ms                                                                                                         |
| Execution Time: 0.379 ms                                                                                                        |


Now look at that, because we added the indeces due to the previous endpoint, our efficiency issues with this query are now fixed as well! How great. There aren't any other index based solutions that I would suggest for this, so I figure I can leave this here. Especially since the only table referenced for this query is the users_to_group table. Onto the next. 

## DELETE /groups/{group_id}/users/{user_id} - __27.302__ ms

First Run:
| QUERY PLAN                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------- |
| Nested Loop  (cost=1000.29..4560.50 rows=1 width=54) (actual time=13.528..24.679 rows=1 loops=1)                                 |
|   ->  Gather  (cost=1000.00..4557.98 rows=1 width=4) (actual time=13.406..24.555 rows=1 loops=1)                                 |
|         Workers Planned: 1                                                                                                       |
|         Workers Launched: 0                                                                                                      |
|         ->  Parallel Seq Scan on users_to_group  (cost=0.00..3557.88 rows=1 width=4) (actual time=13.112..24.163 rows=1 loops=1) |
|               Filter: ((user_id = 33881) AND (group_id = 1))                                                                     |
|               Rows Removed by Filter: 249999                                                                                     |
|   ->  Index Scan using users_pkey on users  (cost=0.29..2.51 rows=1 width=54) (actual time=0.116..0.118 rows=1 loops=1)          |
|         Index Cond: (id = 33881)                                                                                                 |
| Planning Time: 0.676 ms                                                                                                          |
| Execution Time: 24.818 ms                                                                                                        |

On the first part of the query plan, we run a filter when we could be indexing into the table instead, however what is interesting is that there is an index condition for the second half of the query, which could have been genereted while grabbing the first part, though I am not positive.

The logical solution to the would be to add indeces for the user_id and group_id in the users_to_group table


```CREATE INDEX idx_user_id ON public.users_to_group (user_id);
CREATE INDEX idx_group_id ON public.users_to_group (group_id);```


| QUERY PLAN                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------- |
| Nested Loop  (cost=3.65..6.99 rows=1 width=54) (actual time=0.181..0.183 rows=1 loops=1)                                        |
|   ->  Bitmap Heap Scan on users_to_group  (cost=3.36..4.47 rows=1 width=4) (actual time=0.094..0.095 rows=1 loops=1)            |
|         Recheck Cond: ((user_id = 33881) AND (group_id = 1))                                                                    |
|         Heap Blocks: exact=1                                                                                                    |
|         ->  BitmapAnd  (cost=3.36..3.36 rows=1 width=0) (actual time=0.053..0.053 rows=0 loops=1)                               |
|               ->  Bitmap Index Scan on idx_user_id  (cost=0.00..1.54 rows=3 width=0) (actual time=0.031..0.031 rows=2 loops=1)  |
|                     Index Cond: (user_id = 33881)                                                                               |
|               ->  Bitmap Index Scan on idx_group_id  (cost=0.00..1.56 rows=6 width=0) (actual time=0.020..0.020 rows=5 loops=1) |
|                     Index Cond: (group_id = 1)                                                                                  |
|   ->  Index Scan using users_pkey on users  (cost=0.29..2.51 rows=1 width=54) (actual time=0.084..0.085 rows=1 loops=1)         |
|         Index Cond: (id = 33881)                                                                                                |
| Planning Time: 0.846 ms                                                                                                         |
| Execution Time: 0.341 ms                                                                                                        |

This is the improvement I hexpected and you can see the index scans wiht the conditions be the variables that we input being used, which is very statifying!
