container = """
<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>
"""

mimetype = "application/epub+zip"

content_opf = """
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
<dc:identifier id="BookId">hbooker:${book_id}</dc:identifier>
<dc:title>${book_title}</dc:title>
<dc:creator opf:role="aut">${book_author}</dc:creator>
<dc:language>zh-CN</dc:language>
<dc:publisher>hbooker.com</dc:publisher>
<meta name="cover" content="cover.jpg"/>
</metadata>
<manifest>
<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml" />
<item href="Images/cover.jpg" id="cover.jpg" media-type="image/jpeg" />
<item href="Text/cover.xhtml" id="cover.xhtml" media-type="application/xhtml+xml" />
${chapter_format_manifest}={{{<item href="Text/${chapter_id}.xhtml" id="${chapter_id}.xhtml" media-type="application/xhtml+xml" />}}}
${image_format_manifest}={{{<item href="Images/${filename}" id="${filename}" media-type="${media_type}" />}}}
</manifest>
<spine toc="ncx">
<itemref idref="cover.xhtml" />
${chapter_format_spine}={{{<itemref idref="${chapter_id}.xhtml" />}}}
</spine>
<guide>
<reference href="Text/cover.xhtml" title="书籍封面" type="cover" />
</guide>
</package> 
"""

toc_ncx = """
<?xml version="1.0" encoding="utf-8" standalone="no" ?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta content="hbooker:${book_id}" name="dtb:uid"/>
<meta content="2" name="dtb:depth"/>
<meta content="0" name="dtb:totalPageCount"/>
<meta content="0" name="dtb:maxPageNumber"/>
</head>
<docTitle>
<text>${book_title}</text>
</docTitle>
<docAuthor>
<text>${book_author}</text>
</docAuthor>
<navMap>
<navPoint id="cover" playOrder="1"><navLabel><text>書籍封面</text></navLabel><content src="Text/cover.xhtml" /></navPoint>
${chapter_format_navMap}={{{<navPoint id="${chapter_id}" playOrder="${chapter_index}"><navLabel><text>${chapter_title}</text></navLabel><content src="Text/${chapter_id}.xhtml" /></navPoint>}}}
</navMap>
</ncx>  
"""

cover_xhtml = """
<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ch">
<head>
<title>书籍封面</title>
</head>
<body>
<div style="text-align: center; padding: 0; margin: 0;">
<svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 179 248" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">
<image height="248" width="179" xlink:href="../Images/cover.jpg"> </image>
</svg>
</div>
</body>
</html> 
"""

chapter_xhtml = """
<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>${chapter_title}</title>
</head>
<body>
${chapter_content}
</body>
</html>
"""