Each folder / main file of the project (alphabetically)

### app.py
This is the entry file. It does checks and starts the app loop.

### data/
Contains the static files used by the app while its running. 
- **color-theme.json** is a CTk theme file
- **gdevelop-metadata.json** is a generated file containing event metadata.

### docs/
Notes for developers and contributors.

### fonts/
Font files. We currently bundle Inter.

### images/
Images icons and logo we use.

### scripts/
These are external scripts not used by the app. 
- extract-extensions.js is used to generate gdevelop-metadata.json. See [[updating-metadata]]

### src/ 
This is the main app.
- **core** contains live configurations used at runtime
- **debug** contains dead code
- **media** contains all live media e.g ImageFile etc
- **operations** contains high level functions in each domain (git, project)
- **preferences** contains code for settings and user configuration
- **utils** contains helper code
- **window** contains rendering logic

## tests/ 
Pytest functions are here
