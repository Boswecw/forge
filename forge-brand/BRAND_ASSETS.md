# Forge Brand Assets

## Canonical sources
- `forge-brand/assets/anvil-seal.svg` is the source of truth for the anvil geometry.
- `forge-brand/assets/anvil-seal-decorative.svg` must match the master geometry exactly.
- `forge-brand/assets/anvil-seal-16px.svg` is a simplified shape for small sizes.
- `forge-brand/assets/anvil-seal-with-tagline.svg` reuses the master geometry and adds the tagline.

## Usage guidance
- Use `anvil-seal.svg` for primary logo placements at 24px and up.
- Use `anvil-seal-16px.svg` when the rendered size is 16px (or smaller) to avoid loss of detail.
- Use `anvil-seal-decorative.svg` only when the icon is decorative and should be ignored by assistive tech.
- `anvil-seal-with-tagline.svg` must have its text converted to paths before shipping production assets.

## Exports
- PNGs are derivatives; never hand-edit exports.
- Export PNGs with:
  - `bash forge-brand/scripts/export-pngs.sh`
- Verify geometry drift with:
  - `node forge-brand/tools/verify-anvil-geometry.mjs`

## Rules
- SVGs are the source of truth. Update SVGs, then regenerate PNGs.
- Keep decorative geometry identical to the master.
- Convert tagline text to paths prior to release builds.
