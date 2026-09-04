# Lists BOM components that still have no licence metadata AND are real
# distributed packages — i.e. entries carrying a PURL, excluding pkg:github/
# (GitHub Actions, which Syft catalogues out of the workflow files themselves).
#
# This is the diagnostic view only; it does not alter the BOM. It deliberately
# ignores plain-file and GitHub-Action entries so the workflow log surfaces just
# the components Dependency-Track's licence report actually covers.
#
# Usage: jq -r -f .github/scripts/unlicensed-packages.jq bom.json

(.components // [])[]
| select(((.licenses // []) | length) == 0)
| select((.purl // "") != "")
| select((.purl | startswith("pkg:github/")) | not)
| "  - \(.name)@\(.version // "?")  \(.purl)"
