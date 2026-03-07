# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec 文件 - 离线翻译服务
打包命令: pyinstaller translate-server.spec
"""

import os
import ctranslate2
import sentencepiece

# 获取库路径（用于拷贝 DLL / .so）
ct2_dir = os.path.dirname(ctranslate2.__file__)
sp_dir = os.path.dirname(sentencepiece.__file__)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'app',
        'app.config',
        'app.translator',
        'app.schemas',
        'app.routes',
        'app.routes.translate',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'pandas',
        'numpy.testing',
        'PIL',
        'cv2',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='translate-server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='translate-server',
)
