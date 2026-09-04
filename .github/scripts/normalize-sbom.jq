# Normalise a CycloneDX BOM before it is uploaded to Dependency-Track.
#
#   1. Drops components that are really manifest/lock FILES rather than
#      packages. Scanners running in filesystem mode emit these, and
#      Dependency-Track then counts each one as a licence-less component.
#   2. Fills in licences for packages whose upstream metadata genuinely omits
#      them, from .github/license-overrides.json.
#
# Usage:
#   jq --slurpfile ov .github/license-overrides.json \
#      -f .github/scripts/normalize-sbom.jq bom-raw.json > bom.json

def basename: split("/") | last;

# Manifest and lock filenames, matched on the basename so they are caught at
# any depth in a monorepo (e.g. "javascript/package-lock.json").
def is_manifest_file:
  (.name // "")
  | basename
  | test("^(?:"
      + "package-lock\\.json|npm-shrinkwrap\\.json|yarn\\.lock|pnpm-lock\\.yaml|.*lock\\.json"
      + "|Gemfile|Gemfile\\.lock|gems\\.locked"
      + "|requirements.*\\.txt|Pipfile|Pipfile\\.lock|poetry\\.lock|uv\\.lock|pyproject\\.toml|setup\\.py"
      + "|go\\.mod|go\\.sum"
      + "|Cargo\\.lock|composer\\.lock"
      + "|pom\\.xml|build\\.gradle|build\\.gradle\\.kts"
    + ")$");

# PURL without qualifiers, e.g. "pkg:npm/foo@1.0.0?arch=x64" -> "pkg:npm/foo@1.0.0".
# Yields "" for components that carry no PURL at all (scanners emit such entries
# for plain files); note jq's ("" | split("?")) is [], hence the `first // ""`.
def purl_key: (.purl // "") | split("?") | (first // "");

def has_license: ((.licenses // []) | length) > 0;

($ov[0].overrides // {}) as $overrides
| .components |= (
    (. // [])
    | map(select(is_manifest_file | not))
    | map(
        if has_license then .
        else
          ($overrides[purl_key]) as $hit
          | if $hit == null then . else .licenses = [{ "license": { "id": $hit.id } }] end
        end
      )
  )
