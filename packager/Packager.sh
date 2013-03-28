#!/bin/bash
# Sébastien Boisvert
# automated installer

programDirectory=$(dirname $BASH_SOURCE)
template=$programDirectory/Module.txt

source $1

if test "$BuildRequires" != ""
then
	module load $BuildRequires
fi



###################

version=$Version
package=$Name
build=$Release
category=$Group
tarball=$Source0

# Download the tarball
distribution=$(basename $tarball)

mock=$package-$version-$build-Sandbox

if test -f $distribution
then
	echo "" &> /dev/null
else
	echo "[Packager] Downloading $tarball"
	wget $tarball -O $distribution
fi

rm -rf $mock
mkdir $mock
cd $mock

ln -s ../$distribution

# Uncompress
if test $(echo $distribution|grep .tar.bz2$|wc -l) -eq 1
then
	tar -xjf $distribution
elif test $(echo $distribution|grep .tar.gz$|wc -l) -eq 1
then
	tar -xzf $distribution
elif test $(echo $distribution|grep .zip$|wc -l) -eq 1
then
	unzip $distribution
fi

cd $(ls|grep -v $distribution)

packageName=$package
packageVersion=$version-$build

prefix=/software/$category/$packageName/$packageVersion

# Configure the source
echo "prefix= $prefix"

if test -f bootstrap.sh
then
	./bootstrap.sh --prefix=$prefix
	./b2 install
elif test -f configure
then
	./configure --prefix=$prefix $configureFlags
	make -j 4
	make install
elif test -f CMakeLists.txt
then
	mkdir self-build
	cd self-build
	cmake ..
	make -j 4
	cd ..

	mkdir -p $prefix
	cp -rP bin lib include $prefix
elif test -f Makefile
then
	make -j 4

	mkdir -p $prefix
	mkdir $prefix/{bin,lib,share}
	mkdir -p $prefix/share/man/man1

	for i in $(find . | grep -v self-build)
	do
		if test -x $i
		then
			cp -P $i $prefix/bin
			rm -f $prefix/bin/lib*.so*
		elif test $(echo $i|grep .1$|wc -l) -eq 1
		then
			cat $i | gzip -9 > $prefix/share/man/man1/$i.gz
		fi
	done
fi

# Create the module file
mkdir -p ~/modulefiles/$category/$packageName

moduleFile=~/modulefiles/$category/$packageName/$packageVersion

cp $template $moduleFile

expression="s/REQUIRES/$Requires/g"
sed -i "$expression" $moduleFile
expression="s/CATEGORY/$category/g"
sed -i "$expression" $moduleFile
expression="s/PACKAGE_NAME/$packageName/g"
sed -i "$expression" $moduleFile
expression="s/PACKAGE_VERSION/$packageVersion/g"
sed -i "$expression" $moduleFile

# Fix permissions
chgrp clumeq -R $prefix
chmod g+w -R $prefix
chgrp clumeq -R $moduleFile

