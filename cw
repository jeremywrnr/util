#!/usr/bin/perl -w

# like a sandwhich. cat any path-visible script by name
# author: Jeremy Warner, dec 2014

use strict;

my $help;
$help .= "usage: cw <tool> [-l <line#>] [-c <context#>]\n";
$help .= "\topt -l <#>: print a specific line number (#)\n";
$help .= "\topt -c <#>: print surrounding lines (#)\n\n";
$help .= "example: cw bb -l 10 -c 2\n";
$help .= "\tprints lines 8-12 of bb\n\n";
$help .= "cw - (catwhich)\n";
$help .= "\ta tool to show source of scripts in path\n";
$help .= "\tslightly better than 'cat \$(which <tool>)'\n\n";

die $help unless (@ARGV);
my $contextLines = 0;
my $lineNum = 0;
my $tool = 0;

# parse user args
foreach(@ARGV){

    # check for line number mode
    if(/-l/){ $lineNum = -1; next }

    # if entered line mode, parse line number
    elsif($lineNum < 0){ $lineNum = $_ ; next }

    # check for line number mode
    elsif(/-c/){ $contextLines = -1; next }

    # if entered context lines, parse line number
    elsif($contextLines < 0){ $contextLines = $_ ; next }

    # get the name of the file
    elsif(! $tool){ $tool = $_; next }

}

# check for sensible args
if ($contextLines && $lineNum <= 0){
    my $stat = "Error: Need a line number to give context around!\n";
    $stat .= "Specify a positive integer after -l, (cw <tool> -l <#>)\n";
    die $stat;
} elsif ($tool =~ /^-/){
    die "\n\tError: Tool name cannot start with a '-'!\n\n$help";
}

# get full script/tool path
my $path = `which $tool`;
if($?){ # if non zero exit code, errors :(
    die "($tool) not found in path.\n";
}

#print "tool = $tool\n";
#print "path = $path";

# open up requested file
chomp($path);
open(my $TOOLCONTENT, '<:encoding(UTF-8)', $path);

# show a specific line number
if($lineNum){

    # print header with file, lines
    print "\n$tool - ($path)\n";
    print "line - ($lineNum)";
    print ", context - ($contextLines)" if ($contextLines);
    print "\n\n";

    # determine which lines to show
    my $first = $lineNum - $contextLines;
    my $last = $lineNum + $contextLines;

    # print out desired line number range
    while(<$TOOLCONTENT>){
        print "$.\t$_" if ( ($. >= $first) && ($. <= $last) );
    }
    print "\n";
    exit 1

}

# otherwise open up, print all contents
print "\n# $tool - ($path)\n\n";
while(<$TOOLCONTENT>){ print }
print "\n";

