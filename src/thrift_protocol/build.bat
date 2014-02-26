@echo off
echo Building for Twisted
thrift-0.9.1.exe -recurse -out src/twisted --gen py:twisted,slots,utf8strings,new_style src/protocol.thrift

echo Building for Standard
thrift-0.9.1.exe -recurse -out src/plain --gen py:slots,utf8strings,new_style src/protocol.thrift