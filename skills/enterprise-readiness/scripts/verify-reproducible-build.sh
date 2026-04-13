#!/bin/bash
# verify-reproducible-build.sh - Verify builds are reproducible (bit-for-bit identical)
# Usage: ./verify-reproducible-build.sh [build-type] [output-binary]
# OpenSSF Badge Criteria: build_reproducible (Gold)
#
# SECURITY: Uses an allowlist of known build commands instead of eval.
# Supported build types: go (default), docker, make, composer, npm
set -euo pipefail

# Build type (not arbitrary command) - validated against allowlist
BUILD_TYPE="${1:-go}"
OUTPUT="${2:-binary}"

# Validate that OUTPUT doesn't contain dangerous characters
if [[ "$OUTPUT" =~ [^a-zA-Z0-9._/-] ]]; then
    echo "Error: Output path contains invalid characters"
    exit 1
fi

# Execute build command from allowlist - no eval, no arbitrary input
run_build() {
    case "$BUILD_TYPE" in
        go)
            go build -trimpath -ldflags '-s -w -buildid=' -o "$OUTPUT" .
            ;;
        docker)
            docker build -o "$OUTPUT" .
            ;;
        make)
            make build
            ;;
        composer)
            composer install --no-dev --optimize-autoloader
            ;;
        npm)
            npm run build
            ;;
        *)
            echo "Error: Unknown build type '$BUILD_TYPE'"
            echo "Supported types: go, docker, make, composer, npm"
            exit 1
            ;;
    esac
}
TEMP_DIR=$(mktemp -d)

echo "=== Reproducible Build Verification ==="
echo "Build type: $BUILD_TYPE"
echo "Output file: $OUTPUT"
echo "Temp directory: $TEMP_DIR"
echo ""

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Function to compute hash
compute_hash() {
    local file="$1"
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$file" | awk '{print $1}'
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$file" | awk '{print $1}'
    else
        echo "Error: No SHA256 tool found"
        exit 1
    fi
}

echo "=== Build 1 ==="
echo "Building..."
run_build

if [ ! -f "$OUTPUT" ]; then
    echo "Error: Build output not found: $OUTPUT"
    exit 1
fi

HASH1=$(compute_hash "$OUTPUT")
SIZE1=$(wc -c < "$OUTPUT" | tr -d ' ')
echo "SHA256: $HASH1"
echo "Size: $SIZE1 bytes"

# Save first build
cp "$OUTPUT" "$TEMP_DIR/build1"

# Clean and rebuild
echo ""
echo "=== Build 2 ==="
echo "Cleaning..."
rm -f "$OUTPUT"

# Add small delay to ensure different timestamp
sleep 1

echo "Building..."
run_build

if [ ! -f "$OUTPUT" ]; then
    echo "Error: Second build output not found: $OUTPUT"
    exit 1
fi

HASH2=$(compute_hash "$OUTPUT")
SIZE2=$(wc -c < "$OUTPUT" | tr -d ' ')
echo "SHA256: $HASH2"
echo "Size: $SIZE2 bytes"

# Save second build
cp "$OUTPUT" "$TEMP_DIR/build2"

echo ""
echo "=== Comparison ==="

if [ "$HASH1" = "$HASH2" ]; then
    echo "✓ Builds are IDENTICAL"
    echo ""
    echo "SHA256: $HASH1"
    echo "Size: $SIZE1 bytes"
    echo ""
    echo "The build is reproducible!"
    echo ""
    echo "OpenSSF Badge: build_reproducible = Met"
    exit 0
else
    echo "✗ Builds are DIFFERENT"
    echo ""
    echo "Build 1: $HASH1 ($SIZE1 bytes)"
    echo "Build 2: $HASH2 ($SIZE2 bytes)"
    echo ""

    # Try to identify differences
    if command -v xxd >/dev/null 2>&1 && command -v diff >/dev/null 2>&1; then
        echo "=== Binary Differences ==="
        echo "First 10 differences:"
        diff <(xxd "$TEMP_DIR/build1") <(xxd "$TEMP_DIR/build2") 2>/dev/null | head -20 || true
    fi

    echo ""
    echo "=== Troubleshooting ==="
    echo ""
    echo "Common causes of non-reproducible builds:"
    echo ""
    echo "1. Embedded timestamps"
    echo "   Fix: Use SOURCE_DATE_EPOCH environment variable"
    echo ""
    echo "2. Embedded build paths"
    echo "   Fix (Go): Use -trimpath flag"
    echo "   Fix (C): Use -ffile-prefix-map"
    echo ""
    echo "3. Build ID embedded in binary"
    echo "   Fix (Go): Use -ldflags '-buildid='"
    echo ""
    echo "4. Non-deterministic link order"
    echo "   Fix: Sort inputs, use deterministic linker"
    echo ""
    echo "5. Parallel build race conditions"
    echo "   Fix: Use -j1 for make, single-threaded builds"
    echo ""
    echo "Recommended Go build command:"
    echo "  CGO_ENABLED=0 go build -trimpath -ldflags '-s -w -buildid=' -o binary ."
    echo ""
    echo "For more info: https://reproducible-builds.org/"
    exit 1
fi
