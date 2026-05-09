---
name: "shadcn-ui"
description: "Provides complete shadcn/ui component library patterns including installation, configuration, registry workflows, theme-token extraction, and implementation of accessible UI components. Use when setting up shadcn/ui, installing components, building forms with React Hook Form and Zod, customizing themes with Tailwind CSS, creating or consuming shadcn registries, using shadcn/create presets or previews, porting shadcn styles into non-React systems, or implementing UI patterns like buttons, dialogs, dropdowns, tables, and complex form layouts."
metadata:
  version: "1.1.1"
---

# shadcn/ui Component Patterns

Build accessible, customizable UI components with shadcn/ui, Radix UI, and Tailwind CSS.

## Overview

- Components are **copied into your project** — you own and customize the code
- Built on **Radix UI** primitives for full accessibility
- Styled with **Tailwind CSS** and CSS variables for theming
- CLI-based installation: `npx shadcn@latest add <component>`
- The shadcn CLI is also the source of truth for project introspection, presets, and registry output: `info --json`, `preset`, `view`, `docs`, and `build --output`
- Registries are framework-agnostic distribution bundles. They can package React components, theme files, hooks, pages, config, rules, or other project files when the registry item contract is explicit

## When to Use

Activate when user requests involve:
- "Set up shadcn/ui", "initialize shadcn", "add shadcn components"
- "shadcn create", "create preview", "preset", "apply theme", "decode preset"
- "custom registry", "registry.json", "registry item", "namespaced registry"
- "Install button/input/form/dialog/card/select/toast/table/chart"
- "React Hook Form", "Zod validation", "form with validation"
- "accessible components", "Radix UI", "Tailwind theme"
- "shadcn button", "shadcn dialog", "shadcn sheet", "shadcn table"
- "dark mode", "CSS variables", "custom theme"
- "charts with Recharts", "bar chart", "line chart", "pie chart"
- "use shadcn styles in TYPO3/Astro/PHP/non-React", "port shadcn styles", "token-driven components"

## Quick Reference

### CLI Workflow

| Task | Command | Notes |
|------|---------|-------|
| Initialize or create | `npx shadcn@latest init` / `npx shadcn@latest create` | `create` is an alias for `init`; choose a template such as `next`, `vite`, `laravel`, or `astro` when scaffolding a scratch project |
| Inspect project config | `npx shadcn@latest info --json` | Use before changing components, tokens, or registry setup; expect imperfect framework detection in nonstandard repos |
| Inspect preset | `npx shadcn@latest preset decode <code> --json` | Decode shadcn/create preset ids before committing theme tokens |
| Apply preset parts | `npx shadcn@latest apply <code> --only theme` | Use when only theme/font tokens should change |
| View registry item | `npx shadcn@latest view <item>` | Works with namespaced registries such as `@acme/button` |
| Search registry | `npx shadcn@latest search @shadcn -q button` | Use to find official or custom registry items |
| Build registry | `npx shadcn@latest build --output <dir>` | Reads `registry.json` and writes consumable registry item JSON |
| Fetch docs | `npx shadcn@latest docs <component> --json` | Prefer this or official docs when component APIs may have changed |

### Available Components

| Component | Install Command | Description |
|-----------|----------------|-------------|
| `button` | `npx shadcn@latest add button` | Variants: default, destructive, outline, secondary, ghost, link |
| `input` | `npx shadcn@latest add input` | Text input field |
| `form` | `npx shadcn@latest add form` | React Hook Form integration with validation |
| `card` | `npx shadcn@latest add card` | Container with header, content, footer |
| `dialog` | `npx shadcn@latest add dialog` | Modal overlay |
| `sheet` | `npx shadcn@latest add sheet` | Slide-over panel (top/right/bottom/left) |
| `select` | `npx shadcn@latest add select` | Dropdown select |
| `toast` | `npx shadcn@latest add toast` | Notification toasts |
| `table` | `npx shadcn@latest add table` | Data table |
| `menubar` | `npx shadcn@latest add menubar` | Desktop-style menubar |
| `chart` | `npx shadcn@latest add chart` | Recharts wrapper with theming |
| `textarea` | `npx shadcn@latest add textarea` | Multi-line text input |
| `checkbox` | `npx shadcn@latest add checkbox` | Checkbox input |
| `label` | `npx shadcn@latest add label` | Accessible form label |

## Instructions

### Current Workflow From shadcn/create to Production

Use this sequence when the user wants a shadcn preset, preview, registry, or non-React implementation:

