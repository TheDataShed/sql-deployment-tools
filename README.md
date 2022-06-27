# SSIS Deployments

![SQL Deployment Tools CI](https://github.com/TheDataShed/sql-deployment-tools/actions/workflows/sql-deployment-tools-ci.yml/badge.svg)
![SQL Deployment Tools - Windows](https://github.com/TheDataShed/sql-deployment-tools/actions/workflows/build-executable-windows.yml/badge.svg)
![SQL Deployment Tools - Debian](https://github.com/TheDataShed/sql-deployment-tools/actions/workflows/build-executable-debian.yml/badge.svg)
![SQL Deployment Tools - Mac OSX](https://github.com/TheDataShed/sql-deployment-tools/actions/workflows/build-executable-macosx.yml/badge.svg)
![Unit Test Results](https://gist.github.com/GooseLF/dabe49eaf9102b6392e3845b2048d664/raw/badge.svg)

## Pre-requisites

Linux will require permissions to run the build script:

```bash
chmod +x build.sh
```

### Software

- Build agent requires:
  - Windows OS
  - PowerShell (current implementation)
- DevOps extensions:
  - [SSIS DevOps Tools](https://marketplace.visualstudio.com/items?itemName=SSIS.ssis-devops-tools)

### Permissions

Each target SSIS server requires:

1. Add build agent account as SQL login
1. Create user in `SSISDB` for build agent login
1. Add the build agent user to the following roles in `SSISDB`:
   1. `ssis_admin`
   1. `db_datareader`
1. Create user in `msdb` for build agent login
1. Add the build agent user to the following roles in `msdb`:
   1. `db_datareader`
   1. `SqlAgentUserRole`

## Build

```bash
pip install --requirement requirements/build.txt
rm -rf dist/
./build.sh
```

This will create `dist/ssis-deployment.exe`.

## Deployment Steps

1. (optional?) Create SSIS Folder
1. Deploy `*.ispac` artifact to SSISDB (using SSIS DevOps Tools extension)
   1. This can include the creation of the SSIS folder/project
1. Create SSIS environment
1. Create SSIS environment reference (links the folder with the SSIS
   environment)
1. Remove/reset all SSIS environment variables
1. For each project parameter:
   1. Create/set variable
   1. Mark variable as sensitive (optional)
   1. Set reference to SSIS folder/project
1. Create SQL Agent job
1. Create job step to execute package
1. Create job schedule(s)
1. TODO: Create agent operator (optional)
1. TODO: Create notification (optional)

### Example Config

```toml
project = "Form Enrichment Sync Service"
folder = "def"
environment = "default"

[[parameters]]
name = "name1"
value = "{SECRET_VALUE}"
sensitive = true

[[parameters]]
name = "name2"
value = "value2"
sensitive = false

[job]
name = "whatever"
description = "cool"
enabled = true

[[job.steps]]
name = "todo"
type = "SSIS"
package = "FormEnrichmentSynchronisationPackage.dtsx"

[[job.steps]]
name = "2"
type = "SSIS"
package = "FormEnrichmentSynchronisationPackage.dtsx"

[[job.schedules]]
name = "name1"
every_n_minutes = 12

[[job.schedules]]
name = "name2"
every_n_minutes = 111
```

Note the `{SECRET_VALUE}` token in the above config.

This placeholder approach allows for source control of the configuration without
storing secrets.

Secrets/tokens can then be injected at deployment time using the
`--replacement-tokens` argument, e.g.:

```bash
ssis-deployment deploy --replacement-tokens '{"SECRET_VALUE": "***"}'
```

### Example Connection String

```text
Driver={SQL Server Native Client 11.0};Server=.;Database=SSISDB;Trusted_Connection=yes;
```
