---
name: postgres-best-practices-supabase
description: Supabase-specific Postgres patterns including auth.uid(), RLS policies, Edge Functions, and MCP server integration.
version: 1.0.0
parent: postgres-best-practices
triggers:
  - supabase
  - auth.uid
  - supabase-js
  - edge-functions
  - supabase-mcp
---

# Supabase-Specific Patterns

> **Prerequisite:** Read the main `SKILL.md` first for general Postgres best practices.

This supplement covers Supabase-specific patterns including authentication, RLS with `auth.uid()`,
Edge Functions, and the Supabase MCP server for AI agents.

## 1. Authentication with auth.uid()

Supabase provides the `auth.uid()` function to get the current user's ID from the JWT.

### Basic RLS Policy with auth.uid()

```sql
-- Enable RLS on the table
alter table orders enable row level security;

-- Policy using auth.uid()
create policy "Users can view their own orders"
on orders for select
to authenticated
using (user_id = auth.uid());

-- Policy for insert
create policy "Users can insert their own orders"
on orders for insert
to authenticated
with check (user_id = auth.uid());

-- Policy for update
create policy "Users can update their own orders"
on orders for update
to authenticated
using (user_id = auth.uid())
with check (user_id = auth.uid());

-- Policy for delete
create policy "Users can delete their own orders"
on orders for delete
to authenticated
using (user_id = auth.uid());
```

### Performance: Wrap auth.uid() in SELECT

**Critical:** Always wrap `auth.uid()` in a subquery for caching.

```sql
-- BAD: auth.uid() called for every row
create policy bad_policy on orders
  using (auth.uid() = user_id);

-- GOOD: auth.uid() called once, cached
create policy good_policy on orders
  using ((select auth.uid()) = user_id);
```

### Getting User Metadata

```sql
-- Get current user's email
select auth.jwt()->>'email';

-- Get current user's role
select auth.jwt()->>'role';

-- Get custom claims
select auth.jwt()->'app_metadata'->>'organization_id';
```

## 2. Common RLS Patterns

### Team-Based Access

```sql
-- Users can access data belonging to their teams
create policy "Team members can view team data"
on projects for select
to authenticated
using (
  team_id in (
    select team_id from team_members
    where user_id = (select auth.uid())
  )
);
```

### Role-Based Access

```sql
-- Admins can do anything
create policy "Admins have full access"
on orders for all
to authenticated
using (
  (select auth.jwt()->>'role') = 'admin'
);

-- Regular users can only view their own
create policy "Users view own orders"
on orders for select
to authenticated
using (
  user_id = (select auth.uid())
  or (select auth.jwt()->>'role') = 'admin'
);
```

### Public Read, Authenticated Write

```sql
-- Anyone can read
create policy "Public read access"
on posts for select
using (true);

-- Only authenticated users can write
create policy "Authenticated users can insert"
on posts for insert
to authenticated
with check (author_id = (select auth.uid()));
```

### Time-Based Access

```sql
-- Users can only view published posts or their own drafts
create policy "View published or own posts"
on posts for select
to authenticated
using (
  published_at <= now()
  or author_id = (select auth.uid())
);
```

## 3. Supabase Client Patterns

### JavaScript/TypeScript

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
)

// Insert with automatic user_id from auth
const { data, error } = await supabase
  .from('orders')
  .insert({ product_id: 123, quantity: 2 })
  .select()

// RLS automatically filters to current user's data
const { data: orders } = await supabase
  .from('orders')
  .select('*')
```

### Server-Side with Service Role

```typescript
// Service role bypasses RLS - use carefully!
const supabaseAdmin = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

// This will return ALL orders (bypasses RLS)
const { data: allOrders } = await supabaseAdmin
  .from('orders')
  .select('*')
```

### Setting user_id Automatically

```sql
-- Use a trigger to set user_id on insert
create or replace function set_user_id()
returns trigger as $$
begin
  new.user_id := auth.uid();
  return new;
end;
$$ language plpgsql security definer;

