# -*- mode: python -*-

block_cipher = None


a = Analysis(['RX_COV.py'],
             pathex=['/Users/dennisngsze_yang/PycharmProjects/RX_COV_PLOT'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='RX_COV',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='RX_COV.app',
             icon=None,
             bundle_identifier=None)
