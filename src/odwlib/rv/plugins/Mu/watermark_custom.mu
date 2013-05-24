use glyph;
use gl;
use gltext;
use rvtypes;
use commands;

documentation: """
This is modify from an rvio overlay script. Overlay scripts are Mu modules which
contain a function called main() with specific arguments which rvio
will supply. This script is not used by rv.

Draws a water mark centered on the image. The script takes two
arguments: the string to render as a watermark and the opacity of the
watermark. The font size is determined by the bounding box of the
characters in the input string. So large strings are scaled down to
fit into the image.

----
  rvio inputImage -overlay watermark_custom "some text" 1 15 100 400 1 1 0 -o ouputImage
----

""";

module: watermark_custom
{
    documentation: "See module documentation.";

    \: main (void; int w, int h, 
             int tx, int ty,
             int tw, int th,
             bool stereo,
             bool rightEye,
             int frame,
             [string] argv)
    {
	let _ : text : op : textSize : posx : posy : colorR: colorG: colorB: _ = argv;

        setupProjection(w, h);

        glEnable(GL_LINE_SMOOTH);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

	//size
	gltext.size( int(textSize) );
	//color
        gltext.color(Color(float(colorR),float(colorG),float(colorB),float(op)));
        
        //position:screen left,screen bottom
        gltext.writeAt(int(posx), int(posy), text);

    }
}
