#!/bin/bash
# Maintainer: Faris Chugthai

# Overwhelmingly so I remember what the fuck I did
# Aug 31, 2020
[[ ! -d ~/.pandoc ]] && mkdir ~/.pandoc

[[ ! -f ~/.pandoc/custom_reference.docx ]] && ln -s ~/projects/codys_templates/custom_reference.docx ~/.pandoc/custom_reference.docx

