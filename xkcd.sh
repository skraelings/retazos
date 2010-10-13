#!/bin/sh

# usage() {
#     echo "Usage:"
#     echo -e "\t$(basename $0 .sh) NUMBER1 [NUMBER2] ..."
#     exit 1
# }

xkcd_download() {
    emacs --batch --eval "(progn (load \"$(pwd)/xkcd.el\")
                                 (xkcd-retrieve \"$1\"))"
}

if test $# -eq 0; then
    xkcd_download
else
    for NUM in $@; do
	xkcd_download $NUM
    done
fi
