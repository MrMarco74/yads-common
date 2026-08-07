# Contributing to yads-common

First off, thank you for considering contributing to `yads-common`! It's people like you that make open source such a great community.

## How can I contribute?

### Reporting Bugs
- Make sure you are on the latest version.
- Use the GitHub Issues tab to search if the bug has already been reported.
- If not, open a new issue. Include a clear description of the problem, steps to reproduce it, and which downstream project (e.g. [`yads`](https://github.com/MrMarco74/yads)) you hit it from.

### Suggesting Enhancements
- Open a new issue with the label `enhancement`.
- Describe the current behavior and the new behavior you want to see.
- Explain why this enhancement would be useful to most users.

### Submitting Pull Requests
1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Update `README.md` if you change the public API.
4. Ensure your code follows the existing style and conventions.
5. Issue the pull request!

## Development Setup
`yads-common` is a small shared GUI/utility library (PySide6 helpers: dark-mode detection, ANSI-to-HTML log formatting) used across YADS tooling. The package lives in `yads_common/`.

### Running locally
```bash
pip install -e .
```
installs it editable so changes are picked up immediately by anything importing `yads_common`.

### Running the test suite
This repo doesn't currently ship a test suite — see the open issues for status, or open one if you'd like to add coverage.

## Project Philosophy

This codebase is built agentically (with Claude Code) and run as a hobby
project in the maintainer's spare time — there's no roadmap, SLA, or
guarantee that a given issue or pull request gets reviewed. Contributions
and reports are genuinely welcome, but they get acted on when they
happen to interest the maintainer, not on any particular schedule.
