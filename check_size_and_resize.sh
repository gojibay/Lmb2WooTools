#!/bin/bash

# usage :
# ./check_size_and_resize.sh image_file_name
# example : 
# for i in * ; do if [ -f $i ] ; then echo $i ; ./check_size_and_resize.sh $i  ; fi; done

# initializations
size=2048 			# this is the size images will be resized to
filename=$1  		# get filename from first command line argument
target_dir='target'	# target directory resized images will be written to

# infos on images
width=`identify -format "%w"  $filename`
height=`identify -format "%h" $filename`


echo "#################"
echo "Widht : " $width
echo "Height : " $height

# mogrify overwrites input image file
# mogrify -verbose -resize "500<x500<" $i -gravity center  -background white -flatten ${target_dir}/$i  

echo "Resizing started..."
if [ $width -ge $size ]; then
	echo "Image width greater or equal than $size"
	if [ $height -ge $size ]; then
		echo "Image height greater or equal than $size"
		convert -verbose -resize "${size}x${size}" $filename -gravity center -crop ${size}x${size}+0+0\! -background white -flatten ${target_dir}/$filename
		identify ${target_dir}/$filename
	else
		echo "Image height lower than $size"
		convert -verbose -resize "${size}x${size}" $filename -gravity center -crop ${size}x${size}+0+0\! -background white -flatten ${target_dir}/$filename
                identify ${target_dir}/$filename

	fi

elif [ $width -lt $size ] ; then
	echo "Image width lower than $size"
	if [ $height -ge $size ]; then
		echo "Image height greater or equal than $size"
		convert -verbose -resize "${size}x${size}" $filename -gravity center -crop ${size}x${size}+0+0\! -background white -flatten ${target_dir}/$filename
                identify ${target_dir}/$filename

        else
		echo "Image height lower than $size"
		convert -verbose -resize "${size}x${size}" $filename -gravity center -crop ${size}x${size}+0+0\! -background white -flatten  ${target_dir}/$filename
                identify ${target_dir}/$filename

        fi
echo "...resizing done."
echo ""

fi

