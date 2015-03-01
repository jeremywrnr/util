#!/usr/bin/env ruby

core = %w{
fasd
tree
tmux
reattach-to-user-namespace
}

core.each {|c| `brew install #{c}`}
