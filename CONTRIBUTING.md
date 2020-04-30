<img src="images/gallery_shot.png" >

# Contributing

## What makes a good tutorial?


## Adding a tutorial


## Setting gallery thumbnails

To set the gallery thumbnail for a given tutorial (as seen in the image above) one needs to set a cell tag in the notebook for a cell that generates an image as its output.  To make the tabs visible do:

<img src="images/menu_tags.png" width="50%" >

The cell's whos output you would like to use, you must add the tag: `nbsphinx-thumbnail`.
<img src="images/set_tag.png" >

If a tag is not set, then the Qiskit logo is used as a placeholder.