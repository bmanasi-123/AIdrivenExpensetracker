DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'expense_category') THEN
        CREATE TYPE expense_category AS ENUM ('Food', 'Travel', 'Shopping', 'Entertainment', 'Bills', 'Other');
    END IF;
END $$;

SELECT * FROM pg_enum WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'expense_category');

CREATE TABLE IF NOT EXISTS public.expenses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES public.backend_customuser(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    category expense_category NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP	
);

select * from expenses;

EXPLAIN ANALYZE 
SELECT id, name, amount, category, created_at 
FROM expenses 
WHERE user_id = 1 
ORDER BY created_at DESC 
LIMIT 50;


CREATE INDEX idx_expenses_user_id ON expenses(user_id);

SELECT pid, age(clock_timestamp(), query_start), state, query 
FROM pg_stat_activity 
WHERE state != 'idle' 
ORDER BY query_start;

SELECT * FROM expenses WHERE user_id = 1;


