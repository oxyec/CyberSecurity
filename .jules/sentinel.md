## 2025-06-21 - [Ineffective Login Rate Limiting and Default View Bypass]
**Vulnerability:**
1.  Rate limiting logic was implemented in `form_invalid`, which executes *after* form validation and authentication (password hashing). This allows an attacker to exhaust server CPU by sending many login requests, even if they are eventually blocked by the limit, because the expensive `authenticate()` function is called for every request.
2.  The application defined a secure `CustomLoginView` but the default `/accounts/login/` URL (used by `@login_required`) was mapped to Django's standard `LoginView`, effectively bypassing the security controls.

**Learning:**
Security controls must be placed *before* the expensive operations they are meant to protect. Specifically, rate limiting should happen in `dispatch` or middleware, not in form validation methods.
Also, ensuring that *all* entry points to a sensitive function are protected is crucial. Having a secure view is useless if the application defaults to an insecure one.

**Prevention:**
-   Implement rate limiting in `dispatch()` or use a middleware/decorator that runs early in the request lifecycle.
-   Audit `urls.py` to ensure that standard paths (like `accounts/login/`) are overridden to use the secured views.
-   Test security controls by verifying *resource usage* (e.g., call counts to expensive functions), not just the final outcome (pass/fail).
