# iswa_graphite.py is a python script to create a International SignWriting
# Alphabet Graphite font by importing svg glyphs. It reads a list of unicode
# points from standard input (one code, hexadecimal without the 0x prefix)
# 
# it then creates the font and the Graphite Description Language (GDL) to
# be compiled and added to the font, for the ISWA text to show properly
# 
# Copyright (c) 2012 Eduardo Trapani <etrapani@gmail.com>
#
# License:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import fontforge
import os

def iswa_rotation(x):
	return x >= 0xFD820 and x <= 0xFD82F

def iswa_fill(x):
	return x >= 0xFD810 and x <= 0xFD815

def iswa_structural(x):
	return x >= 0xFD800 and x <= 0xFD804

def iswa_symbol(x):
	return x >= 0xFD830 and x <= 0xFDABB

def iswa_number(x):
	return x >= 0xFDE06 and x <= 0xFDFF9

def iswa_unicode(x):
	return x >= 0xFD800 and x <= 0xFDFF9

def rules_fill_rotation():
	rules = ""
	for fill in range(0,6):
		for rotation in range(0,16):
			rules = rules + ("clsFill%d clsRotation%d > unicode(0x%X):(1 2) _;\n" % (fill + 1,rotation + 1,FILL_ROTATION + fill * 16 + rotation))
	return rules

def rules_ranges_aux(cls_ranges):
	rules = ""
	for i in cls_ranges:
		rules = rules + "clsRange%X clsAux > clsRange%X$2:(1 2)  _;\n" % (i,i)
	return rules

def gdl_class(myClasses):
	# this function expects a list with a dictionary in each entry, holding the name of the class,
	# the elements and an optional attribute-setting string
	gdl = ""
	for i in myClasses:
		name = myClasses[i]['name']
		elements = ""

		for k in myClasses[i]['elements']:
			if len(elements) - elements.rfind("\n") > 80:
				elements = elements + ");\n%s += unicode(" % name
			elements = elements + ("0x%X " % (k))
			
		attributes = myClasses[i]["attributes"] if "attributes" in (myClasses[i]) else ""

		gdl = gdl + "%s = unicode(%s) %s;\n" % (name,elements,attributes)
	return gdl

def new_glyph(f,u,p):
	new_glyph.counter += 1

#	if new_glyph.stop : return 0

#	if new_glyph.counter > int(sys.argv[1]) and iswa_symbol(u):
#		print "No more glyphs"
#	 	new_glyph.stop = True
#		return 0

	print "New glyph[%d] %x ...(%s)" % (new_glyph.counter,u,p)
	char = f.createChar(u)
	char.importOutlines(p)
	char.left_side_bearing = 5
	char.right_side_bearing = 5
	#	char.removeOverlap()
	char.autoInstr()
	#print "Loaded! (%s)" % p
	return char

processed = dict()

cls_center = dict()
cls_center[0] = dict()
cls_center[0]['name'] = 'clsCenter'
cls_center[0]['elements'] = []

cls_symbol = []
cls_realSymbol = []
cls_individual = dict()
SYMBOLS_BASE = 0xD0000
FILL_ROTATION = 0xEFFA0

if len(sys.argv) > 1:
	svg_base = sys.argv[1]
else:
	svg_base = "./"

# Create font
font = fontforge.font()
font.descent = 15
font.ascent = 15
font.em = 30
font.fontname = "SignWriting_ISWA_2010"
font.familyname = "SignWriting_ISWA_2010"
font.fondname = "SignWriting_ISWA_2010"
font.fullname = "SignWriting ISWA 2010"
font.createChar(0, ".notdef")

new_glyph.counter = 0
new_glyph.stop = False

svg_placeholder_name = "placeholder.svg"

# Create glyphs for helper class (numbers)
for codigo in range(FILL_ROTATION,FILL_ROTATION + 0x60):
#	new_glyph(font,codigo,svg_base + "/34a/34a10.svg")
	new_glyph(font,codigo,svg_base + svg_placeholder_name)

# Create glyphs for numbers
for codigo in range(0xFDE06,0xFDFF9 + 1):
#	new_glyph(font,codigo,svg_base + "/34a/34a10.svg")
	new_glyph(font,codigo,svg_base + svg_placeholder_name)

# Create glyphs for fills
for codigo in range(0xFD810,0xFD815 + 1):
#	new_glyph(font,codigo,svg_base + "/2fa/2fa00.svg")
	new_glyph(font,codigo,svg_base + svg_placeholder_name)

# Create glyphs for rotations
for codigo in range(0xFD820,0xFD82F + 1):
#	new_glyph(font,codigo,svg_base + "/2fa/2fa20.svg")
	new_glyph(font,codigo,svg_base + svg_placeholder_name)

