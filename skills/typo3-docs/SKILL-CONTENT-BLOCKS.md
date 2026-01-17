---
name: typo3-docs-content-blocks
description: Documenting Content Blocks extensions. RST patterns for config.yaml, templates, and usage examples.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-docs
  - typo3-content-blocks
triggers:
  - document content blocks
  - content blocks documentation
---

# Documenting Content Blocks

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-docs](./SKILL.md) - Main documentation guide
> - [typo3-content-blocks](../typo3-content-blocks/SKILL.md) - Content Blocks development

---

## 1. Content Block Reference

```rst
Content Elements
================

Hero Banner
-----------

The hero banner element displays a full-width header section.

**CType:** ``myvendor_hero``

**Fields:**

.. confval:: header
   :type: string
   :required: true

   Main headline of the hero section.

.. confval:: subheadline
   :type: string

   Optional subheadline text.

.. confval:: image
   :type: file
   :maxitems: 1

   Background image for the hero.

**Example:**

.. code-block:: yaml
   :caption: ContentBlocks/ContentElements/hero/config.yaml

   name: myvendor/hero
   fields:
     - identifier: header
       useExistingField: true
     - identifier: subheadline
       type: Text
     - identifier: image
       type: File
       maxitems: 1
```

---

## 2. Template Documentation

```rst
Templates
=========

Frontend Template
-----------------

.. code-block:: html
   :caption: ContentBlocks/ContentElements/hero/templates/frontend.html

   <section class="hero">
       <f:if condition="{data.image}">
           <f:for each="{data.image}" as="img">
               <f:image image="{img}" class="hero-bg"/>
           </f:for>
       </f:if>
       <h1>{data.header}</h1>
       <f:if condition="{data.subheadline}">
           <p>{data.subheadline}</p>
       </f:if>
   </section>

Template Variables
------------------

All Content Blocks templates receive:

- ``{data}`` - The content element record with all fields
- ``{data.uid}`` - The UID of the element
- ``{data.pid}`` - The page ID
- ``{data.fieldname}`` - Each custom field value
```

---

## 3. Migration Documentation

```rst
Migration from Classic TCA
==========================

If migrating from a classic extension, update your code:

**Before (Classic):**

.. code-block:: php

   $data['CType'] = 'myext_hero';
   $data['tx_myext_subheadline'] = 'Text';

**After (Content Blocks):**

.. code-block:: php

   $data['CType'] = 'myvendor_hero';
   $data['myvendor_hero_subheadline'] = 'Text';

See :ref:`typo3-content-blocks/SKILL-MIGRATION` for detailed migration steps.
```

---

## 4. Record Type Documentation

```rst
Record Types
============

Team Member
-----------

The team member record stores information about team members.

**Table:** ``tx_myvendor_team_member``

.. confval:: name
   :type: string
   :required: true

   Full name of the team member.

.. confval:: position
   :type: string

   Job title or position.

.. confval:: photo
   :type: file
   :maxitems: 1

   Profile photo.
```

---

## References

- [typo3-docs SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL.md](../typo3-content-blocks/SKILL.md)
- [TYPO3 How to Document](https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
