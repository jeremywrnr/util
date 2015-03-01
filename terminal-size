#!/usr/bin/env ruby

require 'terminfo'

# ts - terminal sizer, with terminfo

case ARGV.first
when '-v'
  puts "hieght: " << TermInfo.screen_size[0].to_s
  puts "width:  " << TermInfo.screen_size[1].to_s
else
  puts TermInfo.screen_size
end

