# Container Security Assessment

**Project:** Healthcare SRE Platform  
**Image:** `healthcare-sre-api:dev`  
**Base image:** `python:3.12-slim-trixie`  
**Operating system:** Debian 13.8 (Trixie)  
**Assessment date:** November 25, 2026  
**Scanner:** Trivy 0.76.2

## 1. Vulnerability Scan Results

| Severity | Findings |
|---|---:|
| Critical | 0 |
| High | 53 |
| Medium | 76 |
| Low | 77 |
| Unknown | 16 |
| **Total** | **222** |

The scan includes narrowly scoped Rego exceptions for three setuptools findings associated with pip's bundled SBOM inventory. These are documented separately and are not blanket vulnerability exclusions.

## 2. High-Severity Findings

The 53 HIGH package findings represent 13 unique CVEs across 21 packages.

- 52 findings reported as affected.
- 1 finding reported as fix deferred.
- No fixed versions reported by Trivy at assessment time.

Major affected components include util-linux, SQLite, OpenSSL, ACL, ncurses, systemd and Perl.

## 3. Runtime Exposure Assessment

### OpenSSL
Python's `_ssl` extension dynamically loads `libssl.so.3` and `libcrypto.so.3`.

Python reported OpenSSL 3.5.9.

Two HIGH findings relate to QUIC functionality. The application does not directly implement QUIC or HTTP/3. OpenSSL remains necessary for TLS functionality and must not be removed.

### SQLite
Python's `_sqlite3` extension dynamically loads `libsqlite3.so.0`.

Python reported SQLite 3.46.1.

Three HIGH findings affect SQLite functionality. No direct SQLite, FTS5 or database usage was found in the application source or declared requirements.

Python's SQLite support remains installed as part of the runtime.

### Perl
`perl-base` is an essential Debian package.

Trivy reported two Perl findings with deferred fixes:
- CVE-2026-9538 (HIGH): Archive::Tar denial of service.
- CVE-2026-15534 (MEDIUM): Perl regular-expression vulnerability.

The package was retained rather than removing an essential operating-system component.

### Other operating-system packages
The remaining findings include util-linux, ACL, ncurses and systemd components. These require continued monitoring and package-level risk assessment.

## 4. Remediation Performed

- Explicitly selected Debian Trixie using `python:3.12-slim-trixie`.
- Applied available APT package upgrades during image build.
- Upgraded pip and setuptools.
- Created a dedicated non-root application user.
- Configured the container to run as that non-root user.
- Investigated Python runtime library dependencies.
- Checked available Debian package versions.
- Reviewed direct Python dependencies and transitive installed packages.
- Verified Python dependency consistency using `pip check`.
- Added narrowly scoped Trivy Rego exceptions for three pip bundled-SBOM setuptools findings.


## 5. Software Bill of Materials (SBOM)

Generated a CycloneDX 1.7 SBOM using Trivy 0.76.2.

- Artifact: `security/container-sbom.cdx`
- Image: `healthcare-sre-api:dev`
- Components inventoried: 141
- SBOM-based vulnerability scan: 222 Debian OS findings and 0 Python package findings.

The SBOM-based scan reproduced the vulnerability counts from the direct image scan. This provides a machine-readable inventory for software component tracking and vulnerability analysis. It does not mean the outstanding OS vulnerabilities are resolved.

## 6. Residual Risk and Follow-up

The remaining HIGH and MEDIUM findings are not considered resolved.

Actions:
1. Monitor Debian security advisories for package fixes.
2. Rebuild the image regularly using the pinned Trixie variant.
3. Repeat Trivy scans after base-image updates.
4. Reassess OpenSSL, SQLite and Perl vulnerabilities.
5. Review whether unused OS components can be safely reduced without removing essential packages.
6. Maintain documented risk acceptance for findings without available fixes.
7. Keep container scanning as a CI security gate.

## 7. Security Validation

- Bandit: Passed.
- pip-audit: Passed with no known Python dependency vulnerabilities.
- pip check: Passed.
- Trivy: 0 Critical findings; outstanding High, Medium, Low and Unknown findings remain.

### GitHub Actions CI Validation

**Workflow:** Healthcare SRE Platform CI
**Run:** [Run #5](https://github.com/afkhan2021/healthcare-sre-platform/actions/runs/45702846333)
**Commit:** `0e1ba8f`
**Date:** November 25, 2026

The container security checks were successfully executed in GitHub-hosted CI.

| Validation | Result |
|---|---|
| Docker image build | Passed |
| Trivy full vulnerability report | Passed |
| Debian OS findings (all severities) | 222 |
| Python package findings | 0 |
| Trivy Critical-only scan | 0 findings |
| Critical vulnerability gate | Passed |

The Critical-only scan returned zero findings for both Debian OS packages and Python packages. The full scan continues to report outstanding OS vulnerabilities, which remain subject to remediation and monitoring.

**Assessment conclusion:** The container has undergone security hardening and runtime dependency analysis. It is not vulnerability-free or certified for medical or production use. Outstanding operating-system vulnerabilities require ongoing remediation and risk monitoring.
