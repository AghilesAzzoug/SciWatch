# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deleted

## [1.1.0]

### Added

- Add [Reddit](https://www.reddit.com/) wrapper

### Changed


### Deleted

- Remove config class

## [1.0.2] - 2025-02-28

## Changed

- Updated scrapping code for Arvix (number of latest papers should be one of 25, 50, 100, 250, 500, 1000, 2000)
- Updated TechCrunch scrapping code

## [1.0.1] - 2024-06-18

## Changed

- Updated scrapping code for Arvix, TechCrunch, and OpenAI

## [1.0.0] - 2024-02-19

### Added

- Papers/blogs summary based on LLM (using [Langchain](https://www.langchain.com/))
- Send papers through Teams message (using [PyTeams](https://pypi.org/project/pymsteams))
- Send papers through Slack message (using [Slack SDK](https://slack.dev/python-slack-sdk))
- [CHANGELOG.md](./CHANGELOG.md) file
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) file

### Changed

- Updated `gmail_password` env variable to `gmail_token`
- Updated HTML email template
- Updated GitHub CI actions (Checkout & Python)

## [0.0.1] - 2023-07-30

### Added

- Package creation
