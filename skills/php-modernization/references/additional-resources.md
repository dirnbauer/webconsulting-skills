# Additional Resources

## Migration Checklist

- [ ] `declare(strict_types=1)` in all files
- [ ] PSR-4 autoloading in composer.json
- [ ] PER Coding Style enforced via PHP-CS-Fixer
- [ ] PHPStan level 9+ (level 10 for new projects)
- [ ] All methods have return types
- [ ] All parameters have type declarations
- [ ] All properties have type declarations
- [ ] **DTOs for data transfer**, Value Objects for domain concepts
- [ ] **Enums** for fixed sets of values (not string constants)
- [ ] Constructor property promotion used
- [ ] `final` on classes not designed for inheritance
- [ ] `readonly` on immutable classes
- [ ] No `@var` annotations when type is declared
- [ ] PHPat architecture tests for layer dependencies

## Resources

- **PHP-FIG**: https://www.php-fig.org/
- **PHPStan**: https://phpstan.org/
- **Rector**: https://getrector.com/
- **PHP-CS-Fixer**: https://cs.symfony.com/
- **PHPat**: https://www.phpat.dev/

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/php-modernization-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)
Adapted by webconsulting.at for this skill collection
