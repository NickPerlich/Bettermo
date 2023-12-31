create table
  public.groups (
    id bigint generated by default as identity,
    groups timestamp with time zone not null default now(),
    name text null,
    description text null,
    constraint groups_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.users (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    name text null,
    email text null,
    phone text null,
    constraint users_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.users_to_group (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    user_id integer null,
    group_id integer null,
    constraint users_to_group_pkey primary key (id)
  ) tablespace pg_default;