1. **Identify the source.** Start from the user-provided `https://ui.shadcn.com/create` URL, `?item=preview`, preset code, registry item, or existing `components.json`.
2. **Inspect with the CLI.** Run `npx shadcn@latest info --json` in the project when `components.json` exists. If the repo is not a normal React app, treat framework detection as advisory and focus on `tailwind.css`, `style`, `base`, `iconLibrary`, aliases, and registries. Do not assume `new-york`, `default`, or any other style: `components.json` may point at a preset such as `radix-lyra`, and the official `@shadcn` registry resolves component code through `https://ui.shadcn.com/r/styles/{style}/{name}.json`.
   - For shadcn/create preset ids, decode the preset before touching component classes. Current v4 create styles decode as short names such as `nova`, `mira`, or `lyra`; registry style ids are the corresponding `radix-nova`, `radix-mira`, or `radix-lyra`. The icon library and base color also come from the preset, so sync `components.json` alongside generated primitives.
3. **Use a scratch app when needed.** For non-React systems, scaffold or inspect in an Astro/Vite/React scratch project to learn shadcn token values, primitive class contracts, component states, and data attributes. Do not copy React runtime code into the target system unless the target actually uses React.
4. **Commit tokens, not a downloader.** Store the selected preset/theme as local CSS variables, Tailwind v4 source, and project config. Keep `:root` as the light base and `.dark` as the dark override.
5. **Port component contracts.** Recreate the shadcn behavior in the target framework with semantic tokens (`--background`, `--foreground`, `--card`, `--border`, `--ring`, `--primary`, `--chart-1`...) and shared primitives. Avoid one-off visual variants that are not represented by shadcn components or tokens.
6. **Use include files for JavaScript.** Keep interactive behavior in shared JS/TS/Astro include files or framework asset pipelines. Templates should emit data attributes and structured JSON payloads rather than inline script renderers.
7. **Build and verify registries.** For custom distribution, add a root `registry.json`, a namespace in `components.json`, and a script such as `shadcn build --output public/registry`. Registry items may package theme sources, framework config, runtime assets, docs, and rules when that is the intended reusable artifact.
8. **Audit the output.** Run the relevant build/test commands, scan for raw colors outside committed token files, and verify that generated CSS/registry artifacts are in sync.

### Token and Styling Rules

- Treat shadcn/ui as the source for tokens, component class contracts, data attributes, states, spacing, borders, radius, focus rings, and typography.
- When a project uses a style preset, compare local atoms/molecules against the registry output for that exact style before applying generic examples from docs. If changing the style is requested, update the preset/config first, then port the resulting registry classes.
- Raw `oklch()`, `hsl()`, `rgb()`, and hex color values belong in the committed shadcn theme token source or generated build output. Feature code, templates, component CSS, charts, icons, and fixtures should consume semantic tokens.
- Prefer token-backed option fields (`primary`, `secondary`, `accent`, `muted`, `destructive`) over arbitrary color pickers when the UI should follow theme changes.
- Charts should use `--chart-1` through `--chart-5` or the component's generated `--color-*` variables, not hardcoded color fallbacks.
- If a project has local atoms/molecules or framework-specific primitives, update those shared primitives before editing many individual feature templates.

### Initialize Project

```bash
# New Next.js project
npx create-next-app@latest my-app --typescript --tailwind --eslint --app
cd my-app
npx shadcn@latest init

# Existing project
npm install tailwindcss-animate class-variance-authority clsx tailwind-merge lucide-react
npx shadcn@latest init

# Install components
npx shadcn@latest add button input form card dialog select toast
```

### Basic Component Usage

```tsx
// Button with variants and sizes
import { Button } from "@/components/ui/button"

<Button variant="default">Default</Button>
<Button variant="destructive" size="sm">Delete</Button>
<Button variant="outline" disabled>Loading...</Button>
```

### Form with Zod Validation

```tsx
"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "", password: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-4">
        <FormField name="email" control={form.control} render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input type="email" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <FormField name="password" control={form.control} render={({ field }) => (
          <FormItem>
            <FormLabel>Password</FormLabel>
            <FormControl><Input type="password" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit">Login</Button>
      </form>
    </Form>
  )
}
```

See [references/forms-and-validation.md](references/forms-and-validation.md) for advanced multi-field forms, contact forms with API submission, and login card patterns.

### Dialog (Modal)

```tsx
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>
    </DialogHeader>
    {/* content */}
  </DialogContent>
</Dialog>
```

### Toast Notification

```tsx
// 1. Add <Toaster /> to app/layout.tsx
import { Toaster } from "@/components/ui/toaster"

// 2. Use in components
import { useToast } from "@/components/ui/use-toast"

const { toast } = useToast()
toast({ title: "Success", description: "Changes saved." })
toast({ variant: "destructive", title: "Error", description: "Something went wrong." })
```

### Bar Chart

```tsx
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import { ChartContainer, ChartTooltipContent } from "@/components/ui/chart"

const chartConfig = {
  desktop: { label: "Desktop", color: "var(--chart-1)" },
} satisfies import("@/components/ui/chart").ChartConfig

<ChartContainer config={chartConfig} className="min-h-[200px] w-full">
  <BarChart data={data}>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="month" />
    <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
    <ChartTooltip content={<ChartTooltipContent />} />
  </BarChart>
</ChartContainer>
```