create trigger set_user_id_trigger
before insert on orders
for each row execute function set_user_id();
```

## 4. Edge Functions with Database

### Basic Edge Function

```typescript
// supabase/functions/process-order/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    {
      global: {
        headers: { Authorization: req.headers.get('Authorization')! }
      }
    }
  )

  // Get current user
  const { data: { user } } = await supabase.auth.getUser()
  
  // RLS policies apply automatically
  const { data: orders } = await supabase
    .from('orders')
    .select('*')

  return new Response(JSON.stringify({ orders }), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

## 5. Supabase MCP Server

The [Supabase MCP server](https://supabase.com/docs/guides/getting-started/mcp) allows AI agents
to connect directly to your Supabase project.

### What MCP Provides

- Create tables and modify schemas
- Run queries and mutations
- Manage RLS policies
- Configure storage buckets
- Natural language database operations

### MCP + Best Practices

The MCP server gives agents the **ability** to work with your database.
The `postgres-best-practices` skill teaches them to do it **correctly**.

Example: When an agent uses MCP to create a table, this skill ensures it:
- Uses proper data types (`bigint` not `int`, `text` not `varchar`)
- Creates indexes on foreign keys
- Enables RLS with proper policies
- Uses `timestamptz` not `timestamp`

### MCP Configuration

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server"],
      "env": {
        "SUPABASE_URL": "https://xxx.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key"
      }
    }
  }
}
```

## 6. Database Functions

### Security Definer Functions

Use `security definer` for complex RLS checks:

```sql
create or replace function is_team_member(team_id uuid)
returns boolean
language sql
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.team_members
    where team_id = $1 and user_id = (select auth.uid())
  );
$$;

-- Use in RLS policy
create policy "Team access"
on projects for all
using ((select is_team_member(team_id)));
```

### Database Webhooks

```sql
-- Function to call Edge Function on insert
create or replace function notify_order_created()
returns trigger as $$
begin
  perform
    net.http_post(
      url := 'https://xxx.supabase.co/functions/v1/order-created',
      headers := '{"Authorization": "Bearer ' || current_setting('supabase.service_role_key') || '"}'::jsonb,
      body := row_to_json(new)::jsonb
    );
  return new;
end;
$$ language plpgsql security definer;

create trigger order_created_webhook
after insert on orders
for each row execute function notify_order_created();
```

## 7. Realtime Subscriptions

### RLS with Realtime

RLS policies automatically apply to Realtime subscriptions:

```typescript
// Only receives orders for the current user (RLS enforced)
const channel = supabase
  .channel('orders')
  .on('postgres_changes', 
    { event: '*', schema: 'public', table: 'orders' },
    (payload) => console.log(payload)
  )
  .subscribe()
```

### Broadcast with Presence

```typescript
const channel = supabase.channel('room:123')

// Track user presence
channel.on('presence', { event: 'sync' }, () => {
  const state = channel.presenceState()
  console.log('Online users:', Object.keys(state).length)
})

// Join and track
channel.subscribe(async (status) => {
  if (status === 'SUBSCRIBED') {
    await channel.track({ user_id: user.id, online_at: new Date() })
  }
})
```

## 8. Storage with RLS

### Storage RLS Policies

```sql
-- Allow users to upload to their own folder
create policy "Users can upload to their folder"
on storage.objects for insert
to authenticated
with check (
  bucket_id = 'avatars' and
  (storage.foldername(name))[1] = (select auth.uid())::text
);

-- Allow users to view their own files
create policy "Users can view their files"
on storage.objects for select
to authenticated
using (
  bucket_id = 'avatars' and
  (storage.foldername(name))[1] = (select auth.uid())::text
);
```

## Quick Reference: Supabase Functions

| Function | Description |
|----------|-------------|
| `auth.uid()` | Current user's UUID |
| `auth.jwt()` | Full JWT payload as JSONB |
| `auth.role()` | Current role (authenticated/anon) |
| `auth.email()` | Current user's email |

---

## Credits

Based on [Supabase Documentation](https://supabase.com/docs) and
[Supabase Agent Skills](https://github.com/supabase/agent-skills).
