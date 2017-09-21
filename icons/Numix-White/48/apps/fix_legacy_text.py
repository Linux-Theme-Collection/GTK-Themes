#!/usr/bin/env python
"""
fix_legacy_text - Fix text baseline spacing in legacy documents

Copyright (C) 2016 su_v <suv-sf@users.sf.net>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
# standard library
import re

# local library
import inkex
import simplestyle


__version__ = '0.3'


# globals
LINEHEIGHT_ZERO = '0%'
LINEHEIGHT_DEFAULT = '125%'
FONTSIZE_ZERO = '0px'
FONTSIZE_DEFAULT = '12px'
FONTFAMILY_DEFAULT = 'sans-serif'
FONTFAMILY_GENERIC = {
    'Sans': 'sans-serif',
    'Serif': 'serif',
    'Monospace': 'monospace',
}
BLANK_LINE = u'\u00A0'    # workaround: non-breaking space
BLANK_DEBUG = u'\u2588'  # workaround: full block


def formatted(f, precision=8):
    """Pretty-printer for floats, return formatted string."""
    # pylint: disable=invalid-name
    fstring = '.{0}f'.format(precision)
    return format(f, fstring).rstrip('0').rstrip('.')


def parse_length(val):
    """Parse length into list of float (value) and string (unit)."""
    value = 0.0
    unit = ''
    skip = ['normal', 'inherit']  # CSS line-height values
    if isinstance(val, str) and val not in skip:
        params = re.compile(
            r'(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)(.*$)')
        split_match = params.match(val)
        if split_match:
            split_vals = split_match.groups()
            if len(split_vals):
                value = float(split_vals[0])
            if len(split_vals) > 1:
                unit = split_vals[-1].strip()
    return [value, unit]


def max_length(length1, length2):
    """Compare length values, return max length of two."""
    # FIXME: compare lengths in same base unit
    val1 = length1[0] or 0
    val2 = length2[0] or 0
    return length1 if val1 >= val2 else length2


def min_length(length1, length2):
    """Compare length values, return min length of two."""
    # FIXME: compare lengths in same base unit
    val1 = length1[0] or 0
    val2 = length2[0] or 0
    return length1 if val1 <= val2 else length2


def eq_length(length1, length2):
    """Compare length values for equaliy."""
    # FIXME: test lengths for nearness in same base unit
    val1 = length1[0] or 0
    val2 = length2[0] or 0
    return True if val1 == val2 else False


def print_length(alist):
    """Return length string."""
    return '{}{}'.format(*alist)


def is_text(node):
    """Check whether node is <text> or <flowRoot> type."""
    return (node.tag == inkex.addNS('text', 'svg') or
            node.tag == inkex.addNS('flowRoot', 'svg'))


def is_tspan(node):
    """Check whether node is <tspan> type."""
    return node.tag == inkex.addNS('tspan', 'svg')


def is_line(node):
    """Check whether node has 'sodipodi:role' set to 'line'."""
    return node.get(inkex.addNS('role', 'sodipodi')) == 'line'


def is_flowroot(node):
    """Check whether node is <flowRoot> type."""
    return node.tag == inkex.addNS('flowRoot', 'svg')


def is_flowspan(node):
    """Check whether node is <flowSpan> type."""
    return node.tag == inkex.addNS('flowSpan', 'svg')


def is_flowpara(node):
    """Check whether node is <flowPara> type."""
    return node.tag == inkex.addNS('flowPara', 'svg')


def is_flowdiv(node):
    """Check whether node is <flowDiv> type."""
    return node.tag == inkex.addNS('flowDiv', 'svg')


def set_attr(node, prop, val):
    """Set presentation attribute on node."""
    node.set(prop, val)


def update_attr(node, prop, val):
    """Update presentation attribute on node."""
    if prop in node.attrib:
        node.set(prop, val)


def del_attr(node, prop):
    """Delete attribute from node."""
    if prop in node.attrib:
        return node.attrib.pop(prop)


def set_prop(node, prop, val):
    """Set style property on node."""
    sdict = simplestyle.parseStyle(node.get('style'))
    sdict[prop] = val
    node.set('style', simplestyle.formatStyle(sdict))


def update_prop(node, prop, val):
    """Update attribute and style property to val."""
    update_attr(node, prop, val)
    set_prop(node, prop, val)


def get_prop(node, prop):
    """Get attribute or style property from node."""
    val = None
    if prop in node.attrib:
        val = node.get(prop)
    sdict = simplestyle.parseStyle(node.get('style'))
    if prop in sdict:
        val = sdict[prop]
    return val


def del_prop(node, prop):
    """Delete attribute or style property from node."""
    if prop in node.attrib:
        del node.attrib[prop]
    pdict = simplestyle.parseStyle(node.get('style'))
    if prop in pdict:
        del pdict[prop]
        node.set('style', simplestyle.formatStyle(pdict))


def get_max_length_prop(node, prop):
    """Get max prop with length value of node and descendants."""
    result = [None, '']
    if node.text or any(child.tail for child in node.iterchildren()):
        val = get_prop(node, prop)
        if val is not None:
            result = parse_length(val)
    for child in node.iterchildren(tag=inkex.etree.Element):
        result = max_length(result, get_max_length_prop(child, prop))
    return result


def get_min_length_prop(node, prop):
    """Get min prop with length value of node and descendants."""
    result = [None, '']
    if node.text or any(child.tail for child in node.iterchildren()):
        val = get_prop(node, prop)
        if val is not None:
            result = parse_length(val)
    for child in node.iterchildren(tag=inkex.etree.Element):
        result = min_length(result, get_min_length_prop(child, prop))
    return result


def textify(node):
    """Return all text content within node."""
    return inkex.etree.tostring(
        node, encoding='unicode', method="text", with_tail=True)


def is_blank(node):
    """Check whether node and descendents have no text content."""
    # inkex.errormsg(textify(node).strip())
    return not textify(node).strip()


def set_blank(node, fontsize, lineheight, debug=False):
    """Replace blank line with placeholder character, update props."""
    cdict = simplestyle.parseStyle(node.get('style'))
    node.text = BLANK_LINE if not debug else BLANK_DEBUG
    if fontsize is not None:
        cdict['font-size'] = fontsize
        node.set('style', simplestyle.formatStyle(cdict))
    if lineheight is not None:
        cdict['line-height'] = lineheight
        node.set('style', simplestyle.formatStyle(cdict))


def css_strut(node):
    """Return value of CSS 'strut'.

    The minimum height consists of a minimum height above the baseline
    and a minimum depth below it, exactly as if each line box starts
    with a zero-width inline box with the element's font and line height
    properties.  We call that imaginary box a "strut."
    ref: https://www.w3.org/TR/CSS22/visudet.html#strut
    """
    lineheight = get_prop(node, 'line-height') or '1.25'  # LINEHEIGHT_DEFAULT
    fontsize = get_prop(node, 'font-size') or FONTSIZE_DEFAULT
    fontfamily = get_prop(node, 'font-family') or FONTFAMILY_DEFAULT
    return {
        'line-height': lineheight,
        'font-size': fontsize,
        'font-family': fontfamily,
    }


def get_max_line_height(node, strut):
    """Parse node and descendants for max height (CSS line box)."""
    fs_length = get_max_length_prop(node, 'font-size')
    if fs_length[0] is not None:
        fontsize = print_length(fs_length)
    else:
        fontsize = strut['font-size']
    # FIXME: support unitless line-height values (1.0 vs 100%)
    lh_length = get_max_length_prop(node, 'line-height')
    if lh_length[0] is not None:
        lineheight = print_length(lh_length)
    else:
        lineheight = strut['line-height']
    return fontsize, lineheight


def get_min_line_height(node, strut):
    """Parse node and descendants for min height (CSS line box)."""
    fs_length = get_max_length_prop(node, 'font-size')
    if fs_length[0] is not None:
        fontsize = print_length(fs_length)
    else:
        fontsize = strut['font-size']
    # FIXME: support unitless line-height values (1.0 vs 100%)
    lh_length = get_min_length_prop(node, 'line-height')
    if lh_length[0] is not None:
        lineheight = print_length(lh_length)
    else:
        lineheight = strut['line-height']
    return fontsize, lineheight


def fix_line_spacing(node, lineheight_zero=LINEHEIGHT_ZERO):
    """Fix line spacing (copy to inner, zero on outer style)."""
    prop = 'line-height'
    lineheight = css_strut(node)[prop]
    # inner style
    inner = False
    for child in node.iterdescendants(tag=inkex.etree.Element):
        cdict = simplestyle.parseStyle(child.get('style'))
        if is_tspan(child) and is_line(child):
            inner = True
            # regular text
            if prop not in cdict:
                cdict[prop] = lineheight
                child.set('style', simplestyle.formatStyle(cdict))
        elif is_flowpara(child) or is_flowdiv(child):
            inner = True
            # flowed text
            if prop not in cdict:
                cdict[prop] = lineheight
                child.set('style', simplestyle.formatStyle(cdict))
    # outer style
    if inner:
        # inkex.debug(lineheight_zero)
        if is_flowroot(node):
            # val = '0.01%'  # workaround for some fonts in flowed text
            val = lineheight_zero
        else:
            val = lineheight_zero
        update_prop(node, prop, val)


def fix_font_size(node, mode='unset'):
    """Fix font size (copy to inner, unset for outer style)."""
    prop = 'font-size'
    fontsize = css_strut(node)[prop]
    # inner style
    inner = False
    for child in node.iterdescendants(tag=inkex.etree.Element):
        cdict = simplestyle.parseStyle(child.get('style'))
        if is_tspan(child) and is_line(child):
            # regular text
            inner = True
            if prop not in cdict and fontsize is not None:
                cdict[prop] = fontsize
                child.set('style', simplestyle.formatStyle(cdict))
        elif is_flowpara(child) or is_flowdiv(child):
            # flowed text
            inner = True
            if prop not in cdict and fontsize is not None:
                cdict[prop] = fontsize
                child.set('style', simplestyle.formatStyle(cdict))
    # outer style
    if inner:
        # unset font-size
        if mode == 'unset':
            del_prop(node, prop)
        elif mode == 'zero':
            if is_flowroot(node):
                val = FONTSIZE_ZERO
            else:
                val = FONTSIZE_ZERO
            update_prop(node, prop, val)
        else:
            pass


def fix_blank_line(node, debug=False):
    """Fix blank lines (insert space, copy font-size from prior line)."""
    strut = css_strut(node)
    fontsize = strut['font-size']
    lineheight = strut['line-height']
    # inner style
    for child in node.iterchildren(tag=inkex.etree.Element):
        if is_tspan(child) and is_line(child):
            # regular text
            if is_blank(child):
                # add placeholder character, set props from prior line
                set_blank(child, fontsize, lineheight, debug)
            else:
                # store properties contributing to current CSS line box
                fontsize, lineheight = get_max_line_height(child, strut)
        elif is_flowpara(child) or is_flowdiv(child):
            # flowed text
            if is_blank(child):
                # add placeholder character, set props from prior line
                set_blank(child, fontsize, lineheight, debug)
            else:
                # store properties contributing to current CSS line box
                fontsize, lineheight = get_max_line_height(child, strut)


def fix_font_name(node, debug=False):
    """Fix generic font names (sans-serif, serif, monospace)."""
    prop = 'font-family'
    ink_prop = '-inkscape-font-specification'
    # inner style
    for child in node.iterchildren(tag=inkex.etree.Element):
        fix_font_name(child, debug)
    # outer style
    if prop in node.attrib:
        name = node.get(prop)
        if name in FONTFAMILY_GENERIC:
            node.set(prop, FONTFAMILY_GENERIC[name])
    pdict = simplestyle.parseStyle(node.get('style'))
    if prop in pdict:
        name = pdict[prop]
        if name in FONTFAMILY_GENERIC:
            pdict[prop] = FONTFAMILY_GENERIC[name]
            node.set('style', simplestyle.formatStyle(pdict))
    if ink_prop in pdict:
        if debug:
            inkex.debug(pdict[ink_prop])
        ink_val = pdict[ink_prop].strip("'").split()
        name = ink_val[0]
        if name in FONTFAMILY_GENERIC:
            if len(ink_val) > 1:
                ink_val[0] = FONTFAMILY_GENERIC[name]
                pdict[ink_prop] = "'" + ' '.join(ink_val) + "'"
            elif len(ink_val):
                pdict[ink_prop] = FONTFAMILY_GENERIC[name]
            node.set('style', simplestyle.formatStyle(pdict))


def fix_plain_text(node, debug=False):
    """Fix plain text by adding sodipodi:role="line" to tspans."""
    if not is_flowroot(node):
        prop = inkex.addNS('role', 'sodipodi')
        val = 'line'
        for child in node.iterchildren(tag=inkex.etree.Element):
            if is_tspan(child) and not is_line(child):
                set_attr(child, prop, val)
                if debug:
                    # inkex.debug('--- fix_plain_text:')
                    inkex.errormsg(textify(child))
                if debug == 'reset':
                    hpos = child.get('x')
                    vpos = del_attr(child, 'y')
                    inkex.debug('{}: '.format(child.get('id')) +
                                'x="{}" '.format(hpos) +
                                'y="{}"'.format(vpos))


def fix_split_text(node, debug=False):
    """Split text into lines preserving x,y position."""
    if not is_flowroot(node) and len(node) > 1:
        lines = inkex.etree.Element(inkex.addNS('g', 'svg'))
        for attr in ['id', 'transform']:
            if attr in node.attrib:
                set_attr(lines, attr, node.get(attr))
        for child in node.iterchildren(tag=inkex.etree.Element):
            if is_tspan(child) and is_line(child):
                if debug:
                    # inkex.debug('--- fix_split_text:')
                    inkex.errormsg(textify(child))
                line = inkex.etree.Element(inkex.addNS('text', 'svg'))
                for prop in node.attrib:
                    set_attr(line, prop, node.get(prop))
                for attr in ['id', 'transform']:
                    del_attr(line, attr)
                for coord in ['x', 'y']:
                    if coord in child.attrib:
                        set_attr(line, coord, child.get(coord))
                line.append(child)
                lines.append(line)
        if len(lines):
            index = node.getparent().index(node)
            node.getparent().insert(index+1, lines)
            node.getparent().remove(node)


class LegacyText(inkex.Effect):
    """Fix text layout in legacy documents."""

    def __init__(self):
        """Set options and instance attributes for LegacyText()."""
        inkex.Effect.__init__(self)
        # options
        self.OptionParser.add_option("--fix_line_spacing",
                                     action="store", type="inkbool",
                                     dest="fix_line_spacing", default=True,
                                     help="Fix line spacing")
        self.OptionParser.add_option("--fix_font_size",
                                     action="store", type="inkbool",
                                     dest="fix_font_size", default=False,
                                     help="Fix font size")
        self.OptionParser.add_option("--fix_blank_line",
                                     action="store", type="inkbool",
                                     dest="fix_blank_line", default=True,
                                     help="Fix blank lines")
        self.OptionParser.add_option("--fix_font_name",
                                     action="store", type="inkbool",
                                     dest="fix_font_name", default=True,
                                     help="Fix generic font names")
        self.OptionParser.add_option("--fix_plain_text",
                                     action="store", type="inkbool",
                                     dest="fix_plain_text", default=False,
                                     help="Make plain text editable")
        self.OptionParser.add_option("--fix_split_text",
                                     action="store", type="inkbool",
                                     dest="fix_split_text", default=False,
                                     help="Split text into lines")
        # debug
        self.OptionParser.add_option("--min_lh_divisor",
                                     action="store", type="int",
                                     dest="min_lh_divisor", default=100,
                                     help="Divisor for minimal line-height")
        self.OptionParser.add_option("--fontsize_reset",
                                     action="store", type="string",
                                     dest="fontsize_reset", default="unset",
                                     help="Reset font-size of outer style")
        self.OptionParser.add_option("--verbose",
                                     action="store", type="inkbool",
                                     dest="verbose", default=False,
                                     help="Verbose output (svg source)")
        self.OptionParser.add_option("--debug",
                                     action="store", type="inkbool",
                                     dest="debug", default=False,
                                     help="Visual debug aids")
        # tabs
        self.OptionParser.add_option("--tab",
                                     action="store", type="string",
                                     dest="tab", help="Active tab")

    def process_items(self, node):
        """Recursively process node and its children."""
        debug = self.options.debug
        if is_text(node):
            if self.options.fix_plain_text:
                fix_plain_text(node, debug)
            if self.options.fix_blank_line:
                fix_blank_line(node, debug)
            if self.options.fix_line_spacing:
                if self.options.min_lh_divisor > 0:
                    min_height = formatted(1.0/self.options.min_lh_divisor)
                    min_height += '%'
                else:
                    min_height = LINEHEIGHT_ZERO
                fix_line_spacing(node, min_height)
            if self.options.fix_font_size:
                fix_font_size(node, mode=self.options.fontsize_reset)
            if self.options.fix_font_name:
                fix_font_name(node, debug)
            if self.options.fix_split_text:
                fix_split_text(node, debug)
        else:
            for child in node:
                self.process_items(child)

    def effect(self):
        """Fix text layout in regular and flowed text elements."""
        items = self.selected.values() or self.document.getroot()
        for node in items:
            self.process_items(node)
        if self.options.verbose:
            inkex.debug(inkex.etree.tostring(self.document))


if __name__ == '__main__':
    ME = LegacyText()
    ME.affect()

# vim: et shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=79
