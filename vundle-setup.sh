#!/bin/bash

# get vundle package manager
vundloc='~/.vim/bundle/Vundle.vim'
mkdir -p $vundloc
git clone https://github.com/gmarik/Vundle.vim.git $vundloc
vim +BundleInstall +qa

# youcompleteme auto-completion
cd ~/.vim/bundle/YouCompleteMe
git submodule update --init --recursive
./install.py --clang-completer
