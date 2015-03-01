#!/usr/bin/env ruby

# gemup.rb - simple system wide gem management
# by jeremy warner, fall 2015

#http://axonflux.com/uninstalling-and-reinstalling-all-ruby-gems
def allgems
  `gem list | cut -d" " -f1`.split "\n"
end

# update all gems
def update(gems)
  gems.each do |gem|
    system "gem update #{gem}"
  end
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
  puts "gemup takes one of [update, reinstall, pristine, list]"
  puts "you entered: #{arg}" unless arg.nil?
end


ARGV.each do |arg|
  case arg
  when 'update'
    update allgems
  when 'reinstall'
    reinstall allgems
  when 'pristine'
    pristine allgems
  when 'list'
    listing allgems
  when 'version'
    puts `gem list`
  else
    showhelp arg
  end
end

# no args given, help
showhelp if ARGV.empty?
