---
name: typo3-docs-php84
description: Documenting PHP 8.4 features in TYPO3 extension documentation. RST patterns for new language features.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-docs
  - php-modernization
triggers:
  - docs php 8.4
  - document php84
---

# Documenting PHP 8.4 Features

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-docs](./SKILL.md) - Main documentation guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. Documenting PHP Requirements

### Index.rst

```rst
.. include:: /Includes.rst.txt

============
My Extension
============

:Extension key:
   my_extension

:Package name:
   vendor/my-extension

:Version:
   |release|

:Language:
   en

:Author:
   Your Name

:License:
   GPL-2.0-or-later

:PHP:
   8.2 - 8.4

:TYPO3:
   13.0 - 14.x
```

---

## 2. Code Examples with PHP 8.4

### Property Hooks Documentation

```rst
Property Hooks
==============

This extension uses PHP 8.4 property hooks for validation:

.. code-block:: php
   :caption: Classes/Domain/Model/Product.php

   final class Product
   {
       public string $sku {
           set (string $value) {
               if (!preg_match('/^[A-Z]{3}-\d{4}$/', $value)) {
                   throw new \InvalidArgumentException('Invalid SKU');
               }
               $this->sku = $value;
           }
       }
   }

.. note::
   Property hooks require PHP 8.4 or higher.
```

---

## 3. Compatibility Notes

```rst
PHP Compatibility
=================

.. important::
   This extension requires PHP 8.2 or higher. PHP 8.4 is recommended
   for full feature support.

PHP 8.4 Features Used
---------------------

- Property hooks for validation
- Asymmetric visibility for encapsulation
- New array functions (``array_find``, ``array_any``, ``array_all``)

Backward Compatibility
----------------------

When running on PHP 8.2 or 8.3, the extension functions normally
but without PHP 8.4-specific optimizations.
```

---

## 4. API Documentation

```rst
API Reference
=============

ProductService
--------------

.. php:class:: Vendor\\MyExtension\\Service\\ProductService

   Service for product operations.

   .. php:method:: findActive(): array

      Find all active products.

      :returns: Array of active products
      :rtype: Product[]

      **Example:**

      .. code-block:: php

         $products = $productService->findActive();

         // PHP 8.4: Check if any are on sale
         $hasOnSale = array_any($products, fn($p) => $p->isOnSale());
```

---

## References

- [typo3-docs SKILL.md](./SKILL.md)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)
- [TYPO3 Documentation Standards](https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
