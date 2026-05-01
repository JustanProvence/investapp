---
name: Investment Tracker System
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#45464d'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#505f76'
  on-secondary: '#ffffff'
  secondary-container: '#d0e1fb'
  on-secondary-container: '#54647a'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#002113'
  on-tertiary-container: '#009668'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-xl:
    fontFamily: Manrope
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  data-mono:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  container-margin: 20px
  stack-gap: 12px
---

## Brand & Style

The design system is anchored in a **Corporate Modern** aesthetic, specifically tailored for high-stakes financial environments where clarity and reliability are paramount. It evokes an emotional response of security, precision, and institutional-grade intelligence. 

The visual language balances the density of data-heavy information with a breathable, minimalist layout. By utilizing significant vertical whitespace and a restricted palette, the system ensures that critical financial shifts are immediately visible without overwhelming the user. The style leverages subtle depth through layering and soft shadows to create a clear mental model of the interface's hierarchy, moving away from flat, lifeless data displays toward a more tactile and premium digital experience.

## Colors

This design system utilizes a sophisticated, high-contrast palette designed for financial legibility.

- **Primary (Deep Navy):** Used for primary headings, active navigation states, and core branding elements to establish authority.
- **Secondary (Slate Gray):** Employed for secondary text, metadata, and iconography to provide context without competing with key data.
- **Backgrounds:** A crisp white primary background is paired with a soft, off-white neutral for grouping elements, ensuring the interface feels open and "high-end."
- **Accents:** The semantic palette is strictly functional. **Emerald Green** is reserved exclusively for growth and positive delta indicators. **Amber** signals caution or pending states. **Crimson** highlights high-risk assets or significant losses. These colors should be used sparingly against the navy/white backdrop to maintain their urgency.

## Typography

**Manrope** has been selected for its modern, geometric construction and exceptional legibility in financial contexts. It offers a balanced look that feels both human and technical.

- **Data Hierarchy:** Financial figures should use a slightly heavier weight (`600` or `700`) than the surrounding descriptive text to ensure they are the primary focal point of the card.
- **Letter Spacing:** Larger displays and headlines use a slight negative letter-spacing to appear more compact and professional.
- **Labels:** Small labels use an uppercase transformation with increased letter-spacing to distinguish metadata from actionable data points.

## Layout & Spacing

The layout philosophy follows a **Fluid Grid** model designed for mobile responsiveness, emphasizing vertical flow and scannability.

- **Rhythm:** A 4px baseline grid ensures consistent vertical alignment. 
- **Vertical Breathing Room:** To prevent "data fatigue," the design system mandates generous padding within cards (minimum 20px) and substantial gaps between list items (12px).
- **Safe Areas:** All content is contained within a 20px horizontal margin to ensure visibility on all modern mobile edge-to-edge displays.
- **Grouping:** Use the `stack-gap` for related items within a section, and `xl` spacing to separate major content blocks (e.g., Portfolio Summary vs. Asset List).

## Elevation & Depth

This design system uses **Ambient Shadows** and **Tonal Layers** to create a three-dimensional hierarchy that feels tangible.

- **Level 0 (Base):** The primary background (White).
- **Level 1 (Cards/Lists):** Elements sit on the base with a subtle, diffused shadow (`Y: 4, Blur: 12, Opacity: 0.05, Color: Navy`). This distinguishes individual investment cards from the background.
- **Level 2 (Active/Modals):** Elements like focused inputs or bottom sheets use a more pronounced shadow (`Y: 8, Blur: 24, Opacity: 0.1, Color: Navy`) to indicate they are closer to the user.
- **Interactions:** Upon press, cards should visually "sink" by reducing shadow spread, providing haptic-like visual feedback.

## Shapes

The shape language is defined by **Rounded** corners, striking a balance between the precision of finance and the friendliness of modern mobile apps.

- **Cards & Primary Containers:** Use a 16px (`1rem`) radius to create a soft, contained look for data sets.
- **Buttons & Chips:** Use a full pill-shape or 12px radius to differentiate interactive elements from static containers.
- **Selection Indicators:** Small indicators (like checkboxes) use a 4px radius to maintain the system's cohesive softened geometry.

## Components

### Cards & List Items
Tables are strictly prohibited. All data must be encapsulated in **Cards** or **List Items**. 
- **Investment Cards:** Should feature a "Primary Value" in the top right, "Asset Name" in the top left, and a "Trend Sparkline" or "Percentage Change" at the bottom.
- **List Items:** Use for high-frequency data where density is needed. Each item must have a minimum height of 64px to remain touch-friendly.

### Buttons
- **Primary:** Deep Navy background with White text. Bold and authoritative.
- **Secondary:** White background with a Slate Gray border.
- **Ghost:** No border, Navy text; used for secondary actions like "View All."

### Chips
Small, low-profile containers used for asset categories (e.g., "Crypto," "Stocks"). Use a light gray background with Slate Gray text. Semantic versions (Green/Amber/Red) should use a 10% opacity background of the accent color with full-saturation text.

### Input Fields
Clean lines with a 1px Slate Gray border. When focused, the border transitions to Deep Navy with a soft glow effect.

### Progress Indicators
Used for portfolio diversification. Avoid harsh edges; use rounded caps on all bar charts and progress rings.

### Navigation
A bottom navigation bar with clear iconography and a 12px top-radius, using a blur effect (Glassmorphism) to show the content scrolling beneath it without losing legibility.