#!/usr/bin/perl

while (<STDIN>) {
    if (/^From:\s+(.*\@example\.com)/i){
        die "Email Rejected: Blocked sender from domain: $1\n";
    }
    print $_;
}