See [references/charts-components.md](references/charts-components.md) for Line, Area, and Pie chart examples.

## Examples

### Login Form with Validation
```tsx
"use client"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Min 8 characters"),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "", password: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-4">
        <FormField name="email" control={form.control} render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input type="email" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <FormField name="password" control={form.control} render={({ field }) => (
          <FormItem>
            <FormLabel>Password</FormLabel>
            <FormControl><Input type="password" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit">Login</Button>
      </form>
    </Form>
  )
}
```

### Data Table with Actions
```tsx
import { ColumnDef } from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { DataTable } from "@/components/ui/data-table"

const columns: ColumnDef<User>[] = [
  { id: "select", header: ({ table }) => (
    <Checkbox checked={table.getIsAllPageRowsSelected()} />
  ), cell: ({ row }) => (
    <Checkbox checked={row.getIsSelected()} />
  )},
  { accessorKey: "name", header: "Name" },
  { accessorKey: "email", header: "Email" },
  { id: "actions", cell: ({ row }) => (
    <Button variant="ghost" size="sm">Edit</Button>
  )},
]
```

### Dialog with Form
```tsx
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Add User</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Add New User</DialogTitle>
    </DialogHeader>
    {/* <LoginForm /> */}
  </DialogContent>
</Dialog>
```

### Toast Notifications
```tsx
import { useToast } from "@/components/ui/use-toast"
import { Button } from "@/components/ui/button"

const { toast } = useToast()

toast({ title: "Saved", description: "Changes saved successfully." })
toast({ variant: "destructive", title: "Error", description: "Failed to save." })
```

## Best Practices

- **Accessibility**: Use Radix UI primitives — ARIA attributes are built in
- **Client Components**: Add `"use client"` for interactive components (hooks, events)
- **Type Safety**: Use TypeScript and Zod schemas for form validation
- **Theming**: Configure CSS variables in `globals.css` for consistent design
- **Token Ownership**: Keep raw preset colors inside the theme token source; consume semantic tokens everywhere else
- **CLI Verification**: Run `npx shadcn@latest info --json` before and after config changes so aliases, Tailwind CSS path, style, base, icon library, and registries are visible
- **Registry Builds**: Run `npx shadcn@latest build --output <dir>` whenever `registry.json` or registry item files change
- **Customization**: Modify component files directly — you own the code
- **Path Aliases**: Ensure `@` alias is configured in `tsconfig.json`
- **Registry Security**: Only install components from trusted registries; review generated code before production use
- **Dark Mode**: Set up with CSS variables strategy and `next-themes`
- **Forms**: Always use `Form`, `FormField`, `FormItem`, `FormLabel`, `FormMessage` together
- **Toaster**: Add `<Toaster />` once to root layout

## Constraints and Warnings

- **Not an NPM Package**: Components are copied to your project; they are not a versioned dependency
- **Registry Security**: Components from `npx shadcn@latest add` are fetched remotely; always verify the registry source is trusted before installation
- **Client Components**: Most interactive components require `"use client"` directive
- **Radix Dependencies**: Ensure all `@radix-ui` packages are installed
- **Tailwind Required**: Components rely on Tailwind CSS utilities
- **Path Aliases**: Configure `@` alias in `tsconfig.json` for imports
- **Non-React Targets**: Do not install React components into TYPO3, Astro-only, PHP, or server-rendered systems as runtime code just to get the style. Use scratch apps for inspection and port the token/component contract into the target framework.
- **Framework Detection**: `shadcn info --json` can misidentify unusual repos. Trust the resolved paths and shadcn config more than the framework label.

## References

Consult these files for detailed patterns and code examples:

- **[references/setup-and-configuration.md](references/setup-and-configuration.md)** — Full installation, tsconfig, tailwind config, CSS variables
- **[references/ui-components.md](references/ui-components.md)** — Button, Input, Card, Dialog, Sheet, Select, Toast, Table, Menubar
- **[references/forms-and-validation.md](references/forms-and-validation.md)** — React Hook Form + Zod, advanced forms, login card, contact form
- **[references/charts-components.md](references/charts-components.md)** — Bar, Line, Area, Pie charts with ChartContainer and theming
- **[references/nextjs-integration.md](references/nextjs-integration.md)** — App Router, Server/Client Components, dark mode, metadata
- **[references/customization.md](references/customization.md)** — Custom variants, CSS variables, cn() utility, extending components

---

## Credits & Attribution

This skill is based on the excellent work by
**[Giuseppe Trisciuoglio](https://github.com/giuseppe-trisciuoglio/developer-kit)**.

Original repository: https://github.com/giuseppe-trisciuoglio/developer-kit

Special thanks to [Giuseppe Trisciuoglio](https://github.com/giuseppe-trisciuoglio/developer-kit) for their generous open-source contributions, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
