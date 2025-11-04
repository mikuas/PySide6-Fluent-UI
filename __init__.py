"""
python.exe -m nuitka `
         --standalone `
         --enable-plugin=pyside6 `
         --assume-yes-for-downloads `
         --windows-console-mode=disable `
         --output-dir=./bin `
         --remove-output `
         --nofollow-import-to="tkinter,turtle,test,unittest" `
         --windows-icon-from-ico=.\app.ico `
         --lto=yes `
         --jobs=16 `
         --output-filename=imageCropper `
         .\main.py

python.exe -m nuitka `
         --standalone `
         --enable-plugin=pyside6 `
         --assume-yes-for-downloads `
         --windows-console-mode=disable `
         --output-dir=./bin `
         --remove-output `
         --nofollow-import-to="tkinter,turtle,test,unittest" `
         --noinclude-dlls-from-namespace=scipy `
         --windows-icon-from-ico=.\app.ico `
         --lto=yes `
         --jobs=16 `
         --output-filename=imageCropper `
         .\main.py

"""