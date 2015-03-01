#!/usr/bin/env zsh

DFPATH=~/GitHub/dotfiles
RUNPATH=$(cd "${0%/*}"; pwd)

cd $DFPATH/vim
vim $DFPATH/vim/mappings.vim +NERDTree
cd $DFPATH
git add vimrc
git add vim/*
git commit -av
git push origin master
echo "Commit complete."
$RUNPATH/dot
cd -
