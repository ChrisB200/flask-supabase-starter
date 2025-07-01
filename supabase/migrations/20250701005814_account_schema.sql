create table "public"."accounts" (
    "id" uuid not null default gen_random_uuid(),
    "username" character varying not null,
    "user_id" uuid not null
);


CREATE UNIQUE INDEX accounts_pkey ON public.accounts USING btree (id);

CREATE UNIQUE INDEX accounts_user_id_key ON public.accounts USING btree (user_id);

CREATE UNIQUE INDEX accounts_username_key ON public.accounts USING btree (username);

alter table "public"."accounts" add constraint "accounts_pkey" PRIMARY KEY using index "accounts_pkey";

alter table "public"."accounts" add constraint "accounts_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."accounts" validate constraint "accounts_user_id_fkey";

alter table "public"."accounts" add constraint "accounts_user_id_key" UNIQUE using index "accounts_user_id_key";

alter table "public"."accounts" add constraint "accounts_username_key" UNIQUE using index "accounts_username_key";

grant delete on table "public"."accounts" to "anon";

grant insert on table "public"."accounts" to "anon";

grant references on table "public"."accounts" to "anon";

grant select on table "public"."accounts" to "anon";

grant trigger on table "public"."accounts" to "anon";

grant truncate on table "public"."accounts" to "anon";

grant update on table "public"."accounts" to "anon";

grant delete on table "public"."accounts" to "authenticated";

grant insert on table "public"."accounts" to "authenticated";

grant references on table "public"."accounts" to "authenticated";

grant select on table "public"."accounts" to "authenticated";

grant trigger on table "public"."accounts" to "authenticated";

grant truncate on table "public"."accounts" to "authenticated";

grant update on table "public"."accounts" to "authenticated";

grant delete on table "public"."accounts" to "service_role";

grant insert on table "public"."accounts" to "service_role";

grant references on table "public"."accounts" to "service_role";

grant select on table "public"."accounts" to "service_role";

grant trigger on table "public"."accounts" to "service_role";

grant truncate on table "public"."accounts" to "service_role";

grant update on table "public"."accounts" to "service_role";


