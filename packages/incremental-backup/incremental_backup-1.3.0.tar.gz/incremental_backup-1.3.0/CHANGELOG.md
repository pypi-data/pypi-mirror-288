# Incremental Backup Tool - Changelog

Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The public API consists of all entities in the `incremental_backup` package and public members thereof.
Private entities begin with a single underscore (e.g. modules, functions, class members).

TODO: update when making changes.

## 1.3.0 - 2024/08/01

Add script entrypoint for package install.  
Use setuptools_scm for package versioning.

## 1.2.2 - 2024/07/10

Improve and unify test setup.

## 1.2.1 - 2024/04/28

Improve documentation.

## 1.2.0 - 2024/04/10

Flag to skip creation of backups which record no changes.

## 1.1.0 - 2024/04/04

Prune command for deleting unnecessary backups.

## 1.0.1 - 2024/02/25

Fix package version.

## 1.0.0 - 2024/02/25

Initial public release.  
Basic backup and restore functionality.
