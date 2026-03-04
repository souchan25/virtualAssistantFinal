## 2024-03-04 - Floating Action Buttons lack focus indicators
**Learning:** Floating action buttons and modal close icons (like the one in `EmergencySOS.vue`) frequently lack keyboard focus indicators in this application's design system, making them difficult for keyboard users to interact with.
**Action:** When working on similar overlay or floating components, ensure to add accessible names (`aria-label`) and explicit focus states using `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[color]` (e.g., `focus-visible:ring-cpsu-green` or `focus-visible:ring-red-400`).
