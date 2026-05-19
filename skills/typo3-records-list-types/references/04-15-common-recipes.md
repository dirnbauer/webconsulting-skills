# 15. Common Recipes

Continues `typo3-records-list-types` from [full guide](full-guide.md).

## 15. Common Recipes

### Grid as Default for Media Folders

```tsconfig
[traverse(page, "doktype") == 254]
    mod.web_list.viewMode.default = grid
    mod.web_list.viewMode.allowed = list,grid
    mod.web_list.gridView.cols = 6
[END]
```

### Disable Extension for Specific Pages

```tsconfig
[traverse(page, "uid") == 123 || traverse(page, "pid") == 123]
    mod.web_list.viewMode.allowed = list
[END]
```

### Force View for User Group

```tsconfig
# User TSconfig — **`options.layout.records.forceView` is provided by EXT:records_list_types**, not Core TYPO3.
options.layout.records.forceView = grid
```

### Photo Gallery (48 items, Grid template)

```tsconfig
mod.web_list.viewMode.types.gallery {
    label = Photo Gallery
    icon = actions-image
    template = GridView
    columnsFromTCA = 0
    displayColumns = label
    itemsPerPage = 48
}

mod.web_list.gridView.table.sys_file_metadata {
    titleField = title
    imageField = file
    preview = 1
}
```

### Companion Extension

Install [typo3-records-list-examples](https://github.com/dirnbauer/typo3-records-list-examples) for 6 ready-to-use view types: Timeline, Catalog, Address Book, Event List, Gallery, Dashboard.
