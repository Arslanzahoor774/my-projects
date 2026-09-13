# import csv
# import requests
# from bs4 import BeautifulSoup
# r=requests.get("https://images.app.goo.gl/6Q8ZmbVKTiCx9ws27")
# print(r.url)
# import csv
# import requests
# from bs4 import BeautifulSoup

# url = "https://images.app.goo.gl/6Q8ZmbVKTiCx9ws27"
# r = requests.get(url)

# # Check if the request was successful (status code 200)
# if r.status_code == 200:
#     # Parse the HTML content of the page
#     soup = BeautifulSoup(r.content, 'html.parser')

#     # Extract the title of the page
#     title = soup.title.text

#     # Store the URL and title in a CSV file
#     csv_data = [{'URL': url, 'Title': title}]

#     with open('output.csv', 'w', newline='') as csv_file:
#         fieldnames = ['URL', 'Title']
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#         # Write header
#         writer.writeheader()

#         # Write data
#         writer.writerows(csv_data)

#     print(f"Data written to 'output.csv'.")
# else:
#     print("Failed to retrieve the webpage. Status code:", r.status_code)

# -*- mode: python ; coding: utf-8 -*-


# a = Analysis(
#     ['hye.py'],
#     pathex=[],
#     binaries=[],
#     datas=[],
#     hiddenimports=[],
#     hookspath=[],
#     hooksconfig={},
#     runtime_hooks=[],
#     excludes=[],
#     noarchive=False,
# )
# pyz = PYZ(a.pure)

# exe = EXE(
#     pyz,
#     a.scripts,
#     [],
#     exclude_binaries=True,
#     name='hye',
#     debug=False,
#     bootloader_ignore_signals=False,
#     strip=False,
#     upx=True,
#     console=True,
#     disable_windowed_traceback=False,
#     argv_emulation=False,
#     target_arch=None,
#     codesign_identity=None,
#     entitlements_file=None,
# )
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='hye',
# )




