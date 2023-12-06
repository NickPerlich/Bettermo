-- Creating an index on the from_user column
CREATE INDEX idx_from_user ON public.transactions (from_user);

-- Creating an index on the to_user column
CREATE INDEX idx_to_user ON public.transactions (to_user);