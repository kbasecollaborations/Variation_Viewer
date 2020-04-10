class genomeutils:

    def __init__(self):
        pass

    def gff2bed(self, gff_file, output_dir):
        #awk -F "\t" '{print $1"\t"$4"\t"$5"\t"$9"\t"$6"\t"$7"\t"$2"\t"$8"\t"$9}' GCA_009858895.3_ASM985889v3_genomic.gff
        gff_file_name = gff_file.split("/")[-1]
        bed_file = gff_file_name.replace(".gff",".bed")

        try:
           fw = open(output_dir +"/igv_output/data/"+bed_file, "w")

           try:
              with open(gff_file, "r") as fp:
                 for line in fp:
                    if not line.lstrip().startswith('#'):
                       line = line.rstrip()
                       rec = line.split("\t")
                       fw.write(rec[0]+"\t"+rec[3]+"\t"+rec[4]+"\t"+rec[8]+"\t"+rec[5]+"\t"+rec[6]+"\t"+rec[1]+"\t"+rec[7]+"\t"+rec[8]+"\n")
           except IOError:
               print ("could not write to bed file\n")

        except IOError:
            print("could not read input gff file\n")

            fw.close()

        return bed_file
