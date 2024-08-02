from .lmtranslator import Translator

translate = Translator.translate
translate_df = Translator.translate_df
translate_with_llm = Translator.translate_with_llm
load_llm_for_translation = Translator.load_llm_for_translation

__all__ = ['translate', 'translate_df', 'translate_with_llm', 'load_llm_for_translation']