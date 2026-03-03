
## 2024-05-17 - Icon-Only Password Toggles and Inline Buttons Accessibility
**Learning:** In standard login forms, developers often overlook `aria-label` and `aria-pressed` for icon-only password visibility toggles. Additionally, inline `button` elements (like "Forgot password?") or absolute positioned icon buttons lack explicit `:focus-visible` styling, making keyboard navigation difficult since default browser outlines are often suppressed by modern CSS resets.
**Action:** When reviewing or implementing authentication flows, always ensure icon-only buttons have dynamic `aria-label` attributes and include explicit `focus-visible:ring-2 focus-visible:ring-[brand-color]` classes to guarantee clear keyboard focus indicators.
