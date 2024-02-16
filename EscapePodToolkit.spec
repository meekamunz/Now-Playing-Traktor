# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['EscapePodToolKit.py'],
    pathex=[],
    binaries=[],
    datas=[('icecast.py', '.'), ('nssm.py', '.'), ('winamp.py', '.'), ('amip.py', '.'), ('functions.py', '.'), ('cleanup.py', '.'), ('traktorSettings.py', '.'), ('operateThePod.py', '.'), ('logger_config.py', '.')],
    hiddenimports=['urllib.request', 'requests', 'ctypes', 'psutil', 'pickletools', 'bs4', 'pygetwindow'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EscapePodToolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
