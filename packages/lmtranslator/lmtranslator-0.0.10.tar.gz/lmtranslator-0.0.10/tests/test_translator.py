import lmtranslator
import pandas as pd

data = {
    'Sentences': [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is transforming the world.",
        "She sells seashells by the seashore.",
        "The weather today is sunny with a chance of rain.",
        "Python is a versatile programming language.",
        "He quietly opened the door and tiptoed inside.",
        "The conference was attended by experts from various fields.",
        "Reading books can significantly improve your vocabulary.",
        "The cat sat on the mat and purred contentedly.",
        "Traveling to new places can be a great learning experience."
    ]
}

# Creating the DataFrame
df = pd.DataFrame(data)

def test_translation():
    translated_text = lmtranslator.translate("Je vais au magazin.")
    
    assert translated_text == "I'm going to the store."

def test_translate_df():
    lmtranslator.translate_df(df, src_col="Sentences", tgt_col="translation")

    assert not df.empty
    assert 'translation' in df.columns

def test_translate_df():
    lmtranslator.translate_df(df, src_col="Sentences", tgt_col="translation", src_lang="fra_Latn")

    assert not df.empty
    assert 'translation' in df.columns