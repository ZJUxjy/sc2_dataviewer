# CSS-in-JS Approaches Reference

## Tailwind CSS

### Setup

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### config/tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          500: "#3b82f6",
          900: "#1e3a8a",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Poppins", "sans-serif"],
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
```

### styles/globals.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn {
    @apply px-4 py-2 rounded-md font-medium transition-colors;
  }
  .btn-primary {
    @apply bg-blue-600 text-white hover:bg-blue-700;
  }
}
```

### React Component with Tailwind

```tsx
interface ButtonProps {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  children: ReactNode;
  onClick?: () => void;
}

function Button({
  variant = "primary",
  size = "md",
  isLoading,
  children,
  onClick,
}: ButtonProps) {
  const base = "inline-flex items-center justify-center rounded-md font-medium";
  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
    ghost: "hover:bg-gray-100",
  };
  const sizes = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-6 py-3 text-lg",
  };

  return (
    <button
      onClick={onClick}
      disabled={isLoading}
      className={`${base} ${variants[variant]} ${sizes[size]}`}
    >
      {isLoading && <Spinner className="mr-2 animate-spin" />}
      {children}
    </button>
  );
}
```

## CSS Modules

### Component.module.css

```css
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s;
}

.primary {
  composes: button;
  background: #3b82f6;
  color: white;
}

.primary:hover {
  background: #2563eb;
}

.small {
  composes: button;
  font-size: 0.875rem;
  padding: 0.375rem 0.75rem;
}
```

### Component.tsx

```tsx
import styles from "./Button.module.css";

interface ButtonProps {
  variant?: "primary" | "secondary";
  size?: "small" | "medium" | "large";
  children: ReactNode;
}

function Button({ variant = "primary", size = "medium", children }: ButtonProps) {
  const className = [styles[variant], styles[size]].join(" ");
  return <button className={className}>{children}</button>;
}
```

## styled-components

### Setup

```bash
npm install styled-components
npm install -D @types/styled-components
```

### Component

```tsx
import styled, { css, keyframes } from "styled-components";

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

interface ButtonProps {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  fullWidth?: boolean;
}

const Button = styled.button<ButtonProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
  border: none;

  /* Variants */
  ${({ variant }) => {
    switch (variant) {
      case "primary":
        return css`
          background-color: #3b82f6;
          color: white;
          &:hover {
            background-color: #2563eb;
          }
        `;
      case "secondary":
        return css`
          background-color: #f3f4f6;
          color: #111827;
          &:hover {
            background-color: #e5e7eb;
          }
        `;
      case "ghost":
        return css`
          background-color: transparent;
          &:hover {
            background-color: #f3f4f6;
          }
        `;
      default:
        return css`
          background-color: #3b82f6;
          color: white;
        `;
    }
  }}

  /* Sizes */
  ${({ size }) => {
    switch (size) {
      case "sm":
        return css`
          padding: 0.375rem 0.75rem;
          font-size: 0.875rem;
        `;
      case "lg":
        return css`
          padding: 0.75rem 1.5rem;
          font-size: 1.125rem;
        `;
      case "md":
      default:
        return css`
          padding: 0.5rem 1rem;
          font-size: 1rem;
        `;
    }
  }}

  /* Full width */
  ${({ fullWidth }) =>
    fullWidth &&
    css`
      width: 100%;
    `}

  /* Animation */
  animation: ${fadeIn} 0.3s ease-out;

  /* Add transitions for hover states */
  transform: translateY(var(--hover-adjust, 0px));

  &:hover {
    --hover-adjust: -2px;
  }
`;
```

### Theme Provider

```tsx
import { ThemeProvider } from "styled-components";
import type { ReactNode } from "react";

const theme = {
  colors: {
    primary: "#3b82f6",
    secondary: "#8b5cf6",
    success: "#10b981",
    error: "#ef4444",
  },
  spacing: {
    sm: "0.5rem",
    md: "1rem",
    lg: "1.5rem",
  },
  breakpoints: {
    mobile: "480px",
    tablet: "768px",
    desktop: "1024px",
  },
};

export function App({ children }: { children: ReactNode }) {
  return <ThemeProvider theme={theme}>{children}</ThemeProvider>;
}

// Usage
const Card = styled.div`
  border: 1px solid ${({ theme }) => theme.colors.gray[200]};
  padding: ${({ theme }) => theme.spacing.md};

  @media (max-width: ${({ theme }) => theme.breakpoints.tablet}) {
    padding: ${({ theme }) => theme.spacing.sm};
  }
`;
```

## Emotion

### Setup

```bash
npm install @emotion/react @emotion/styled
```

### Component

```tsx
/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";

const buttonBase = css`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
`;

const buttonVariants = {
  primary: css`
    background-color: #3b82f6;
    color: white;
    &:hover {
      background-color: #2563eb;
    }
  `,
  secondary: css`
    background-color: #f3f4f6;
    color: #111827;
    &:hover {
      background-color: #e5e7eb;
    }
  `,
};

interface ButtonProps {
  variant?: keyof typeof buttonVariants;
  size?: "sm" | "md" | "lg";
  children: ReactNode;
}

function Button({ variant = "primary", size = "md", children }: ButtonProps) {
  const sizeStyles = {
    sm: css`
      padding: 0.375rem 0.75rem;
      font-size: 0.875rem;
    `,
    md: css`
      padding: 0.5rem 1rem;
      font-size: 1rem;
    `,
    lg: css`
      padding: 0.75rem 1.5rem;
      font-size: 1.125rem;
    `,
  };

  return (
    <button css={[buttonBase, buttonVariants[variant], sizeStyles[size]]}>
      {children}
    </button>
  );
}
```

### Styled Components with Emotion

```tsx
import styled from "@emotion/styled";

