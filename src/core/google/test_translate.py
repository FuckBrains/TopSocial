from core.google.google_translate import *

detect_language('سلام خوبی')

# def test_detect_language(capsys):
#     detect_language('سلام خوبی')
#     out, _ = capsys.readouterr()
#     assert 'is' in out
#
#
# def test_list_languages(capsys):
#     list_languages()
#     out, _ = capsys.readouterr()
#     assert 'Icelandic (is)' in out
#
#
# def test_list_languages_with_target(capsys):
#     list_languages_with_target('is')
#     out, _ = capsys.readouterr()
#     assert u'íslenska (is)' in out
#
#
# def test_translate_text(capsys):
#     translate_text('is', 'Hello world')
#     out, _ = capsys.readouterr()
#     assert u'Halló heimur' in out
#
#
# def test_translate_utf8(capsys):
#     text = u'나는 파인애플을 좋아한다.'
#     translate_text('en', text)
#     out, _ = capsys.readouterr()
#     assert u'I like pineapple.' in out