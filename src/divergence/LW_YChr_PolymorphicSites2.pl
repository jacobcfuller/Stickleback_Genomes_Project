#!/usr/bin/perl

use warnings;
use constant WINDOW => 1000;

open (FILE, "maleFemaleSNPComparison.diff.sites_in_files") || die "Unable to open file: $!\n"; 
	
	my $counter = 0;
	my $totalYPolymorphic = 0;
	my @YWindows;

while (<FILE>) {

	$counter++;
	
	my @LWSNPs = split (/\t/, $_);
	chomp(@LWSNPs);
	my $male_ref = $LWSNPs[4];
	my $male_alt = $LWSNPs[6];
	my $female_ref = $LWSNPs[5];
	my $female_alt = $LWSNPs[7];
	my $in_file = $LWSNPs[3];
	my $position = $LWSNPs[1];

	
	# fix <NON_REF> alleles to equal reference allele
	if ($male_alt eq "<NON_REF>") {
		$male_alt = $male_ref;
		
}	
	
	if ($female_alt eq "<NON_REF>") { 	
		$female_alt = $female_ref;
			
}

	
	
	#insert if statements to compare male and female genotypes
	#if genotypes indicate position is polymorphic on Y, enter the counting loop
	if ($male_ref eq $female_ref and $male_alt ne $female_alt and 
	$female_ref eq $female_alt and $male_ref ne $male_alt and 
	length($male_ref) == 1 and length($female_ref) == 1 and length($male_alt) == 1 
	and length($female_alt) == 1 and $male_alt ne "*" and $male_alt ne "." 
	and $in_file eq "B") {
		$totalYPolymorphic++;



}
	#check if counter equals 1000
	if ($counter == 1000) {
		$counter = 0;
		push(@YWindows, $totalYPolymorphic);
		$totalYPolymorphic = 0;
		
		
}	
	print "$counter \t $totalYPolymorphic\n";
		
}
	#set data to output file
open (OUT, "> YChr_PolymorphicSites4.txt") || die "$!";

	print OUT "@YWindows \n"; # print to file