
class genomeutils:

    def __init__(self):
        pass

    def gff2bed(self, gff_file):
        #awk -F "\t" '{print $1"\t"$4"\t"$5"\t"$9"\t"$6"\t"$7"\t"$2"\t"$8"\t"$9}' GCA_009858895.3_ASM985889v3_genomic.gff
        fw = open("bedfile.txt", "w")

        with open(gff_file, "r") as fp:
             for line in fp: 
                if not line.lstrip().startswith('#'):
                   line = line.rstrip()
                   rec = line.split("\t")
                   fw.write(rec[0]+"\t"+rec[3]+"\t"+rec[4]+"\t"+rec[8]+"\t"+rec[5]+"\t"+rec[6]+"\t"+rec[1]+"\t"+rec[7]+"\t"+rec[8]+"\n")
        #return bed_file


#gu = genomeutils()
#gu.gff2bed("/home/manish/Desktop/apps/Variation_Viewer/deps/igv_output/tmp/GCA_009858895.3_ASM985889v3_genomic.gff")

