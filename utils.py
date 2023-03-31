def generate_sequence(exon_starts=[], exon_ends=[]):
    """Create a genome array from a list of exon start and end positions."""
    genome_start = exon_starts[0]
    genome_end = exon_ends[-1]
    genome_length = genome_end - genome_start
    genome = [0] * genome_length
    
    for start, end in zip(exon_starts, exon_ends):
        for i in range(start - genome_start, end - genome_start):
            genome[i] = 1
    
    return genome