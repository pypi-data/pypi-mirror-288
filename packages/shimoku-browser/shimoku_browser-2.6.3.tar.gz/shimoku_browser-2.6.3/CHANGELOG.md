# CHANGELOG

## 2.6.3 (2024-08-01)

- Fixed actions when using files

## 2.6.2 (2024-07-29)

- Fixed more permissive and updated pandas version install error

## 2.6.1 (2024-07-29)

- More permissive and updated pandas version install

## 2.6.0 (2024-07-23)

- This version adds a request function to the main client, 
this enables the actions to use requests easily with a 
generic function

## 2.5.0 (2024-07-22)

- Dashboard roles fix

- Can invite without email

- Table links work correctly

- Users can be invited with roles

- Can get component hash externally

- Fine grained data set methods

## 2.4.0 (2024-05-10)

-  Added buttons to table rows

## 2.3.1 (2024-04-09)

- Fixed CORS error when deleting resources with Actions

## 2.3.0 (2024-04-08)

- User accounts handling through the SDK

## 2.2.3 (2024-04-05)

-  Fixed CORS error with the API from the execution of the Actions

## 2.2.2 (2024-03-22)

### Fixed

- Fixed communication with the front end in the actions execution

## 2.2.1 (2024-03-19)

### Fixed

- Next token is implement in the local server

## 2.2.0 (2024-03-18)

- Actions can be created and executed from the SDK

## 2.1.2 (2024-03-01)

- Solved cache issues with modals and tabs
- Solved execution in async context with threads
- Reformatted the code with black
- Better organization of the tests

## 2.1.1 (2024-02-20)

### Fixed

- Added the list accounts method to the local server
- Added the theme to the boards schema

## 2.1.0 (2024-02-20)

### Improvements

- Boards can have themes now, the user can set the theme of the board when creating it, or update it later.
- When creating a board, if no theme is provided the workspace theme will be used.

## 2.0.4 (2024-02-20)

### Fixed

- Fixed the github action for shimoku-browser package, that didnt set the correct version.

## 2.0.3 (2024-02-20)

### Fixed

- Fixed the github action for shimoku-browser package, that didnt set the correct version.

## 2.0.2 (2024-02-19)

Updated the github actions for the new package names.

## 2.0.0 (2024-02-15)

### Improvements

The name of the package has been changed from shimoku-api-python to shimoku.
This will be reflected in the new scripts as the users will no longer be importing the former package name, the recommended new way to import it is:


    from shimoku import Client

· The inner workings of the SDK have been separated further in order to respect the responsibilities of each module.

· The playground no longer gets initialized automatically, it needs the user to use the new CLI command.

· The code generation functionalities are no longer accessible from the client object, the user needs to use the 
commands provided in the persist module from the CLI.

· A CLI has been added to ensure full access to the functionalities of the SDK.

## 1.6.1 (2024-02-06)

### Fixed

- Roles are created correctly when creating a workspace

## 1.6 (2024-01-17)

### Added

- Added code generation, commit and pull functions to the SDK.

## 1.5 (2024-01-16)

### Added

- Shimoku AI module.

## 1.4.2 (2023-12-14)

### Fixed

- Remove vloop depencency.
- Remove warnings for pydantic

## 1.4.1 (2023-11-20)

### Fixed

- Updating a board to make it public works now.
- Added parameters to the table function to use a column of links.

## 1.4 (2023-11-15)

### Added

- This version brings a new way to develop with the SDK, the Shimoku Playground!

## 1.3 (2023-11-03)

### Improvements

New charts and options have been added:
- Indicators with:
    - Color by value
    - Marked line
    - Segmented line
    - Summary line
    - Segmented area
    - Inputs forms with Drag & Drop
- Variants have been introduced to trend charts
    - clean and minimal for all trend charts
    - shadow and thin available for bar charts, this variants can be combined with the previous ones
- The shimoku palette has been accessible through an Enum for ease of use

## 1.2.1 (2023-10-17)

### Improvements

- Check all data points before uploading the data to the platform. All columns must only contain values of one type and null values are not allowed.

## 1.2 (2023-09-26)

### Improvements

- Dataset filters have been implemented with 4 input types: 
    - Numerical
    - Date range
    - Categorical single selection
    - Categorical multiple selections

## 1.1.1 (2023-09-18)

### Fixed

- Fixed modals issue when on a subpath

## 1.1.0 (2023-08-21)

### Improvements

- Created a function in the s.activities module that enables the creation of webhooks for the activities.

### Fixes

- Get businesses returns a list of dicts
- Free echarts make a copy of the options
- Bentobox ids begin with '_' so that an issue in the FE doesnt appear
- The default bentobox has been set to {}, so that it can be unset from charts
- The SDK now understands some unsupported report types, for it not to crash
- Data sets now support bool values

## 1.0.2 (2023-08-10)

### Fixes

- Linked Indicators: Now, when a user sets the targetPath in the Indicator parameters, the indicator will be interactive and redirect to the specified link.

## 1.0.1 (2023-08-01)

### Fixes

- Solved an issue that didn't let the user create files with characters such as ',..
- Files could not be overwritten, now a parameter has been added to specify if the files want to be overwritten or not, by default set to True.

---

## 1.0.0 (2023-07-18)

### Improvements

- All charts are based on the same method as free-echarts, making them have a very similar style, and all of them use data sets.

- The free-echarts solution has more possibilities and has a more explicit use.

- State based hierarchical code definition, entering and exiting contexts easily to generate the desired components.

- Easier use of Tabs, Modals and Bentoboxes.

- Tables have been updated to use data sets.

- Charts can use shared data sets, N reports -> 1 data set.

- All the modules use the same interface for referencing resources, a uuid can be passed or a name if possible.

- Caching used resources to minimize API calls.

- Caching can be disabled and enabled.

- Lazy loading of resources (only retrieving resources when needed) to minimize API calls.

- Capacity to reuse resources when possible.

- Clearer output for verbosity options.

- Renaming of resources to clearer names for intuitive use:

- Business -> Workspace

- Dashboard -> Board

- App -> Menu path

- Path -> Sub-path

- Report -> Component

### Removed Functionalities

- Filters have been removed as the behavior is very similar to tabs, in next versions a filter that is applied to data sets will be added.
- Local aggregation of data has been removed as it does not fit well with all solutions with the current data sets.

---

## 0.20.0 (2023-05-10)

This version enables embedding, it's time to share dashboards with the internet!

### Improvements

When creating or updating a dashboard the user can set the parameter is_public to True, this will enable the embedding functionality for the dashboard in the frontal page.

See the updated documentation in:

- [Managing Dashboards](https://docs.shimoku.com/development/advanced-usage/management/managing-dashboards)

---

## 0.19.0 (2023-04-28)

This is a small version that improves the UX of the dashboard manipulation.

### Improvements

- The dashboard's default behaviour on the plotting module has been changed so that the name of the working dashboard is always respected. Before the apps were only included in a dashboard by the plotting module when the apps were being created, now every time an app is used by the plotting module it will check if the app is in the working dashboard, in case it is not, the module will automatically add the app to the dashboard.

- Now the apps can be referenced by name in the dashboards module.

- New methods have been added to the dashboards module:
- `s.dashboard.group_apps`
- `s.dashboard.remove_all_apps_from_dashboard`
- `s.dashboard.is_app_in_dashboard`
- `s.dashboard.force_delete_dashboard`

See the updated documentation in:

- [Quick Start](https://docs.shimoku.com/development/getting-started/quickstart)
- [Menu]
- [Managing Dashboards](https://docs.shimoku.com/development/advanced-usage/management/managing-dashboards)