for line in sys.stdin:
	codigo = int(line,16)

	# Ignore the stuff outside of ISWA (plane 15)
	if not iswa_unicode(codigo) : continue

	print "Processing %x" % (codigo)
	# Get the svg file to import
	if iswa_structural(codigo):
		# svg_name = "2fb/2fb05.svg"
		cls_center[0]['elements'].append(codigo)

		# Remember the code
		processed[codigo] = True

		# create glyph
		new_glyph(font,codigo,svg_base + svg_placeholder_name)

#	elif iswa_fill(codigo):
#		svg_name = "2fa/2fa00.svg"
#	elif iswa_rotation(codigo):
#		svg_name = "2fa/2fa20.svg"
#	elif iswa_number(codigo):
#		svg_name = "34a/34a10.svg"
	elif iswa_symbol(codigo):
		base_symbol = codigo - 0xFD730
		svg_name = "%x/%x%s.svg" % (base_symbol, base_symbol, ("10" if base_symbol in [0x14d,0x14f,0x151,0x15c,0x15e,0x1f6,0x204] else "00"))

		# create glyph
		c = new_glyph(font,codigo,svg_base + svg_name)

		if c != 0:
			cls_symbol.append(codigo)
			fake_unicode = SYMBOLS_BASE + (base_symbol - 0x100) * 96
			cls_realSymbol.append(fake_unicode)
			cls_individual[fake_unicode] = dict()
			cls_individual[fake_unicode]['name'] = "clsRange%X" % fake_unicode
			cls_individual[fake_unicode]['elements'] = range(fake_unicode,fake_unicode + 96)

			# Remember the code
			processed[codigo] = True

			# Create the fill/rotate variations
			for fill in range(0,6):
				for rotation in range(0,16):
					fake_unicode = SYMBOLS_BASE + (base_symbol - 0x100) * 96 + fill * 16 + rotation
					svg_full_name = "%s/%x/%x%x%x.svg" % (svg_base,base_symbol,base_symbol,fill,rotation)

					if not os.path.exists(svg_full_name) : svg_full_name = svg_base + svg_placeholder_name # "/100/10000.svg"

					print "Base: %x Fill: %x Rotation: %x -> Fake: %x (%s)" % (base_symbol,fill,rotation,fake_unicode,svg_full_name)

					#print "----------------------(pre %s)" % svg_full_name

					new_glyph(font,fake_unicode,svg_full_name)

					#print "----------------------(post %s)" % svg_full_name
		else:
			print "Skipping %X" % (codigo)

font.generate("iswa.ttf")

# Build XY classes
clsXY = dict()
for i in range(0xFDE06,0xFDFF9 + 1):
	clsXY[i] = dict()
	clsXY[i]['name'] = "clsXY_%d" % (i - 0xFDE06)
	clsXY[i]['elements'] = [i]
	coordinate = ((i - 0xFDE06) - 249) * 35 
	clsXY[i]['attributes'] = "{myPos=point(%dm,%dm)}" % (coordinate,coordinate * -1)

# Build number classes
cls_numbers = dict()
cls_numbers[0] = dict()
cls_numbers[0]['name'] = "clsNumbers"
cls_numbers[0]['elements'] = range(0xFDE06,0xFDFF9 + 1)

# Build fill classes
clsFill = dict()
for i in range(0xFD810,0xFD815 + 1):
	clsFill[i] = dict()
	clsFill[i]['name'] = "clsFill%d" % (i - 0xFD810 + 1)
	clsFill[i]['elements'] = [i]

# Build rotation classes
clsRotation = dict()
for i in range(0xFD820,0xFD82F + 1):
	clsRotation[i] = dict()
	clsRotation[i]['name'] = "clsRotation%d" % (i - 0xFD820 + 1)
	clsRotation[i]['elements'] = [i]

# Build symbol classes
cls_symbol_dict = dict()
cls_symbol_dict[0] = dict()
cls_symbol_dict[0]['name'] = "clsSymbol"
cls_symbol_dict[0]['elements'] = cls_symbol

cls_real_symbol_dict = dict()
cls_real_symbol_dict[0] = dict()
cls_real_symbol_dict[0]['name'] = "clsRealSymbol"
cls_real_symbol_dict[0]['elements'] = cls_realSymbol

cls_all_real_symbols = dict()
cls_all_real_symbols[0] = dict()
cls_all_real_symbols[0]['name'] = "clsAllSymbols"
cls_all_real_symbols[0]['elements'] = []
for i in cls_individual:
	cls_all_real_symbols[0]['elements'] =	cls_all_real_symbols[0]['elements'] + cls_individual[i]['elements']

# Build helper class
cls_helper = dict()
cls_helper[0] = dict()
cls_helper[0]['name'] = "clsAux"
cls_helper[0]['elements'] = range(FILL_ROTATION,FILL_ROTATION + 0x60)

