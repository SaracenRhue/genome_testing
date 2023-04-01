from selenium import webdriver
from selenium.webdriver.common.by import By


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



def get_genome(genome):
    """Get a genome from UCSC."""
    url = f'https://genome.ucsc.edu/cgi-bin/hgTables?hgsid=1599516503_mUYmf99zTvPzPmKW4TfEzYaGgYR6&clade=mammal&org={genome}&db=0&hgta_group=genes&hgta_track=refSeqComposite&hgta_table=ncbiRefSeq&hgta_regionType=range&position=&hgta_outputType=primaryTable&hgta_outFileName='
    op = webdriver.FirefoxOptions()
    op.add_argument('--headless')
    driver = webdriver.Firefox(options=op)
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element(By.ID, 'hgta_doTopSubmit').click()
    text = driver.find_element(By.TAG_NAME, 'pre').text
    driver.quit()
    with open(f'genome_files/{genome}', 'w') as f:
        f.write(text)