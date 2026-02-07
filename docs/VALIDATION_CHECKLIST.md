# Project Validation Checklist

This document outlines the comprehensive validation steps for the Email Triage Assistant. Ensure all checks are passed before major releases.

## 1. Code Quality Review
- [ ] **Linting**: Run `flake8` or `pylint` on backend code. Ensure score > 8/10.
- [ ] **Formatting**: Verify Python code follows PEP 8 and JavaScript follows standard style (e.g., Airbnb or Standard).
- [ ] **Documentation**: Ensure all functions have docstrings (reST or Google style).
- [ ] **Comments**: Verify complex logic (e.g., `ScaleDown` regex, priority scoring) is well-commented.
- [ ] **Dependencies**: Check `requirements.txt` is up-to-date and pinned to stable versions.

## 2. Functional Testing
- [ ] **EML Upload**:
    - [ ] Upload valid .eml file (< 10MB).
    - [ ] Upload invalid file type (e.g., .txt, .pdf).
    - [ ] Upload oversized file (> 10MB).
    - [ ] Upload corrupted .eml file.
- [ ] **Triage Logic**:
    - [ ] Verify priority score calculation matches expected weightings (40% urgency, 30% sender, 30% keywords).
    - [ ] Verify summary generation is accurate and concise.
- [ ] **Social Features**:
    - [ ] Verify "Like", "Comment", and "Share" interactions work in the UI.
    - [ ] Verify "Profile" view loads correctly.
    - [ ] Verify "Dark Mode" toggle persists preference (if implemented) or switches themes correctly.
- [ ] **Batch Processing**:
    - [ ] Verify batch endpoint handles multiple threads/files (mock or real).

## 3. Performance Testing
- [ ] **Load Times**: Run Google Lighthouse on the frontend. Target Performance score > 90.
- [ ] **Core Web Vitals**: Check LCP (Largest Contentful Paint) < 2.5s, CLS (Cumulative Layout Shift) < 0.1.
- [ ] **API Latency**: Ensure `/triage` endpoint responds within 2s for standard emails.
- [ ] **Memory Usage**: Monitor backend memory usage during batch processing (check for leaks).

## 4. Security Audit
- [ ] **Input Validation**: Verify server rejects malicious file names (path traversal) and payloads.
- [ ] **XSS**: Test frontend inputs (e.g., comments, search) with `<script>alert(1)</script>` to ensure escaping.
- [ ] **CSRF**: Ensure state-changing requests (if any sensitive ones exist) are protected (e.g., CSRF tokens).
- [ ] **SQL Injection**: If database is added, verify parameterized queries are used.
- [ ] **File Security**: Ensure uploaded files are processed in memory or temp storage and deleted/sanitized.

## 5. Cross-Browser Compatibility
- [ ] **Google Chrome**: Full feature test.
- [ ] **Mozilla Firefox**: Full feature test (check layout grid).
- [ ] **Safari (macOS)**: Test UI responsiveness and file upload.
- [ ] **Microsoft Edge**: Verify consistency with Chrome.

## 6. Mobile Responsiveness
- [ ] **Phone (Portrait)**: Verify 1-column layout, sidebar hidden (hamburger menu or bottom nav if implemented, currently hidden).
- [ ] **Tablet**: Verify adaptive grid.
- [ ] **Desktop**: Verify 3-column layout.
- [ ] **Touch Targets**: Ensure buttons and nav items are at least 44x44px.

## 7. API Endpoint Testing
- [ ] **Authentication**: If auth is added, verify 401/403 for unauthorized access.
- [ ] **Error Handling**: Verify API returns correct status codes (400 for bad input, 415 for bad media type, 500 for server error).
- [ ] **Payloads**: Test boundary cases (empty body, huge body, special characters).

## 8. Database Integrity (Future Proofing)
- [ ] **Schema**: Verify tables are normalized (if DB is integrated).
- [ ] **Backup**: Test backup and restore procedures.
- [ ] **Data Consistency**: Verify foreign key constraints and transaction atomicity.

## 9. Deployment Verification
- [ ] **Environment Variables**: Check `.env` is loaded correctly (API keys, debug mode).
- [ ] **Configuration**: Verify `DEBUG=False` in production.
- [ ] **Service Status**: Ensure Flask app and any background workers are running.

## 10. User Acceptance Testing (UAT)
- [ ] **Real Scenarios**: Have a user triage 10 real emails and rate the priority accuracy.
- [ ] **Feedback**: Collect feedback on UI intuitiveness (especially the social feed metaphor).
- [ ] **Edge Cases**: Ask users to try to "break" the upload (e.g., drag and drop weird files).
