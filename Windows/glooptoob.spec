# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['glooptoob.pyw'],
    pathex=[],
    binaries=[],
    datas=[('glooptoob.ico', '.'), ('gt.png', '.'), ('GloopToob.lnk', '.'), ('a_download.png', '.'), ('f_download.png', '.'), ('v_download.png', '.'), ('s_download.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='glooptoob',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
