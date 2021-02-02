#!/usr/bin/env python
from django.template import Template, TemplateSyntaxError,TemplateDoesNotExist,Library
from django.conf import settings
from django.template.loader_tags import ExtendsNode,BlockNode
from django.template.loader import select_template,get_template

from .config import theme

register = Library() 

class ThemeExtendsNode(ExtendsNode):
    must_be_first = False
    def __init__(self, nodelist, parent_name, template_dirs=None):
        self.nodelist = nodelist
        self.parent_name = parent_name
        self.template_dirs = template_dirs
        self.blocks = {n.name: n for n in nodelist.get_nodes_by_type(BlockNode)}
        
    # def get_parent(self, context):
    #     if self.parent_name_expr:
    #         self.parent_name = self.parent_name_expr.resolve(context)
    #     parent = theme_template_url() +'/'+ self.parent_name        
    #     if not parent:
    #         error_msg = "Invalid template name in 'extends' tag: %r." % parent
    #         if self.parent_name_expr:
    #             error_msg += " Got this from the '%s' variable." % self.parent_name_expr.token
    #         raise TemplateSyntaxError, error_msg
    #     # try:
    #     #      source, origin = find_template_source(parent, self.template_dirs)
    #     # except TemplateDoesNotExist:
    #     #     raise TemplateSyntaxError, "Template %r cannot be extended, because it doesn't exist" % parent
    #     # else:
    #     #     return get_template_from_string(source, origin, parent)
    #     print get_template(parent)
    #     try:
    #         return get_template(parent)
    #     except TemplateDoesNotExist:
    #         raise TemplateSyntaxError, "Template %r cannot be extended, because it doesn't exist" % parent
    def find_template(self, template_name, context):
        """
        This is a wrapper around engine.find_template(). A history is kept in
        the render_context attribute between successive extends calls and
        passed as the skip argument. This enables extends to work recursively
        without extending the same template twice.
        """
        history = context.render_context.setdefault(
            self.context_key, [self.origin],
        )
        template_name =  theme_template_url() +'/'+ template_name  
        template, origin = context.template.engine.find_template(
            template_name, skip=history,
        )
        history.append(origin)
        return template
 
   

# def do_theme_extends(parser,token):
#     """
#     template based extends
#     """
#     bits = token.contents.split()
#     if len(bits) != 2:
#         raise TemplateSyntaxError, "'%s' takes one argument" % bits[0]
#     parent_name, parent_name_expr = None, None
#     if bits[1][0] in ('"', "'") and bits[1][-1] == bits[1][0]:
#         parent_name = bits[1][1:-1]
#     else:
#         parent_name_expr = parser.compile_filter(bits[1])
#     nodelist = parser.parse()    
#     if nodelist.get_nodes_by_type(ExtendsNode):
#         raise TemplateSyntaxError,"'%s' cannot appear more than once in the same template" % bits[0]
#     return ThemeExtendsNode(nodelist,parent_name,parent_name_expr)

def construct_relative_path(current_template_name, relative_name):
    """
    Convert a relative path (starting with './' or '../') to the full template
    name based on the current_template_name.
    """
    if not any(relative_name.startswith(x) for x in ["'./", "'../", '"./', '"../']):
        # relative_name is a variable or a literal that doesn't contain a
        # relative path.
        return relative_name

    new_name = posixpath.normpath(
        posixpath.join(
            posixpath.dirname(current_template_name.lstrip('/')),
            relative_name.strip('\'"')
        )
    )
    if new_name.startswith('../'):
        raise TemplateSyntaxError(
            "The relative path '%s' points outside the file hierarchy that "
            "template '%s' is in." % (relative_name, current_template_name)
        )
    if current_template_name.lstrip('/') == new_name:
        raise TemplateSyntaxError(
            "The relative path '%s' was translated to template name '%s', the "
            "same template in which the tag appears."
            % (relative_name, current_template_name)
        )
    return '"%s"' % new_name

@register.tag('theme_extends')
def do_theme_extends(parser, token):
    """
    Signal that this template extends a parent template.
    This tag may be used in two ways: ``{% extends "base" %}`` (with quotes)
    uses the literal value "base" as the name of the parent template to extend,
    or ``{% extends variable %}`` uses the value of ``variable`` as either the
    name of the parent template to extend (if it evaluates to a string) or as
    the parent template itself (if it evaluates to a Template object).
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes one argument" % bits[0])
    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    parent_name = parser.compile_filter(bits[1])
    nodelist = parser.parse()
    if nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError("'%s' cannot appear more than once in the same template" % bits[0])
    return ThemeExtendsNode(nodelist, parent_name)
#register.tag('theme_extends',do_theme_extends)

def get_theme_name():
    """
    get the theme name from settings.py
    """
    theme_name = theme()
    if theme_name:
        return theme_name
    else:
        return 'default'   

def media_url():
    """
    Returns the common media url
    """    
    return getattr(settings,'STATIC_URL','')
    
media_url = register.simple_tag(media_url)


def theme_media_url():
    """
    Returns the themes media url
    """   
    #print('theme:' + get_theme_name())
    return media_url() + 'themes/'+ get_theme_name()+'/'
    
register.simple_tag(theme_media_url)

def theme_template_url():
    """
    Returns the themes template url
    """
    url = 'themes/'+ get_theme_name()    
    return url