# VC Dashboard - UX/UI Design Specification

## Design Philosophy

**Core Principle:** Separate workflows, persistent motivation, functional workspace

**Key Insights:**
1. Jobs and Dealflow are **distinct workflows** - don't mix them
2. Gamification should be **always visible** for motivation
3. Dashboard should be **functional**, not just display stats
4. Data should **flow through** the interface naturally

---

## Layout Architecture

### Three-Column Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Top Nav: [Jobs] [Dealflow] [Dashboard]                             │
├──────────┬────────────────────────────────────┬──────────────────────┤
│          │                                    │                      │
│  Left    │         MAIN WORKSPACE             │   Right Sidebar      │
│  Nav     │                                    │   (Gamification)     │
│          │   Functional Interface             │                      │
│  [Jobs]  │   - Tables with actions            │   🔥 Overall: 0d    │
│  [Apps]  │   - Inline forms                   │   📊 Jobs: 0d       │
│          │   - Quick add                      │   🚀 Dealflow: 0d   │
│          │   - Filters/search                 │                      │
│  -------│                                    │   Weekly Goals:      │
│          │                                    │   ⭕ Jobs: 0/10     │
│  [Dash]  │                                    │   ⭕ Deals: 0/5     │
│  [Setts] │                                    │                      │
│          │                                    │   Metrics:           │
│          │                                    │   Response: 0%       │
│          │                                    │   Interview: 0%      │
│          │                                    │   Offer: 0%          │
└──────────┴────────────────────────────────────┴──────────────────────┘
```

---

## Key Components

### 1. Gamification Sidebar (Right - Always Visible)
- Streaks (Overall, Jobs, Dealflow)
- Weekly Goals (Progress rings)
- Context-aware metrics (Jobs: conversion rates, Dealflow: pipeline)
- Quick actions

### 2. Separate Workflows
- Jobs Mode: Browse → Save → Apply → Interview → Offer
- Dealflow Mode: Source → Research → Contact → Meeting → Share
- Dashboard: Analytics and overview

### 3. Functional Workspace
- Kanban boards for pipeline visualization
- Inline editing (no page navigation)
- Quick actions everywhere
- Real-time updates

---

## Implementation Priority

**Phase 1: New Layout**
1. Create 3-column layout component
2. Build persistent gamification sidebar
3. Implement top navigation switcher

**Phase 2: Jobs Workspace**
1. Jobs kanban board (Saved → Applied → Interview → Offer)
2. Inline application cards
3. Quick add functionality

**Phase 3: Dealflow Workspace**
1. Pipeline kanban (Sourced → Contacted → Meeting → Shared)
2. Startup detail cards
3. Contact logging

**Phase 4: Dashboard Analytics**
1. Performance charts
2. Trend visualization
3. Activity feed
