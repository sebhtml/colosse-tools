#!/bin/bash
# Sébastien Boisvert
# automated installer

source $1

###################

# Download the tarball
distribution=$(basename $tarball)

if test -f $distribution
then
	echo "" &> /dev/null
else
	echo "[Packager] Downloading $tarball"
	wget $tarball -O $distribution
fi

rm -rf $package-$version

# Uncompress
if test $(echo $distribution|grep .tar.bz2$|wc -l) -eq 1
then
	tar -xjf $distribution
elif test $(echo $distribution|grep .tar.gz$|wc -l) -eq 1
then
	tar -xzf $distribution
fi

cd $package-$version

packageName=$package
packageVersion=$version-$build

prefix=/software/$category/$packageName/$packageVersion

# Configure the source
echo "prefix= $prefix"

if test -f configure
then
	./configure --prefix=$prefix
fi

# Make it
if test -f Makefile
then
	make -j 4
elif test -f CMakeLists.txt
then
	mkdir self-build
	cd self-build
	cmake ..
	make -j 4
	cd ..
fi

# Install it
if test -f configure
then
	make install
else
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

template=$(dirname $BASH_SOURCE)/Module.txt
moduleFile=~/modulefiles/$category/$packageName/$packageVersion

cp $template $moduleFile
expression="s/CATEGORY/$category/g"
sed -i "$expression" $moduleFile
expression="s/PACKAGE_NAME/$packageName/g"
sed -i "$expression" $moduleFile
expression="s/PACKAGE_VERSION/$packageVersion/g"
sed -i "$expression" $moduleFile

# Fix permissions
chgrp clumeq -R $prefix
chmod g+w -R $prefix
