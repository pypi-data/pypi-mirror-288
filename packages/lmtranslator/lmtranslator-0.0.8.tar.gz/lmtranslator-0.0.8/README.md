# Translator

This repo contains wrapper code for the most performant translation model.

Currently NLLB.

## Features

- Only translates unique sentences
- Checks if input is not empty
- Preprocesses sentences before translation
- Postprocesses translations
- Batch processing
- Automatic language detection
- Only translates sentences where the source language does not match the target language
