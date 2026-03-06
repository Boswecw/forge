# Markdown Import Smoke Test

Short checklist to manually verify the “Import Markdown Plan” flow in the Forge:SMITH Tauri shell. Run from the desktop build (Tauri dev or production) because the feature depends on `window.__TAURI__`.

1. Launch the Tauri app (`pnpm tauri dev` or `pnpm tauri build && ./src-tauri/target/release/app`).
2. Confirm the Planning form still renders and the new **Import Markdown Plan** button appears under the submit actions.
3. Click the button and pick `fixtures/plan_valid.md`.
   * Expect a plan session to start automatically.
   * The planning request should show the canonical Goal/Deliverable/Context block (match the normalized text you see in the streamed plan).
4. Use `fixtures/plan_warn.md` (contains ambiguous deliverables) and confirm:
   * The warnings modal appears.
   * `Memory-safe: No` is rendered when `is_memory_safe` is `false`.
   * “Continue” launches the planning session; “Cancel” stops without calling `startPlanningSession`.
5. Try importing `fixtures/plan_empty.md` (white-space only) and verify:
   * The import fails with a friendly message (“empty or contains only whitespace”).
6. Try importing `fixtures/plan_big.md` (>2 MB) and verify:
   * The import is rejected with a “larger than 2 MB” error.
7. After a successful import, inspect the new planning session in the UI or via developer tools:
   * The session’s request context should include `imported_markdown_plan` with `source_path`, `source_filename`, `imported_at`, and `content_sha256`.

### Fixtures

Create the following files under a `fixtures/` directory inside the repo (use `echo`/`cat` if needed):

* `plan_valid.md` – a small Markdown plan (`# Goal` etc.).
* `plan_warn.md` – includes a deliverables list (bullet or numbered) to trigger normalization warnings.
* `plan_empty.md` – whitespace-only file.
* `plan_big.md` – generate via `yes "line" | head -n 100000 > fixtures/plan_big.md` to exceed 2 MB.

Each fixture should be committed to the repo when the smoke test becomes part of automated QA.
