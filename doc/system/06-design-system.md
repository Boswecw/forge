# §6 — Design System

## Design Philosophy

Forge's visual identity is a **dark-mode HUD** inspired by Bloomberg Terminal aesthetics — information-dense, low-distraction, and purpose-built for governance-critical workflows. There is no light mode. Every pixel earns its place.

**Guiding rules:**
- Dark-mode only — `--forge-void` (#07080c) is the canvas
- No rounded corners > 8px — "this is a HUD, not a toy"
- Transitions 150-250ms — never slower (HUD speed)
- Service identity colors are immutable across all Forge apps
- Budget thresholds: 80% warning (amber), 95% critical (red)

---

## Surface Hierarchy

Five surface layers create depth without shadows:

| Token | Hex | Role |
|-------|-----|------|
| `--forge-void` | `#07080c` | Page canvas — deepest background |
| `--forge-obsidian` | `#0e1018` | Primary card/panel surface |
| `--forge-slate` | `#161a24` | Elevated surfaces, sidebars |
| `--forge-steel` | `#1e2330` | Hover states, active panels |
| `--forge-edge` | `#2a3040` | Borders, dividers |

---

## Service Identity Colors

Each Forge service has an immutable color pair. These are non-negotiable — they identify services across all consumer apps, dashboards, and documentation.

| Service | Token | Hex | Glow Variant |
|---------|-------|-----|-------------|
| DataForge | `--dataforge-blue` | `#3b82f6` | `--dataforge-glow`: `#60a5fa` |
| NeuroForge | `--neuroforge-violet` | `#8b5cf6` | `--neuroforge-glow`: `#a78bfa` |
| Rake | `--rake-bronze` | `#d97706` | `--rake-glow`: `#f59e0b` |
| SMITH | `--smith-emerald` | `#10b981` | `--smith-glow`: `#34d399` |

---

## Ember Accent System

The primary accent is **ember** — the visual metaphor for the forge's fire. Used for CTAs, focus rings, and primary actions.

| Token | Hex | Usage |
|-------|-----|-------|
| `--ember-core` | `#f97316` | Primary CTA color |
| `--ember-hot` | `#fb923c` | Hover state |
| `--ember-dim` | `#9a3412` | Pressed/active |
| `--ember-glow` | `rgba(249, 115, 22, 0.15)` | Background glow |

---

## Semantic Status Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `--status-active` | `#3b82f6` | Running, in progress |
| `--status-success` | `#10b981` | Completed, healthy |
| `--status-warning` | `#f59e0b` | Needs attention, budget 80% |
| `--status-danger` | `#ef4444` | Failed, error, budget 95% |
| `--status-neutral` | `#6b7280` | Inactive, cancelled |

**Budget threshold conventions:**
- < 80% of cap: normal (no status indicator)
- 80-94%: `--status-warning` with amber badge
- 95%+: `--status-danger` with red badge + alert

---

## Typography

| Token | Value | Usage |
|-------|-------|-------|
| `--font-ui` | `'Inter', -apple-system, sans-serif` | Body text, labels, UI elements |
| `--font-mono` | `'JetBrains Mono', 'Fira Code', monospace` | Code blocks, terminal output, IDs |
| `--font-display` | `'Inter', sans-serif` | Page titles, hero metrics |

### Type Scale

| Token | Size | Usage |
|-------|------|-------|
| `--text-xs` | 0.75rem (12px) | Badges, timestamps |
| `--text-sm` | 0.875rem (14px) | Table cells, metadata |
| `--text-base` | 1rem (16px) | Body text |
| `--text-lg` | 1.125rem (18px) | Section headers |
| `--text-xl` | 1.25rem (20px) | Page titles |
| `--text-2xl` | 1.5rem (24px) | Page section titles |
| `--text-3xl` | 1.875rem (30px) | Hero metrics, KPIs |

---

## Spacing

4px increment system:

| Token | Value | Token | Value |
|-------|-------|-------|-------|
| `--space-1` | 0.25rem (4px) | `--space-8` | 2rem (32px) |
| `--space-2` | 0.5rem (8px) | `--space-10` | 2.5rem (40px) |
| `--space-3` | 0.75rem (12px) | `--space-12` | 3rem (48px) |
| `--space-4` | 1rem (16px) | `--space-16` | 4rem (64px) |
| `--space-5` | 1.25rem (20px) | `--space-20` | 5rem (80px) |
| `--space-6` | 1.5rem (24px) | `--space-24` | 6rem (96px) |

---

## Borders & Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-xs` | 2px | Badges |
| `--radius-sm` | 4px | Inputs, buttons |
| `--radius-md` | 6px | Cards |
| `--radius-lg` | 8px | Modals, panels (maximum allowed) |
| `--border-subtle` | `1px solid var(--forge-edge)` | Standard divider |
| `--border-focus` | `1px solid rgba(249, 115, 22, 0.4)` | Ember focus ring |

---

## Shadows & Glows

Subtle depth — no floating-card effects.

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-inset` | `inset 0 1px 0 rgba(255,255,255,0.03)` | Subtle top highlight |
| `--shadow-glow-ember` | `0 0 20px rgba(249,115,22,0.08)` | Active/focused ember elements |
| `--shadow-glow-blue` | `0 0 20px rgba(59,130,246,0.08)` | DataForge-associated elements |
| `--shadow-glow-violet` | `0 0 20px rgba(139,92,246,0.08)` | NeuroForge-associated elements |
| `--shadow-glow-emerald` | `0 0 20px rgba(16,185,129,0.08)` | SMITH-associated elements |

---

## Transitions

| Token | Duration | Usage |
|-------|----------|-------|
| `--duration-fast` | 150ms | Hover, focus, small toggles |
| `--duration-normal` | 200ms | Panel transitions, dropdowns |
| `--duration-slow` | 250ms | Modal open/close (maximum allowed) |

Easing functions:

| Token | Curve |
|-------|-------|
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` |
| `--ease-in` | `cubic-bezier(0.7, 0, 0.84, 0)` |
| `--ease-in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` |

---

## Z-Index Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--z-base` | 0 | Normal flow |
| `--z-dropdown` | 100 | Dropdowns, menus |
| `--z-sticky` | 200 | Sticky headers |
| `--z-overlay` | 300 | Overlays |
| `--z-modal` | 400 | Modals |
| `--z-popover` | 500 | Popovers |
| `--z-toast` | 600 | Toasts |
| `--z-tooltip` | 700 | Tooltips |
| `--z-command-palette` | 800 | Command palette (highest) |

---

## Layout Dimensions

| Token | Value | Usage |
|-------|-------|-------|
| `--sidebar-width-collapsed` | 56px | Nav sidebar (collapsed) |
| `--sidebar-width-expanded` | 240px | Nav sidebar (expanded) |
| `--topbar-height` | 48px | Top navigation bar |
| `--statusbar-height` | 28px | Bottom status bar |
| `--gutter` | 16px | Column gutter |
| `--page-padding` | 24px | Page content padding |
| `--card-padding` | 16px | Card internal padding |

---

## Component Conventions

All UI components follow these patterns (see §7 for implementation details):

### Variant Props

Components expose a `variant` prop for visual variants:

```
variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
size?: 'sm' | 'md' | 'lg'
```

### Slot Pattern

Components use Svelte 5 `Snippet` type for composable content:

```
children?: Snippet          — Main content area
header?: Snippet            — Custom header
actions?: Snippet           — Action buttons
footer?: Snippet            — Custom footer
```

### Event Pattern

Components use callback props (not dispatchers):

```
onclick?: () => void
onSave?: (data: T) => void
onCancel?: () => void
```

---

## Token Source File

All tokens are defined in a single source of truth:

```
forge-smithy/src/styles/forge-tokens.css
```

Consumer apps and services should reference these tokens. No hardcoded color values.

---

*For component implementation patterns, see §7. For service identity usage in API responses, see §8.*
