#!/usr/bin/perl

use Font::TTF::Font;

$f = Font::TTF::Font->open($ARGV[0]) || die "Can't open $ARGV[0]";
$p = $f->{'post'}->read;
for ($i = 0; $i < $f->{'maxp'}{'numGlyphs'}; $i++)
{
    if ($p->{'VAL'}[$i] =~ m/^glyph/o)
        { $p->{'VAL'}[$i] = ".notdef"; }
}

$f->out($ARGV[1])
