import os
import subprocess

class variationutils:
    def __init__(self):
        pass

    def copy_file(self, src, dest):
        os.system("cp " + src + " " +dest)

    def prepare_genome(self, output_dir, genome_file):
        '''
        function for preparing genome
        '''
        cmd = "samtools faidx " + output_dir+"/igv_output/data/"+genome_file
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print (stdout)
        #os.system(cmd)   #use subprocess instead

    def bgzip_vcf(self, output_dir, vcf_file):
        '''
        function for zipping vcf file
        '''
        zipcmd = "bgzip "  + output_dir + "/igv_output/data/"+vcf_file
        zipprocess = subprocess.Popen(zipcmd, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = zipprocess.communicate()
        print (stdout)

    def index_vcf(self, output_dir, vcf_file):
        '''
        function for indexing vcf file
        '''
        indexcmd = "tabix -p vcf " + output_dir + "/igv_output/data/"+vcf_file+".gz"
        indexprocess = subprocess.Popen(indexcmd, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = indexprocess.communicate()
        print (stdout)

    def prepare_vcf(self, output_dir, vcf_file):
        '''
        function for preparing vcf file
        '''
        self.copy_file("/kb/module/test/sample_data/"+ vcf_file, output_dir + "/igv_output/data" )  #hardcoded for testing
        self.bgzip_vcf(output_dir, vcf_file)
        self.index_vcf(output_dir, vcf_file)
       
    def add_header(self):
        header = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\">\n<meta name=\"description\" content=\"\">\n<meta name=\"author\" content=\"\">\n<link rel=\"shortcut icon\" href=\"https://igv.org/web/img/favicon.ico\">\n<title>igv.js</title>\n<script src=\"dist/igv.min.js\"></script>\n</head>\n<body>\n<p>\n<h1>Covid19 VCF file</h1>\n<div id=\"igvDiv\" style=\"padding-top: 10px;padding-bottom: 10px; border:1px solid lightgray\"></div>"
        return header

    def add_reference_genome(self):
        reference_genome = "\nreference:\n{\nid: \"covid19\",\nfastaURL: getLocation() + \"/data/GCA_009858895.3_ASM985889v3_genomic.gbff_genome_assembly.fa\"\n},"
        return reference_genome

    def add_variant_track(self):
        variant_track = "{\ntype: \"variant\",\nformat: \"vcf\",\nurl: getLocation() + \"/data/original_snps.vcf.gz\",\nindexURL: getLocation() + \"/data/original_snps.vcf.gz.tbi\",\nname: \"snps.vcf\", \nsquishedCallHeight: 1, \nexpandedCallHeight: 4, \ndisplayMode: \"squished\", \nvisibilityWindow: 30000 \n} \n]"
        return variant_track          

    def add_gene_track(self):
        gene_track = "\ntracks:\n[\n\n{ \nname: \"Genes\",\ntype: \"annotation\",\nformat: \"bed\",\nurl: getLocation() + \"/data/GCA_009858895.3_ASM985889v3_genomic.bed.gz\",\nindexURL: getLocation() + \"/data/GCA_009858895.3_ASM985889v3_genomic.bed.gz.tbi\",\norder: Number.MAX_VALUE,\nvisibilityWindow: 300000000,\ndisplayMode: \"EXPANDED\"\n},"
        return gene_track

    def add_javascript_code(self):
        jscode = "\n<script type=\"text/javascript\"> \nfunction getLocation() { \n return location.href \n} \ndocument.addEventListener(\"DOMContentLoaded\", function () { \nvar options = \n{"
        jscode += self.add_reference_genome()
        jscode += self.add_gene_track()
        jscode += self.add_variant_track()
        jscode += "\n}; \nvar igvDiv = document.getElementById(\"igvDiv\"); \nigv.createBrowser(igvDiv, options) \n.then(function (browser) { \nconsole.log(\"Created IGV browser\"); \n})\n})"
        return jscode

    def add_footer(self):
        footer = "\n</script></body>\n</html>\n\n"
        return footer

    def create_html(self, output_dir, gene_file, variant_file):
        '''
        function for updating json file with track information
        '''
        htmlfile = self.add_header()
        htmlfile += self.add_javascript_code()
        htmlfile += self.add_footer()
        f= open(output_dir+"/igv_output/index.html", "w")
        f.write(htmlfile)
        f.close()   
        

vu = variationutils()
vu.prepare_genome(".","./igv_output/data/GCA_009858895.3_ASM985889v3_genomic.gbff_genome_assembly.fa")
#vu.copy_file("/home/manish//Desktop/apps/Variation_Viewer/deps/igv_output/data/original_snps.vcf.gz", "/home/manish/Desktop/apps/Variation_Viewer/lib/Variation_Viewer/Utils/igv_output/data/original_snps.vcf.gz")
vu.prepare_vcf(".","original_snps.vcf")
#file = vu.create_html(".","gbk", "snp")
#print(file)
