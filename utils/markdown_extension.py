from utils.uuid import uuid

from markdown import util as md_util
from pymdownx.highlight import Highlight, HighlightExtension

CODE_WRAP = \
    '<pre%s><code%s>%s</code>%s</pre>'
ID_ATTR = ' id="%s"'
CLASS_ATTR = ' class="%s"'
DATA_ATTR = ' data-lang="%s"'
COPY_WRAP = \
    '<a class="copy-code" href="javascript:void(0);" data-clipboard="%s" title="拷贝代码">' \
    '<i class="fa fa-clipboard"></i></a>'


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
            data_str = ''
            code = self.escape(src)
            classes = [css_class] if css_class else []
            if language:
                data_str = DATA_ATTR % language.upper()
                classes.append('language-%s' % language)
            class_str = id_str
            if len(classes):
                class_str += ' '.join(classes)
            if data_str:
                class_str += data_str
        else:
            # Format block code for a JavaScript Syntax Highlighter by specifying language.
            classes = []
            data_str = ''
            linenums = self.linenums_style if (self.linenums or linestart >= 0) and not inline > 0 else False
            if language:
                data_str = DATA_ATTR % language.upper()
                classes.append('language-%s' % language)
            if linenums:
                classes.append('linenums')
            class_str = id_str
            if classes:
                class_str += CLASS_ATTR % ' '.join(classes)
            higlight_class = (CLASS_ATTR % css_class) if css_class else ''
            if data_str:
                class_str += data_str
            code = CODE_WRAP % (higlight_class, class_str, self.escape(src), COPY_WRAP % code_id)
        if inline:
            el = md_util.etree.Element('code', {'class': class_str} if class_str else {})
            el.text = code
            return el
        else:
            return code.strip()

    def get_uuid(self, data):
        ''.join(random.sample(string.ascii_letters + string.digits, 8))
        time.time()
        return


class ChangeCodeExtension(HighlightExtension):

    def __init__(self, *args, **kwargs):
        super(ChangeCodeExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        config = self.getConfigs()
        self.enabled = config.get("_enabled", False)
        md.registerExtension(self)

    def get_pymdownx_highlighter(self):
        return ChangeCodeHighlight


def makeExtension(*args, **kwargs):
    return ChangeCodeExtension(*args, **kwargs)
