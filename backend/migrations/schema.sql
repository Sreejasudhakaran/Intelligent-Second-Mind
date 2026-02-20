-- ============================================================
-- JARVIS Database Schema  
-- PostgreSQL + pgvector
-- Run this in your Supabase SQL Editor
-- ============================================================

CREATE EXTENSION IF NOT EXISTS vector;

-- ── 1. Decisions ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS decisions (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       TEXT NOT NULL DEFAULT 'default_user',
    title         TEXT NOT NULL,
    reasoning     TEXT,
    assumptions   TEXT,
    expected_outcome TEXT,
    confidence_score INTEGER CHECK (confidence_score BETWEEN 0 AND 100),
    category_tag  TEXT DEFAULT 'Strategy',
    embedding     VECTOR(384),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    review_date   TIMESTAMPTZ
);

-- Cosine similarity index
CREATE INDEX IF NOT EXISTS decisions_embedding_cosine_idx
    ON decisions USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

CREATE INDEX IF NOT EXISTS decisions_user_created_idx
    ON decisions (user_id, created_at DESC);

-- ── 2. Reflections ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reflections (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    decision_id    UUID NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    actual_outcome TEXT,
    lessons        TEXT,
    accuracy_score INTEGER CHECK (accuracy_score BETWEEN 0 AND 100),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS reflections_decision_idx ON reflections (decision_id);

-- ── 3. Weekly Summary ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS weekly_summary (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         TEXT NOT NULL DEFAULT 'default_user',
    week_start      DATE NOT NULL,
    maintenance_pct FLOAT DEFAULT 0,
    growth_pct      FLOAT DEFAULT 0,
    brand_pct       FLOAT DEFAULT 0,
    admin_pct       FLOAT DEFAULT 0,
    strategic_pct   FLOAT DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS weekly_user_week_idx ON weekly_summary (user_id, week_start DESC);

-- ── 4. Insights ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS insights (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      TEXT NOT NULL DEFAULT 'default_user',
    insight_type TEXT,
    description  TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS insights_user_created_idx ON insights (user_id, created_at DESC);

-- ── Seed Data ─────────────────────────────────────────────
INSERT INTO weekly_summary (user_id, week_start, maintenance_pct, growth_pct, brand_pct, admin_pct, strategic_pct)
VALUES ('default_user', CURRENT_DATE - INTERVAL '6 days', 61, 19, 8, 12, 0)
ON CONFLICT DO NOTHING;
