@echo off

set DIST_DIR=%CD%\dist\
set PYPI_CACHE=%CD%\.pypi_cache\

pushd %DIST_DIR%
for %%f in (*.whl) DO (
    echo Installing %%f
    pip install %%f --download-cache=%PYPI_CACHE% --find-links=%DIST_DIR% --upgrade
)
popd

rm -r -f %PYPI_CACHE%