@echo off

set BUILD_DIR=%CD%\.build\
set DIST_DIR=%CD%\dist\
rm -r -f %DIST_DIR%
mkdir %DIST_DIR%

FOR /f %%d in ('dir /b /S src\ ^| grep setup.py') do (
    pushd %%~dpd
    echo Building %%~dpd
    python setup.py -q build --build-base=%BUILD_DIR% bdist_wheel
    cp dist\* %DIST_DIR% -f
    rm -r -f dist
    python setup.py -q clean
    rm -r -f *.egg-info
    popd
)

rm -r -f .build