# Now let's generate the gdl document

gdl="""
#include "stddef.gdh"

Bidi = false;
AutoPseudo = 0;
ExtraAscent = 1000m;
ExtraDescent = 1000m;

table(feature)
attach_to_structural.id = 1001;
attach_to_structural.default = 0;
endtable;

table(glyph)
{individualClasses}
{numbers}
{centerClass}
{XYClasses}
{symbol}
{realSymbol}
{fills}
{rotations}
{aux}
endtable;

table(sub)
pass(1)
{fill_rotation}
clsCenter clsNumbers clsNumbers > @1:(1 2) _ _;
endpass;

pass(2)
	clsSymbol > clsRealSymbol;
endpass;

pass(3)
        ANY clsAux clsNumbers clsNumbers > @1 {{user1 = @3.myPos.x;user2 = @4.myPos.y;user3 = 1}} @2 _ _;
endpass;

pass(4)
{ranges_aux}
endpass;

endtable;

table(pos)

pass(1)
	if (attach_to_structural == 0)
		// this allows for matching a sign with an arbitrarily length.  The individual symbols
		// are chained

		clsCenter ANY {{attach {{to=@1; at=point(@2.user1 + 0m,@2.user2 + 0m); with=point(0m,0m)}}}} / _ ^ _ {{@2.user3 > 0}};
		ANY ANY {{attach {{to=@1; at=point(@2.user1 + 0m - @1.user1,@2.user2 + 0m - @1.user2); with=point(0m,0m)}}}} / _ ^ _ {{@1.user3 * @2.user3 > 0}};

	else if (attach_to_structural == 1)

		// this was the original solution, all symbols are attached to the center symbol

		clsCenter ANY {{attach {{to=@1; at=point(@2.user1 + 0m,@2.user2 + 0m); with=point(0m,0m);level = 1}}}};
	endif;
endpass;
 
//pass(2)
//	if (attach_to_structural == 1)
//		clsCenter ANY {{attach {{to=@1; at=point(@3.user1 + 0m,@3.user2 + 0m); with=point(0m,0m);level = 1}}}} /  _ ANY  _ {{@2.user3 * @3.user3 > 0}};
//	endif;
//endpass;

//pass(3)
//	if (attach_to_structural == 1)
//		clsCenter ANY {{attach {{to=@1; at=point(@4.user1 + 0m,@4.user2 + 0m); with=point(0m,0m);level = 1}}}} /  _ ANY  ANY _ {{@2.user3 * @3.user3 * @4.user3 > 0}};
//	endif;
//endpass;

//pass(4)
//	if (attach_to_structural == 1)
//		clsCenter ANY {{attach {{to=@1; at=point(@5.user1 + 0m,@5.user2 + 0m); with=point(0m,0m);level = 1}}}} /  _ ANY ANY ANY _{{@2.user3 * @3.user3 * @4.user3 * @5.user3 > 0}};
//	endif;
//endpass;

//pass(5)
//	if (attach_to_structural == 1)
//		clsCenter ANY {{attach {{to=@1; at=point(@6.user1 + 0m,@6.user2 + 0m); with=point(0m,0m);level = 1}}}} /  _ ANY ANY ANY ANY _ {{@2.user3 * @3.user3 * @4.user3 * @5.user3 * @6.user3 > 0}};
//	endif;
//endpass;

//pass(6)
//	if (attach_to_structural == 1)
//		clsCenter ANY {{attach {{to=@1; at=point(@7.user1 + 0m,@7.user2 + 0m); with=point(0m,0m);level = 1}}}} /  _ ANY ANY ANY ANY ANY _ {{@2.user3 * @3.user3 * @4.user3 * @5.user3 * @6.user3 * @7.user3 > 0}};
//	endif;
//endpass;

//pass(7)
//	if (attach_to_structural == 1)
//		clsCenter ANY {{attach {{to=@1; at=point(@8.user1 + 0m,@8.user2 + 0m); with=point(0m,0m);level = 1}}}} /  _ ANY ANY ANY ANY ANY ANY _ {{@2.user3 * @3.user3 * @4.user3 * @5.user3 * @6.user3 * @7.user3 * @8.user3 > 0}};
//	endif;
//endpass;

endtable;
"""

f = open("iswa.gdl","w")
f.write( gdl.format(individualClasses=gdl_class(cls_individual),
numbers=gdl_class(cls_numbers),
centerClass=gdl_class(cls_center),XYClasses=gdl_class(clsXY),
symbol=gdl_class(cls_symbol_dict),realSymbol=gdl_class(cls_real_symbol_dict),
fills=gdl_class(clsFill),rotations=gdl_class(clsRotation),
aux=gdl_class(cls_helper),

fill_rotation=rules_fill_rotation(),ranges_aux=rules_ranges_aux(cls_individual)
))
f.close()
