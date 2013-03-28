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


# Download the tarball
distribution=$(basename $Source0)

mock=$Name-$Version-$Release-Sandbox

if test -f $distribution
then
	echo "" &> /dev/null
else
	echo "[Packager] Downloading $Source0"
	wget $Source0 -O $distribution
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

for i in $Patch0
do
	patch -p1 < ../../$i
done

prefix=/software/$Group/$Name/$Version-$Release

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
mkdir -p ~/modulefiles/$Group/$Name

moduleFile=~/modulefiles/$Group/$Name/$Version-$Release

cp $template $moduleFile

expression="s%__Requires__%module load $Requires%g"
sed -i "$expression" $moduleFile
expression="s/__Group__/$Group/g"
sed -i "$expression" $moduleFile
expression="s/__Name__/$Name/g"
sed -i "$expression" $moduleFile
expression="s/__Version__/$Version/g"
sed -i "$expression" $moduleFile
expression="s/__Release__/$Release/g"
sed -i "$expression" $moduleFile
expression="s/__Summary__/$Summary/g"
sed -i "$expression" $moduleFile
expression="s%__URL__%$URL%g"
sed -i "$expression" $moduleFile

# Fix permissions
chgrp clumeq -R $prefix
chmod g+w -R $prefix
chgrp clumeq -R $moduleFile

