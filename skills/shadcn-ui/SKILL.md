---
name: shadcn-ui
description: Provides shadcn/ui component patterns, CLI workflows, presets, Tailwind CSS variables, and server-rendered adaptation guidance. Use when setting up shadcn/ui, switching presets from shadcn/create, customizing themes with Tailwind CSS, implementing buttons/cards/dialogs/tables/forms/charts, or translating shadcn/ui patterns into non-React templates such as TYPO3 Fluid, Content Blocks, Alpine-driven UI, or other server-rendered component systems.
allowed-tools: Read, Write, Bash, Edit, Glob
---

# shadcn/ui Component Patterns

Build accessible, customizable UI components with shadcn/ui, Radix UI, and Tailwind CSS.

## Overview

- Components are **copied into your project** — you own and customize the code
- Built on **Radix UI** primitives for full accessibility
- Styled with **Tailwind CSS** and CSS variables for theming
- CLI-based installation: `npx shadcn@latest add <component>`
- For non-React projects, use shadcn/ui as the source for tokens, class strings, states, ARIA/data attributes, and interaction behavior; translate the output into the local component system instead of shipping React components.

## When to Use

Activate when user requests involve:
- "Set up shadcn/ui", "initialize shadcn", "add shadcn components"
- "Install button/input/form/dialog/card/select/toast/table/chart"
- "React Hook Form", "Zod validation", "form with validation"
- "accessible components", "Radix UI", "Tailwind theme"
- "shadcn button", "shadcn dialog", "shadcn sheet", "shadcn table"
- "dark mode", "CSS variables", "custom theme"
- "charts with Recharts", "bar chart", "line chart", "pie chart"
- "shadcn/create", "preset", "apply preset", "switch to --preset"
- "TYPO3 Fluid", "Content Blocks", "server-rendered shadcn", "Alpine shadcn"

## Quick Reference

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

### Start with Current Project Context

If the project has a `components.json`, run the CLI before changing components:

```bash
npx shadcn@latest info --json
```

Use the result to understand Tailwind version, aliases, base library, icon library, installed components, CSS path, and preset assumptions. If there is no `components.json`, inspect the existing build setup first and add shadcn only in the smallest shape that matches the project.

### Presets and shadcn/create

For themes built at `https://ui.shadcn.com/create`, treat the preset id as an input to the project theme pipeline:

```bash
# New or empty supported app
npx shadcn@latest init --preset b0

# Existing shadcn project
npx shadcn@latest apply --preset b3IWPgRwnI

# Theme/font-only preset update when component files should not be rewritten
npx shadcn@latest apply --preset b3IWPgRwnI --only theme
```

Keep preset ids in project configuration when the host framework supports it, for example TYPO3 Site Settings. Never fetch a preset dynamically at runtime in production; generate or commit the CSS variables and font choices.

For Tailwind v4, prefer OKLCH CSS variables, `.dark` overrides, `@theme inline`, `@custom-variant dark (&:is(.dark *))`, and a base layer that applies `border-border`, `outline-ring/50`, `bg-background`, and `text-foreground`.

### TYPO3 Fluid and Server-Rendered Adaptation

When the target project is TYPO3, Fluid, Twig, Blade, or another server-rendered stack:

- Do not install or ship shadcn React components as frontend runtime code.
- Use `npx shadcn@latest view button card tabs accordion dialog sheet table` or a temporary scratch app to inspect upstream component markup, class strings, tokens, slots, states, and ARIA patterns.
- Translate `className` to plain `class`, `data-slot` to stable `data-slot` attributes, and React state selectors to server-rendered `data-state`, ARIA, or Alpine-managed attributes.
- Build atomic Fluid components for repeated primitives: Button, Badge, Card, CardHeader, CardContent, Input, Label, Tabs, Accordion, Dialog/Sheet, Table, Alert, Separator, Skeleton.
- Keep component contracts typed with Fluid `<f:argument>` and use `<f:slot />` for child content.
- For Radix-style interactions, recreate the behavior with small Alpine or vanilla controllers while preserving keyboard support, focus behavior, ARIA-expanded/selected, and `data-state`.
- Prefer shared component templates and Tailwind utilities over per-content-element bespoke CSS.

Read `references/typo3-fluid-adapter.md` when adapting shadcn/ui to TYPO3 Content Blocks or Fluid components.

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
- **Customization**: Modify component files directly — you own the code
- **Path Aliases**: Ensure `@` alias is configured in `tsconfig.json`
- **Registry Security**: Only install components from trusted registries; review generated code before production use
- **Dark Mode**: Set up with CSS variables strategy and `next-themes`
- **Forms**: Always use `Form`, `FormField`, `FormItem`, `FormLabel`, `FormMessage` together
- **Toaster**: Add `<Toaster />` once to root layout
- **Server Rendering**: For TYPO3/Fluid adaptation, port the semantic class recipes and state attributes, not the React component implementation.
- **Preset Updates**: Commit before running `shadcn apply`, inspect the diff, then port token/class changes to owned components deliberately.
- **Future Upgrades**: Use `shadcn view`, `shadcn diff`, `shadcn apply --only theme`, and a temporary scratch project to compare upstream changes without trampling local templates.

## Constraints and Warnings

- **Not an NPM Package**: Components are copied to your project; they are not a versioned dependency
- **Registry Security**: Components from `npx shadcn@latest add` are fetched remotely; always verify the registry source is trusted before installation
- **Client Components**: Most interactive components require `"use client"` directive
- **Radix Dependencies**: Ensure all `@radix-ui` packages are installed
- **Tailwind Required**: Components rely on Tailwind CSS utilities
- **Path Aliases**: Configure `@` alias in `tsconfig.json` for imports

## References

Consult these files for detailed patterns and code examples:

- **[references/setup-and-configuration.md](references/setup-and-configuration.md)** — Full installation, tsconfig, tailwind config, CSS variables
- **[references/ui-components.md](references/ui-components.md)** — Button, Input, Card, Dialog, Sheet, Select, Toast, Table, Menubar
- **[references/forms-and-validation.md](references/forms-and-validation.md)** — React Hook Form + Zod, advanced forms, login card, contact form
- **[references/charts-components.md](references/charts-components.md)** — Bar, Line, Area, Pie charts with ChartContainer and theming
- **[references/nextjs-integration.md](references/nextjs-integration.md)** — App Router, Server/Client Components, dark mode, metadata
- **[references/customization.md](references/customization.md)** — Custom variants, CSS variables, cn() utility, extending components
- **[references/typo3-fluid-adapter.md](references/typo3-fluid-adapter.md)** — Port shadcn/ui patterns to TYPO3 Fluid, Content Blocks, Tailwind v4, Alpine, and site settings

---

## Credits & Attribution

This skill is based on the excellent work by
**[Giuseppe Trisciuoglio](https://github.com/giuseppe-trisciuoglio/developer-kit)**.

Original repository: https://github.com/giuseppe-trisciuoglio/developer-kit

Special thanks to [Giuseppe Trisciuoglio](https://github.com/giuseppe-trisciuoglio/developer-kit) for their generous open-source contributions, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
