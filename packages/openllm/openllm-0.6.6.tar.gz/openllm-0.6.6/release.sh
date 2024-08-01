#!/usr/bin/env bash

set -e

# Function to print script usage
print_usage() {
  echo "Usage: $0 [--release <major|minor|patch|alpha>]"
}

# Function to validate release argument
validate_release() {
  local release=$1

  if [[ $release == "major" || $release == "minor" || $release == "patch" || $release == "alpha" ]]; then
    return 0
  else
    return 1
  fi
}

# Check if release flag is provided
if [[ $1 == "--release" ]]; then
  # Check if release argument is provided
  if [[ -z $2 ]]; then
    echo "Error: No release argument provided."
    print_usage
    exit 1
  fi

  release=$2

  if ! validate_release "$release"; then
    echo "Error: Invalid release argument. Only 'major', 'minor', 'patch', or 'alpha' are allowed."
    print_usage
    exit 1
  fi
else
  echo "Error: Unknown option or no option provided."
  print_usage
  exit 1
fi

# Get the current version and separate the alpha part if it exists
version="$(git describe --tags "$(git rev-list --tags --max-count=1)")"
VERSION="${version#v}"

# Initialize variables for alpha versioning
ALPHA=""
ALPHA_NUM=0

# Check if current version is an alpha version and split accordingly
if [[ $VERSION =~ -alpha ]]; then
  IFS='-' read -r BASE_VERSION ALPHA <<<"$VERSION"
  if [[ $ALPHA =~ [.] ]]; then
    IFS='.' read -r ALPHA ALPHA_NUM <<<"$ALPHA"
  fi
else
  BASE_VERSION="$VERSION"
fi

# Save the current value of IFS to restore it later and split the base version
OLD_IFS=$IFS
IFS='.'
read -ra VERSION_BITS <<<"$BASE_VERSION"
IFS=$OLD_IFS

# Assign split version numbers
VNUM1=${VERSION_BITS[0]}
VNUM2=${VERSION_BITS[1]}
VNUM3=${VERSION_BITS[2]}

# Adjust the version numbers based on the release type
if [[ $release == 'major' ]]; then
  VNUM1=$((VNUM1 + 1))
  VNUM2=0
  VNUM3=0
  ALPHA="" # Reset alpha for major release
elif [[ $release == 'minor' ]]; then
  if [[ -n $ALPHA ]]; then
    ALPHA="" # Remove alpha suffix for minor release from an alpha version
  else
    VNUM2=$((VNUM2 + 1))
    VNUM3=0
  fi
elif [[ $release == 'patch' ]]; then
  VNUM3=$((VNUM3 + 1))
  ALPHA="" # Reset alpha for patch release
elif [[ $release == 'alpha' ]]; then
  if [ -n "$ALPHA" ]; then
    ALPHA_NUM=$((ALPHA_NUM + 1))
  else
    VNUM2=$((VNUM2 + 1))
    VNUM3=0
    ALPHA="alpha"
    ALPHA_NUM=0
  fi
fi

# Construct the new version string
if [ -n "$ALPHA" ]; then
  if ((ALPHA_NUM > 0)); then
    RELEASE_VERSION="$VNUM1.$VNUM2.$VNUM3-alpha.$ALPHA_NUM"
  else
    RELEASE_VERSION="$VNUM1.$VNUM2.$VNUM3-alpha"
  fi
else
  RELEASE_VERSION="$VNUM1.$VNUM2.$VNUM3"
fi

echo "Commit count: $(git rev-list --count HEAD)"
echo "Releasing tag ${RELEASE_VERSION}..." && git tag -a "v${RELEASE_VERSION}" -m "Release ${RELEASE_VERSION} [generated by GitHub Actions]"
git push origin "v${RELEASE_VERSION}"
echo "Finish releasing OpenLLM ${RELEASE_VERSION}"
