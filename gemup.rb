#!/usr/bin/env ruby


# gemup.rb - simple system wide gem management
# by jeremy warner, fall 2015


#http://axonflux.com/uninstalling-and-reinstalling-all-ruby-gems
def allgems
  `gem list | cut -d" " -f1`.split "\n"
end


# reinstall all gems
def reinstall(gems)
  gems.each do |gem|
    system "gem uninstall -aIx #{gem}"
    system "gem install #{gem}"
  end
end


# restore gem state
def pristine(gems)
  gems.each do |gem|
    system "gem pristine #{gem}"
  end
end


# just list gems
def listing(gems)
  gems.each {|gem| puts gem }
end


# show help banner
def showhelp(arg=nil)
  puts "gemup takes one of [reinstall, pristine, list]"
  puts "you entered: #{arg}" unless arg.nil?
end


ARGV.each do |arg|
  case arg
  when 'reinstall'
    reinstall allgems
  when 'pristine'
    pristine allgems
  when 'list'
    listing allgems
  else
    showhelp arg
  end
end


# no args given, help
showhelp if ARGV.empty?

