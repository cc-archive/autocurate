#!/bin/bash -e
# -e to abort immediately on failure

## NOTE:
### uses the bashism getopts

usage() {
    cat << EOF
SAMPLE USAGE:
 ./make_package.sh -f (deb|rpm|tgz) -u 500 -p /home/cc/Desktop/Images/ -o ../filename.deb
-f means format
-u means uid
-p means path from the root
-o means filename you want to create as output

This program turns the current working directory into a package,
so usually you want -o not to be in this directory.
EOF
}

while getopts ":f:u:p:o:" options; do
    case $options in
        f ) FORMAT="$OPTARG";;
        u ) TARGET_UID="$OPTARG";;
        p ) PATH_FROM_ROOT="$OPTARG";;
        o ) OUTFILE="$OPTARG";;
        * ) usage;
            exit 1;;
    esac
done

if [[ -z $FORMAT ]] || [[ -z $TARGET_UID ]] || [[ -z $PATH_FROM_ROOT ]] || [[ -z $OUTFILE ]]
then
     usage
     exit 1
fi

# Now the fun begins.

# First, make some lousy tarball.
echo "WARNING.  I am going to create a directory called pkg-work"
echo "          and work in there.  If you don't like this, ^C now."
sleep 1 || exit 1

# Remove any evidence of our work.
rm -rf pkg-work
mkdir -p pkg-work/root

TARFILE=`mktemp -t make_package_tarfile.XXXXXXXX` &&
FAKEROOT_STATE=`mktemp -t make_package_fakeroot_state.XXXXXXXXX` && {

# Safe to use $TARFILE here
tar zcf "$TARFILE" . --exclude=pkg-work --exclude=.svn
fakeroot -i "$FAKEROOT_STATE" -s "$FAKEROOT_STATE" mkdir -p pkg-work/"$PATH_FROM_ROOT"
mkdir -p "pkg-work/root/$PATH_FROM_ROOT"
pushd "pkg-work/root/$PATH_FROM_ROOT"  >/dev/null
tar zxf "$TARFILE"
fakeroot -i "$FAKEROOT_STATE" -s "$FAKEROOT_STATE" chown "$TARGET_UID" -R .
popd >/dev/null
pushd pkg-work/root > /dev/null

SLACKWARE_PACKAGE=../slackware.tgz
fakeroot -i "$FAKEROOT_STATE" -s "$FAKEROOT_STATE" tar czf $SLACKWARE_PACKAGE .
RESULTING_PACKAGE=$(fakeroot -s "$FAKEROOT_STATE" -i "$FAKEROOT_STATE" alien "--to-$FORMAT" "$SLACKWARE_PACKAGE" | awk '{print $1}')
OLD=$(pwd)
popd >/dev/null
mv "$OLD/$RESULTING_PACKAGE" "$OUTFILE"
echo "$OUTFILE created."
rm -rf pkg-work
}

