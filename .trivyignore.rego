package trivy

import future.keywords.if

default ignore := false

ignore if {
    input.VulnerabilityID == "CVE-2025-47273"
    input.PkgIdentifier.BOMRef == "pkg:pypi/setuptools@70.3.0"
}

ignore if {
    input.VulnerabilityID == "CVE-2026-59890"
    input.PkgIdentifier.BOMRef == "pkg:pypi/setuptools@70.3.0"
}
ignore if {
    input.VulnerabilityID == "GHSA-xmj3-9gf7-h52w"
    input.PkgIdentifier.BOMRef == "pkg:pypi/setuptools@70.3.0"
}