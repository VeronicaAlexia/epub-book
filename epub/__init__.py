import zipfile
import codecs
from .template import *
from .tools import *
from .makedir import set_epub_cache_file


class EpubFile:

    def __init__(self):
        set_epub_cache_file()
        self._chapter_format = chapter_xhtml
        self._toc_ncx = toc_ncx
        self._content_opf_manifest = str_mid(self._content_opf, '<manifest>', '</manifest>')
        self._content_opf_spine = str_mid(self._content_opf, '<spine toc="ncx">', '</spine>')
        self._toc_ncx_navMap = str_mid(self._toc_ncx, '<navMap>', '</navMap>')

        self._content_opf = format_content_opf(Vars.book_info.book_id, Vars.book_info.book_name,
                                               Vars.book_info.author_name)
        self._toc_ncx = format_toc_ncx(Vars.book_info.book_id, Vars.book_info.book_name, Vars.book_info.author_name)

    def _add_manifest_chapter(self, chapter_id: str):
        if self._content_opf_manifest.find('id="' + chapter_id + '.xhtml"') == -1:
            _before = self._content_opf_manifest
            self._content_opf_manifest += format_manifest(chapter_id)
            self._content_opf = self._content_opf.replace(
                f'<manifest>{_before}</manifest>', f'<manifest>{self._content_opf_manifest}</manifest>', 1)

    def _add_manifest_image(self, filename: str):
        if self._content_opf_manifest.find('id="' + filename + '"') == -1:
            _before = self._content_opf_manifest
            _media_type = 'image/png' if filename.endswith('.png') else 'image/jpeg'
            self._content_opf_manifest += format_image_format_manifest(filename, _media_type)
            self._content_opf = self._content_opf.replace(
                '<manifest>' + _before + '</manifest>',
                '<manifest>' + self._content_opf_manifest + '</manifest>', 1)

    def _add_spine(self, chapter_id: str):
        if self._content_opf_spine.find(f'idref="{chapter_id}.xhtml"') == -1:
            _before = self._content_opf_spine
            self._content_opf_spine += format_spine(chapter_id)
            self._content_opf = self._content_opf.replace(
                f'<spine toc="ncx">{_before}</spine>', f'<spine toc="ncx">{self._content_opf_spine}</spine>', 1)

    def add_nav_map(self, chapter_index: str, chapter_id: str, chapter_title: str):
        if self._toc_ncx_navMap.find('id="' + chapter_id) == -1:
            _before = self._toc_ncx_navMap
            self._toc_ncx_navMap += format_nav_map(chapter_id, chapter_index, chapter_title)
            self._toc_ncx = self._toc_ncx.replace(
                f'<navMap>{_before}</navMap>', f'<navMap>{self._toc_ncx_navMap}</navMap>', 1)

    def export(self):
        write(os.path.join(Vars.config_dir, 'OEBPS', 'content.opf'), 'w', self._content_opf)
        with codecs.open(Vars.config_dir + '/OEBPS/toc.ncx', 'w', 'utf-8') as _file:
            _file.write(self._toc_ncx)
        with zipfile.ZipFile(Vars.epub_dir, 'w', zipfile.ZIP_DEFLATED) as _file:
            _result = get_all_files(Vars.config_dir)
            for _name in _result:
                _file.write(_name, _name.replace(Vars.config_dir + '/', ''))

    def add_chapter(self, chapter_info: ciweimao.ContentInfo, content_text: str):
        chapter_data = self._chapter_format.replace(
            '<title>${chapter_title}</title>',
            f'<title>第{chapter_info.chapter_index}章: {chapter_info.chapter_title} </title>') \
            .replace('${chapter_content}', f'<h3>{chapter_info.chapter_title}</h3>\r\n' + content_text)
        write(chapter_info.text_content_path, 'w', get_chapter_image(chapter_data))

    def download_book_write_chapter(self):
        file_name_list = os.listdir(os.path.join(Vars.config_dir, 'OEBPS', 'Text'))
        for order_count, filename in enumerate(sorted(file_name_list), start=2):
            if filename.find('$') > -1 or filename == 'cover.xhtml':
                continue
            if re.findall('^(\\d+).xhtml', filename):
                continue
            f_name = os.path.splitext(filename)[0]
            self._add_manifest_chapter(f_name)
            self._add_spine(f_name)
            _data_chapter = re.sub(r'<h3>.*?</h3>', '', write(Vars.config_dir + '/OEBPS/Text/' + filename, 'r').read())
            division_and_chapter_file = str_mid(_data_chapter, "<title>", "</title>")
            self.add_nav_map(str(order_count), f_name, division_and_chapter_file)

            # for _a in re.findall(r'<a href=.*?>章节链接</a>', _data_chapter):
            #     _data_chapter = _data_chapter.replace(_a, '章节链接:' + str_mid(_a, '<a href="', '"')
            #                                           )
            # for _img in re.findall(r'<img src=.*?>', _data_chapter):
            #     _data_chapter = _data_chapter.replace(_img, '图片:"' + str_mid(_img, "alt='", "'") + '",' + '位置:"'
            #                                           + str_mid(_img, '<img src="', '"').replace('../', '') + '"')

            _data_chapter = re.sub(r'</?[\S\s]*?>', '', _data_chapter)
            write(os.path.splitext(Vars.epub_dir)[0] + ".txt", 'a', re.sub(r'[\r\n]+', '\r\n', _data_chapter))
            order_count += 1
        for filename in sorted(os.listdir(Vars.config_dir + '/OEBPS/Images/')):
            self._add_manifest_image(filename)
        self.export()
