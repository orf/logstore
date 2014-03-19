@echo off

set BUILD_DIR=%CD%\.build\
set DIST_DIR=%CD%\dist\
rm -r -f %DIST_DIR%
mkdir %DIST_DIR%

FOR /f %%d in ('dir /b /S src\ ^| grep setup.py') do (
    pushd %%~dpd
    python setup.py build --build-base=%BUILD_DIR% sdist --formats=gztar
    cp dist\* %DIST_DIR% -f
    rm -r -f dist
    python setup.py clean
    rm -r -f *.egg-info
    popd
)

rm -r -f .build

pushd %DIST_DIR%
for %%f in (*.tar.gz) DO pip install %%f --download-cache="C:\Users\tom\.pypi_cache" --find-links=%DIST_DIR% --upgrade
popd

:rm -r -f %DIST_DIR%