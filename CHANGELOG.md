# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added
- Cards can now have metadata! TODO: link to readme header explaining metadata
- Improved developer experience by creating a Makefile with commonly used development commands. Its use is described in the "CONTRIBUTING.md" document. (@MarkoSagadin)
- Support for continuous integration with GitHub Actions. Backend and frontend will now build with every push to the `main` branch or to the opened PR. (@MarkoSagadin)
- Automated release process with GitHub Actions. A new release can now be manually triggered by providing the next version tag under the _Actions_ tab in the GitHub Web UI. (@MarkoSagadin)
- Added information on how to build the backend project for developers.
- Added new "scrollable code blocks" options to the config file. When set to True, 
the highlighted code blocks in generated Anki cards will be sideways scrollable. This 
option is by default disabled, to ensure that it's addition doesn't break existing 
users. (@MarkoSagadin)

### Fixed
- When reviewing card styles in Anki from its editor view, night mode now triggers the night-mode styles as expected. (@MarkoSagadin)
- Starting the program with an empty file doesn't crash it anymore.
- Removed some extra vault name checks; now you can leave the "Obsidian vault" name empty in your config file.
- Clozes are now the right color with type-in clozes.

### Changed
- Added margin to code blocks and more width to tabs on vertical screens.

## [0.2.0] - 2023-04-19

### Fixed
- Fixed bugs regarding cloze deletion handling.
- You can leave the "Obsidian vault name" empty now.

### Added
- Added a message letting you know the app is checking for when starting updates.

### Changed
- Bad cards are now appended to the "bad cards.md" file instead of overwriting the file. This way you don't have to fix them before running other imports.

## [0.1.2] - 2023-03-16

### Fixed
- Updated dependency to Type-config, which was left to an earlier version in the `pyproject.toml`

## [0.1.1] - 2023-03-16

### Added
- Better documentation for the README file, with video tutorials for the harder parts of the setup.

### Fixed
- Typos in the documentation

## [0.1.0] - 2023-03-15
Initial release! 🥳

