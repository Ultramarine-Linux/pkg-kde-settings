#/bin/sh

DATE=$(date +%Y%m%d)
EXPORT_DIR=kde-settings-4.0

set -x
rm -rf $EXPORT_DIR
# app
svn export http://svn.fedorahosted.org/svn/kde-settings/branches/F-9 $EXPORT_DIR/

tar cjf $EXPORT_DIR-${DATE}svn.tar.bz2 $EXPORT_DIR

# cleanup
rm -rf $EXPORT_DIR

