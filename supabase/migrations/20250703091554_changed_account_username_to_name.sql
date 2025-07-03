alter table "public"."accounts" drop constraint "accounts_username_key";

drop index if exists "public"."accounts_username_key";

alter table "public"."accounts" drop column "username";

alter table "public"."accounts" add column "name" character varying;


