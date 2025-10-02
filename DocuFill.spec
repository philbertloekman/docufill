# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/philbertloekman/Documents/Github/docufill/app.py'],
    pathex=['/Users/philbertloekman/Documents/Github/docufill/src'],
    binaries=[],
    datas=[('/Users/philbertloekman/Documents/Github/docufill/src/ui/index.html', 'ui'), ('/Users/philbertloekman/Documents/Github/docufill/src/ui/resources/AppIcon.png', 'ui/resources')],
    hiddenimports=['utils.excel_reader', 'utils.document_filler', 'constants.excel_constants'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DocuFill',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/philbertloekman/Documents/Github/docufill/src/ui/resources/AppIcon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DocuFill',
)
app = BUNDLE(
    coll,
    name='DocuFill.app',
    icon='/Users/philbertloekman/Documents/Github/docufill/src/ui/resources/AppIcon.icns',
    bundle_identifier=None,
)
