#!/usr/bin/env zsh

DFPATH=~/Documents/Code/dotfiles
RUNPATH=$(cd "${0%/*}"; pwd)

cd $DFPATH/vim
vim $DFPATH/vim/mappings.vim
cd $DFPATH
git add vimrc
git add vim/*
git commit -av
git push origin main
echo "Commit complete."
$RUNPATH/srcdot
cd -
