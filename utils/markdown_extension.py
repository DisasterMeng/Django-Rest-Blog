from utils.uuid import uuid

from markdown import util as md_util
from markdown.blockparser import BlockParser
from markdown.blockprocessors import CodeBlockProcessor
from pymdownx.highlight import Highlight, HighlightExtension

CODE_WRAP = \
    '<pre%s><code%s>%s</code>%s</pre>'
ID_ATTR = ' id="%s"'
CLASS_ATTR = ' class="%s"'
DATA_ATTR = ' data-lang="%s"'
COPY_WRAP = \
    '<a class="copy-code" href="javascript:void(0);" data-clipboard-target="%s" title="拷贝代码">' \
    '<i class="fa fa-clipboard"></i></a>'


class ChangeCodeBlockProcessor(CodeBlockProcessor):

    def __init__(self, *args, **kwargs):
        super(ChangeCodeBlockProcessor, self).__init__(*args, **kwargs)

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        theRest = ''
        if (sibling is not None and sibling.tag == "pre" and
           len(sibling) and sibling[0].tag == "code"):
            # The previous block was a code block. As blank lines do not start
            # new code blocks, append this block to the previous, adding back
            # linebreaks removed from the split into a list.
            code = sibling[0]
            block, theRest = self.detab(block)
            code.text = md_util.AtomicString(
                '%s\n%s\n' % (code.text, md_util.code_escape(block.rstrip()))
            )
        else:
            # This is a new codeblock. Create the elements and insert text.
            code_id = 'code-%s' % uuid(block)
            pre = md_util.etree.SubElement(parent, 'pre')
            code = md_util.etree.SubElement(pre, 'code')
            a = md_util.etree.XML(COPY_WRAP % ('#%s' % code_id))
            pre.append(a)
            block, theRest = self.detab(block)
            code.attrib = {'id': code_id, 'data-lang': 'TEXT'}
            code.text = md_util.AtomicString('%s\n' % md_util.code_escape(block.rstrip()))
        if theRest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, theRest)


class ChangeCodeHighlight(Highlight):

    def __init__(self, *args, **kwargs):
        super(ChangeCodeHighlight, self).__init__(*args, **kwargs)

    def highlight(
            self, src, language, css_class='highlight', hl_lines=None,
            linestart=-1, linestep=-1, linespecial=-1, inline=False
    ):
        """Highlight code."""
        code_id = 'code-%s' % uuid(src)
        id_str = ID_ATTR % code_id
        if inline:
            # Format inline code for a JavaScript Syntax Highlighter by specifying language.
            code = self.escape(src)
            classes = [css_class] if css_class else []
            if language:
                data_str = DATA_ATTR % language.upper()
                classes.append('language-%s' % language)
            else:
                data_str = DATA_ATTR % 'TEXT'
            class_str = id_str
            if len(classes):
                class_str += ' '.join(classes)
            if data_str:
                class_str += data_str
        else:
            # Format block code for a JavaScript Syntax Highlighter by specifying language.
            classes = []
            linenums = self.linenums_style if (self.linenums or linestart >= 0) and not inline > 0 else False
            if language:
                data_str = DATA_ATTR % language.upper()
                classes.append('language-%s' % language)
            else:
                data_str = DATA_ATTR % 'TEXT'
            if linenums:
                classes.append('linenums')
            class_str = id_str
            if classes:
                class_str += CLASS_ATTR % ' '.join(classes)
            higlight_class = (CLASS_ATTR % css_class) if css_class else ''
            if data_str:
                class_str += data_str
            code = CODE_WRAP % (higlight_class, class_str, self.escape(src), COPY_WRAP % ('#%s' % code_id))
        if inline:
            el = md_util.etree.Element('code', {'class': class_str} if class_str else {})
            el.text = code
            return el
        else:
            return code.strip()


class ChangeCodeExtension(HighlightExtension):

    def __init__(self, *args, **kwargs):
        super(ChangeCodeExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        config = self.getConfigs()
        self.enabled = config.get("_enabled", False)
        md.parser.blockprocessors.register(ChangeCodeBlockProcessor(BlockParser(md)), 'change_code', 80)
        md.registerExtension(self)

    def get_pymdownx_highlighter(self):
        return ChangeCodeHighlight


def makeExtension(*args, **kwargs):
    return ChangeCodeExtension(*args, **kwargs)
