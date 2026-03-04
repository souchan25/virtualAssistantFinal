## 2024-05-24 - [High] Cross-Site Scripting (XSS) in AI Chat Render
**Vulnerability:** The ChatView component rendered AI responses using `v-html` without any sanitization, leaving it vulnerable to XSS if malicious payloads were returned (e.g., via prompt injection).
**Learning:** Even internal AI responses should be treated as untrusted input when rendered with `v-html`.
**Prevention:** Always use a sanitization library like DOMPurify (`DOMPurify.sanitize(html)`) when using `v-html` to render dynamic content.
