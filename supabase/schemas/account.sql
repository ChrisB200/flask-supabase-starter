CREATE TABLE accounts(
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL,
  name VARCHAR,
  FOREIGN KEY("user_id") REFERENCES auth.users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
