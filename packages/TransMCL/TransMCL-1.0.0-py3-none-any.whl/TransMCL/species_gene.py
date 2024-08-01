from __future__ import print_function
from .isosvm import flood_fill, run_isosvm, get_isosvm_OG

def get_species_gene(
    gene_lst,
    gene_faa,
    gene_spe,
    gene_ass,
    merged_gene,
    excludes,
    spe_map,
    species
):
    output = [ None ]
    item_map = {}
    item_ass = {}
    for i in range( 1, len(gene_spe)+1 ):
        if spe_map[species] != gene_spe[i]:
            continue
        if i in excludes:
            continue
        item_map[ gene_lst[i] ] = len(output)
        output.append([ gene_lst[i], gene_faa[i][1:] ])
        
    for it in merged_gene:
        if not it:
            continue
        if species != it[2]:
            continue
        item_map[ gene_lst[i] ] = len(output)
        output.append([ species+"_"+it[0], it[1] ])
    
    for k, v in gene_ass.items():
        k = item_map.get( gene_lst[k], None)
        if not k:
            continue
        item_ass[k] = v
    return output, item_ass



def get_isoform(
    file_path,
    gene_map,
    gene_lst,
    gene_grp,
    gene_ass,
    gene_faa, 
    gene_spe, 
    merged_gene,
    excludes,
    spe_map,
    spe_tra,
    threads,
    merged_coo,
    MSA
):
    isoform = [i for i in range(len(gene_lst)) ]
    fp = open( file_path + "/isoform.txt", "w")
    for species, v in spe_map.items():
        if not spe_tra[v]:
            continue  
        species_faa, species_ass = get_species_gene(
            gene_lst,
            gene_faa,
            gene_spe,
            gene_ass,
            merged_gene,
            excludes,
            spe_map,
            species     
        )

        flood_fill(
            file_path + "/" + species,
            species_faa,
            threads
        )

        # Run isosvm
        run_isosvm(
            file_path + "/" + species,
            species_faa,
            threads,
            MSA
        )
        species_isoform = get_isosvm_OG(
            file_path + "/" + species,
            species_faa,
            gene_map,
            gene_lst,
            species_ass,
            gene_grp,
            merged_coo
        )

        if file_path[-3:] == "2nd":
            continue
        
        for it in species_isoform:
            if not it:
                continue
            kept = gene_map[ species_faa[ it[0] ][0] ]
            for gene in it[1:]:
                isoform[ gene_map[ species_faa[gene][0] ] ] = kept
                print ( "%d\t%d" % (gene_map[ species_faa[gene][0] ], kept), file=fp)
    
    fp.close()
    return isoform


if __name__ == "__main__":
    pass
