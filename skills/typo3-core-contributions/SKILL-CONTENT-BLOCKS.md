---
name: typo3-core-contributions-content-blocks
description: Contributing to Content Blocks extension. Patch workflow, testing, and documentation for the Content Blocks project.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-core-contributions
  - typo3-content-blocks
triggers:
  - contribute content blocks
  - content blocks patches
---

# Contributing to Content Blocks

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-core-contributions](./SKILL.md) - Main contributions guide
> - [typo3-content-blocks](../typo3-content-blocks/SKILL.md) - Content Blocks development

---

## 1. Content Blocks Repository

### GitHub Repository

Content Blocks is maintained on GitHub:

```bash
git clone https://github.com/FriendsOfTYPO3/content-blocks.git
cd content-blocks
composer install
```

### Issue Tracker

Report bugs and feature requests:
https://github.com/FriendsOfTYPO3/content-blocks/issues

---

## 2. Development Setup

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/content-blocks.git

# Add upstream
git remote add upstream https://github.com/FriendsOfTYPO3/content-blocks.git

# Create feature branch
git checkout -b feature/my-improvement
```

---

## 3. Running Tests

```bash
# Unit tests
composer test:unit

# Functional tests
composer test:functional

# All tests
composer test
```

---

## 4. Pull Request Guidelines

### Commit Message Format

```
[FEATURE] Add support for new field type

Add FieldType::Custom for user-defined field implementations.

Resolves: #123
```

### PR Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changelog entry added
- [ ] Code follows PSR-12

---

## 5. Documentation Contributions

Content Blocks documentation:
https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/

```bash
# Build docs locally
cd Documentation
make html
```

---

## References

- [typo3-core-contributions SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL.md](../typo3-content-blocks/SKILL.md)
- [Content Blocks GitHub](https://github.com/FriendsOfTYPO3/content-blocks)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
