#!/usr/bin/env zsh

df_path=$(cd "${0%/*}/.."; pwd)

cd $df_path/vim
vim $df_path/vim/mappings.vim +NERDTree
cd $df_path
git add vimrc
git add vim/*
git commit -av
git push origin master
echo "Commit complete."
./util/dot
cd -
