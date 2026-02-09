# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- Project vision and problem statement for REST API contract governance
- Class-based contract definition model (`Contract`, `Field`)
- Initial schema representation for REST API requests and responses
- Change taxonomy for schema drift detection:
  - SAFE
  - RISKY
  - BREAKING
- High-level diff engine design for comparing contract versions
- CLI command design for contract comparison (`pactify diff`)
- CI/CD–friendly exit code strategy
- Comprehensive README with examples, philosophy, and roadmap

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

---

## [0.1.0] – 2026-02-09

### Added
- Initial project scaffolding
- Core abstractions for contract-based API schemas
- Field metadata model (type, optionality, nullability, constraints)
- Diff engine skeleton for schema comparison
- Foundation for backward compatibility rules
- Repository documentation and contribution baseline

---

