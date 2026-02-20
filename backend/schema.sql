-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Decisions table
CREATE TABLE IF NOT EXISTS decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL DEFAULT 'default_user',
    title TEXT NOT NULL,
    reasoning TEXT,
    assumptions TEXT,
    expected_outcome TEXT,
    confidence_score INTEGER CHECK (confidence_score BETWEEN 0 AND 100),
    category_tag TEXT,
    decision_type TEXT DEFAULT 'reversible' CHECK (decision_type IN ('reversible', 'irreversible')),
    embedding VECTOR(384),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    review_date TIMESTAMPTZ
);

-- Migration: add decision_type to existing installations
ALTER TABLE decisions ADD COLUMN IF NOT EXISTS decision_type TEXT DEFAULT 'reversible'
    CHECK (decision_type IN ('reversible', 'irreversible'));


-- Create vector similarity index
CREATE INDEX IF NOT EXISTS decisions_embedding_idx
    ON decisions USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Reflections table
CREATE TABLE IF NOT EXISTS reflections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    decision_id UUID NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    actual_outcome TEXT,
    lessons TEXT,
    accuracy_score INTEGER CHECK (accuracy_score BETWEEN 0 AND 100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Weekly summary table
CREATE TABLE IF NOT EXISTS weekly_summary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL DEFAULT 'default_user',
    week_start DATE NOT NULL,
    maintenance_pct FLOAT DEFAULT 0,
    growth_pct FLOAT DEFAULT 0,
    brand_pct FLOAT DEFAULT 0,
    admin_pct FLOAT DEFAULT 0,
    strategic_pct FLOAT DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Insights table
CREATE TABLE IF NOT EXISTS insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL DEFAULT 'default_user',
    insight_type TEXT,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed a sample weekly summary
INSERT INTO weekly_summary (user_id, week_start, maintenance_pct, growth_pct, brand_pct, admin_pct, strategic_pct)
VALUES ('default_user', CURRENT_DATE - INTERVAL '6 days', 61, 19, 8, 12, 0)
ON CONFLICT DO NOTHING;
