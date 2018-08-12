# Tiling

This project was inspired by some of [Asao Tokolo's](http://tokolo.com/) tiling designs.
I first learned aobut Tokolo when his design was selected for the 2020 Olympics in Tokto.
You can read about that design, his tiles, and other works
[here](http://www.spoon-tamago.com/2016/04/26/who-is-asao-tokolo-the-designer-behind-tokyos-2020-olympic-emblem/).

The goal was to create an image feed of interlocking tiles that would update automatically.
You can visit the tile set here: [random-tiles.tumblr.com](https://random-tiles.tumblr.com/).
(I originally imagined the project would live on Instagram, but they have no API to post images.)

The project works by defining three object types:

- Tiles, which each have one foreground and one background colour, and any number of ellipse segments.
- Quilts, arrays of Tiles such that the edges of the Tiles match up. (Also potentially with edge constraints.) These are individual images in the feed.
- QuiltSequence, which ensures that neighbouring Quilts have matching edge constraints. The blog is built of a single, evolving QuiltSequence.
