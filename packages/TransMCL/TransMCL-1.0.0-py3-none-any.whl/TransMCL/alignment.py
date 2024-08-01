class Alignment:
    
    def __init__(self, line, gene_map):
        # Column 0: query gene
        # Column 1: target gene
        # Column 2: identity
        # Column 3: match sites
        # Column 4: mismatch sites
        # Column 5: gap opens
        # Column 6: query interval left
        # Column 7: query interval right
        # Column 8: target interval left
        # Column 9: target interval right
        # Column 10: e-value
        # Column 11: bit scores
        # Column 12: query species
        # Column 13: target species
        
        line = line.split()
        self.qry = gene_map[ line[0] ]
        self.tar = gene_map[ line[1] ]
        self.idt = float( line[2] )
        self.mat = int( line[3] )
        self.mis = int( line[4] )
        self.gap = int( line[5] )
        self.qrL = int( line[6] )
        self.qrR = int( line[7] )
        self.taL = int( line[8] )
        self.taR = int( line[9] )
        self.eva = float( line[10] )
        self.bit = float( line[11] )