interface FlexProps {
  direction?: "row" | "column";
  justify?: "flex-start" | "center" | "flex-end" | "space-between";
  align?: "flex-start" | "center" | "flex-end";
  gap?: "xs" | "sm" | "md" | "lg";
}

const Flex = styled.div<FlexProps>`
  display: flex;
  flex-direction: ${({ direction }) => direction || "row"};
  justify-content: ${({ justify }) => justify || "flex-start"};
  align-items: ${({ align }) => align || "flex-start"};
  gap: ${({ gap = "md" }) => {
    const gaps = { xs: "2px", sm: "4px", md: "8px", lg: "16px" };
    return gaps[gap];
  }};
`;

// Usage
function Header() {
  return (
    <Flex justify="space-between" align="center" gap="lg">
      <Logo />
      <Navigation />
      <UserMenu />
    </Flex>
  );
}
```

## Vanilla Extract

### Setup

```bash
npm install @vanilla-extract/css
npm install -D @vanilla-extract/webpack-plugin
```

### Component.css.ts

```typescript
import { style, styleVariants, globalStyle } from "@vanilla-extract/css";
import { theme } from "./theme.css";

export const base = style({
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  borderRadius: "6px",
  fontWeight: 500,
  transition: "all 0.2s",
  cursor: "pointer",
  border: "none",
});

export const variants = styleVariants({
  primary: [
    base,
    {
      backgroundColor: theme.colors.primary,
      color: theme.colors.white,
      ":hover": {
        backgroundColor: theme.colors.primaryHover,
      },
    },
  ],
  secondary: [
    base,
    {
      backgroundColor: theme.colors.gray100,
      color: theme.colors.gray900,
      ":hover": {
        backgroundColor: theme.colors.gray200,
      },
    },
  ],
});

export const sizes = styleVariants({
  sm: {
    padding: "6px 12px",
    fontSize: "14px",
  },
  md: {
    padding: "8px 16px",
    fontSize: "16px",
  },
  lg: {
    padding: "12px 24px",
    fontSize: "18px",
  },
});

export const compound = styleVariants(
  {
    primary: variants.primary,
    secondary: variants.secondary,
    sm: sizes.sm,
    md: sizes.md,
    lg: sizes.lg,
  },
  (variantClass, sizeClass) => [variantClass, sizeClass],
);
```

### Component.tsx

```tsx
import { clsx } from "clsx";
import * as styles from "./Button.css";

interface ButtonProps {
  variant?: keyof typeof styles.variants;
  size?: keyof typeof styles.sizes;
  children: ReactNode;
}

function Button({ variant = "primary", size = "md", children }: ButtonProps) {
  return (
    <button className={clsx(styles.variants[variant], styles.sizes[size])}>
      {children}
    </button>
  );
}
```

## Svelte CSS Patterns

### Svelte Component Styles

```svelte
<script lang="ts">
  export let variant: 'primary' | 'secondary' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
</script>

<button class:primary={variant === 'primary'}
        class:secondary={variant === 'secondary'}
        class:sm={size === 'sm'}
        class:md={size === 'md'}
        class:lg={size === 'lg'}>
  <slot />
</button>

<style lang="scss">
  button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.2s;
    cursor: pointer;
    border: none;
  }

  .primary {
    background: #3b82f6;
    color: white;
    &:hover {
      background: #2563eb;
    }
  }

  .sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
  }
</style>
```

## Vue 3 CSS Patterns

### Single File Component

```vue
<template>
  <button :class="buttonClasses" :disabled="isLoading || disabled">
    <Spinner v-if="isLoading" class="mr-2" />
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    variant?: "primary" | "secondary" | "ghost";
    size?: "sm" | "md" | "lg";
    isLoading?: boolean;
    disabled?: boolean;
  }>(),
  {
    variant: "primary",
    size: "md",
    isLoading: false,
    disabled: false,
  },
);

const buttonClasses = computed(() => [
  "inline-flex items-center justify-center rounded-md font-medium transition-colors",
  {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
    ghost: "hover:bg-gray-100",
  }[props.variant],
  {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-6 py-3 text-lg",
  }[props.size],
  (props.isLoading || props.disabled) && "opacity-50 cursor-not-allowed",
]);
</script>
```

## CSS Variables (Design Tokens)

### :root Variables

```css
:root {
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;
  
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
}

/* Dark mode */
[data-theme="dark"] {
  --color-primary-500: #60a5fa;
  --color-bg: #1f2937;
  --color-text: #f9fafb;
}
```

### Component Usage

```tsx
const Card = styled.div`
  background: var(--color-bg, white);
  color: var(--color-text, black);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;
```

## Comparison Matrix

| Framework      | Runtime | Bundle Size | Type Safety | SSR  | Learning Curve |
| -------------- | ------- | ----------- | ----------- | ---- | -------------- |
| Tailwind CSS   | None    | Medium      | ✅ Good     | ✅   | Low            |
| CSS Modules    | None    | Small       | ⚠️ Limited  | ✅   | Low            |
| styled-comps   | Yes     | Large       | ⚠️ Limited  | ⚠️   | Medium         |
| Emotion        | Yes     | Medium      | ✅ Good     | ✅   | Medium         |
| Vanilla Extract| None    | Small       | ✅ Excellent| ✅   | Medium         |

## Recommendations

- **New React/Vue projects**: Tailwind CSS for speed + Vanilla Extract for complex components
- **Design systems**: Vanilla Extract for type-safe tokens + Tailwind for utilities
- **Legacy migration**: CSS Modules for gradual adoption
- **Rapid prototypes**: Tailwind CSS
- **Performance-critical**: Vanilla Extract or CSS Modules
- **Dynamic styling**: Emotion (over styled-components for performance)
