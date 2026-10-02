# Fonts

All four families are licensed under the SIL Open Font License 1.1
(https://openfontlicense.org) and were downloaded from Google Fonts (latin
subset).

- `Caprasimo-400.woff2`: Caprasimo
- `Shrikhand-400.woff2`: Shrikhand
- `Fredoka-700.woff2`: Fredoka, fixed at weight 700
- `Montserrat-600.woff2`, `Montserrat-700.woff2`: Montserrat, fixed at weights 600 and 700

Fredoka and Montserrat are served as variable fonts. Chrome embeds variable
fonts in PDFs as Type 3 fonts, so these fixed-weight copies were made with
fontTools' `varLib.instancer`; they keep the kerning.
