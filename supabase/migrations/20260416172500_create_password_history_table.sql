/*
  # Create password history table for optional cloud sync

  1. New Tables
    - `password_history`
      - `id` (uuid, primary key)
      - `user_id` (uuid, foreign key to auth.users)
      - `password_length` (integer)
      - `has_lowercase` (boolean)
      - `has_uppercase` (boolean)
      - `has_digits` (boolean)
      - `has_special` (boolean)
      - `strength_level` (text)
      - `created_at` (timestamp)

  2. Security
    - Enable RLS on `password_history` table
    - Users can only view their own password generation records
    - Users can only insert their own records
    - Users cannot modify or delete other users' records

  3. Notes
    - Actual passwords are NEVER stored for security reasons
    - Only metadata about generation parameters is tracked
    - Timestamps track when each password was generated
    - This enables optional cloud sync while maintaining security
*/

CREATE TABLE IF NOT EXISTS password_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  password_length integer NOT NULL CHECK (password_length >= 4 AND password_length <= 1024),
  has_lowercase boolean NOT NULL DEFAULT false,
  has_uppercase boolean NOT NULL DEFAULT false,
  has_digits boolean NOT NULL DEFAULT false,
  has_special boolean NOT NULL DEFAULT false,
  strength_level text NOT NULL CHECK (strength_level IN ('Weak', 'Fair', 'Strong', 'Very Strong')),
  created_at timestamptz DEFAULT now()
);

ALTER TABLE password_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own password history"
  ON password_history FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own password history"
  ON password_history FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE INDEX idx_password_history_user_id ON password_history(user_id);
CREATE INDEX idx_password_history_created_at ON password_history(created_at DESC);
