# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['assistentenlohn_1.0.py'],
             pathex=['C:\\Users\\simon\\PycharmProjects\\ad-assistentenlohn'],
             binaries=[],
             datas=[('C:/Users/simon/PycharmProjects/ad-assistentenlohn/images', 'images/')],
             hiddenimports=['sqlalchemy.sql.default_comparator', 'babel.numbers'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='assistentenlohn_1.0',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
