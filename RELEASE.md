# Release Process

This repository defines institutional standards.
Releases must follow a controlled process.

---

# 1. Pre-release checklist

- [ ] All CI checks pass (self-test, smoke, audit paths)
- [ ] CHANGELOG updated
- [ ] VERSIONING impact evaluated
- [ ] Breaking changes reviewed
- [ ] Migration notes added (if needed)
- [ ] Example consumer still passes
- [ ] No unintended artifact path changes
- [ ] No action input/output changes without version bump

---

# 2. Version classification

Confirm release type:

- MAJOR → breaking contract change
- MINOR → backward-compatible feature
- PATCH → bugfix or non-contract change

---

# 3. Tagging

Create annotated tag:

```
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

Update moving major tag:

```
git tag -f vX
git push origin vX --force
```

---

# 4. GitHub Release

Release notes must include:

- Summary
- Added
- Changed
- Removed
- Fixed
- Migration (if applicable)

---

# 5. Post-release validation

- Confirm action can be consumed via:
  uses: julian-najas/clinical-standards/actions/audit-pack@vX
- Confirm example repository passes
- Confirm artifact structure unchanged (unless documented)
