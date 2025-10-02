#!/bin/zsh
# Build a macOS .app with AppIcon.icns, bundling UI and placing template/output next to the app

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT_DIR/venv"
OUT_DIR="$ROOT_DIR/dist/DocuFill_mac"
APP_NAME="DocuFill"
ICON_PATH="$ROOT_DIR/src/ui/resources/AppIcon.icns"

echo "==> Preparing virtual environment"
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

echo "==> Installing build dependencies"
pip install --upgrade pip >/dev/null
pip install -r "$ROOT_DIR/requirements.txt" >/dev/null

echo "==> Cleaning previous builds"
rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist"
mkdir -p "$OUT_DIR"

echo "==> Running PyInstaller"
pyinstaller \
  --noconfirm \
  --name "$APP_NAME" \
  --windowed \
  --icon "$ICON_PATH" \
  --paths "$ROOT_DIR/src" \
  --hidden-import "utils.excel_reader" \
  --hidden-import "utils.document_filler" \
  --hidden-import "constants.excel_constants" \
  --add-data "$ROOT_DIR/src/ui/index.html:ui" \
  --add-data "$ROOT_DIR/src/ui/resources/AppIcon.png:ui/resources" \
  "$ROOT_DIR/app.py"

echo "==> Assembling distribution"
rm -rf "$OUT_DIR" && mkdir -p "$OUT_DIR"
mv "$ROOT_DIR/dist/$APP_NAME.app" "$OUT_DIR/"

# Place template/ and output/ BESIDE the .app bundle
rsync -a --delete "$ROOT_DIR/template" "$OUT_DIR/" 2>/dev/null || cp -R "$ROOT_DIR/template" "$OUT_DIR/"
mkdir -p "$OUT_DIR/output"

echo "==> Creating helper script to remove quarantine and open the app"
HELPER_SCRIPT="$OUT_DIR/Open DocuFill.command"
cat > "$HELPER_SCRIPT" << 'EOF'
#!/bin/zsh
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_PATH="$APP_DIR/DocuFill.app"

if [ ! -d "$APP_PATH" ]; then
  echo "DocuFill.app not found next to this script."
  exit 1
fi

echo "Removing quarantine attributes (if present)..."
xattr -dr com.apple.quarantine "$APP_PATH" || true

echo "Opening DocuFill.app..."
open "$APP_PATH"
EOF

chmod +x "$HELPER_SCRIPT"

echo "==> Codesigning (optional; skipped if no identity)"
if security find-identity -v -p codesigning >/dev/null 2>&1; then
  echo "   You may codesign manually if needed:"
  echo "   codesign --deep --force --sign 'Developer ID Application: YOUR NAME (TEAMID)' '$OUT_DIR/$APP_NAME.app'"
fi

echo "==> Done"
echo "Open: $OUT_DIR"
echo "Contents:"
echo "- $APP_NAME.app"
echo "- template/"
echo "- output/"
echo "- Open DocuFill.command (double-click to unquarantine and launch)"


