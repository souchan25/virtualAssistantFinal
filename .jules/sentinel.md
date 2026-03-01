## 2024-05-24 - [Fix XSS in ChatView]
**Vulnerability:** Found an XSS vulnerability in `Vue/src/views/ChatView.vue` where AI chat messages were rendered directly as HTML using `v-html="formatBotMessage(message.content)"` without sanitization.
**Learning:** `v-html` exposes the application to Cross-Site Scripting attacks if the source content is generated dynamically (even from AI) and could potentially include malicious script tags.
**Prevention:** Always use `DOMPurify.sanitize(html)` to sanitize the HTML before passing it to `v-html`.
