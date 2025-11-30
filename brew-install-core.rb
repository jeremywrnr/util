#!/usr/bin/env ruby

core = %w{
vim
git
curl
fasd
tree
tmux
reattach-to-user-namespace
}

core.each {|c| `brew install #{c}`}
