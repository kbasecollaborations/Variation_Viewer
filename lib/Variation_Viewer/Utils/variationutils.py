import sys
import shutil
import subprocess

class variationutils:
    def __init__(self):
        pass

    def validate_params(self, params):
        if 'vcf_ref' not in params:
            raise ValueError('required vcf_ref field was not defined')

    def copy_file(self, src, dest):
        try:
           shutil.copy(src,dest)
        except IOError as e:
           print("Unable to copy file. %s" % e)
        except:
           print("Unexpected error:", sys.exc_info())


    def prepare_genome(self, output_dir, genome_file):
        '''
        function for preparing genome
        '''
        cmd = "samtools faidx " + output_dir+"/igv_output/data/"+genome_file
        try:
           process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
           stdout, stderr = process.communicate()
           if stdout:
               print ("ret> ", process.returncode)
               print ("OK> output ", stdout)
           if stderr:
               print ("ret> ", process.returncode)
               print ("Error> error ", stderr.strip())

        except OSError as e:
           print ("OSError > ", e.errno)
           print ("OSError > ", e.strerror)
           print ("OSError > ", e.filename)

    def bgzip_vcf(self, output_dir, vcf_file):
        '''
        function for zipping vcf file
        '''
        zipcmd = "bgzip "  + output_dir + "/igv_output/data/"+vcf_file
        try:
            process = subprocess.Popen(zipcmd, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stdout:
                print("ret> ", process.returncode)
                print("OK> output ", stdout)
            if stderr:
                print("ret> ", process.returncode)
                print("Error> error ", stderr.strip())

        except OSError as e:
            print("OSError > ", e.errno)
            print("OSError > ", e.strerror)
            print("OSError > ", e.filename)

    def index_vcf(self, output_dir, vcf_file):
        '''
        function for indexing vcf file
        '''
        indexcmd = "tabix -p vcf " + output_dir + "/igv_output/data/"+vcf_file+".gz"
        try:
            process = subprocess.Popen(indexcmd, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stdout:
                print("ret> ", process.returncode)
                print("OK> output ", stdout)
            if stderr:
                print("ret> ", process.returncode)
                print("Error> error ", stderr.strip())

        except OSError as e:
            print("OSError > ", e.errno)
            print("OSError > ", e.strerror)
            print("OSError > ", e.filename)

    def prepare_vcf(self, output_dir, vcf_file):
        '''
        function for preparing vcf file
        '''
        self.bgzip_vcf(output_dir, vcf_file)
        self.index_vcf(output_dir, vcf_file)
       
    def add_header(self,genome_file):
        header = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\">\n<meta name=\"description\" content=\"\">\n<meta name=\"author\" content=\"\">\n<link rel=\"shortcut icon\" href=\"https://igv.org/web/img/favicon.ico\">\n<title>igv.js</title>\n<script src=\"dist/igv.min.js\"></script>\n</head>\n<body>\n<p>\n<h1>"+ genome_file +"VCF file</h1>\n<div id=\"igvDiv\" style=\"padding-top: 10px;padding-bottom: 10px; border:1px solid lightgray\"></div>"
        return header

    def add_reference_genome(self, genome_file):
        reference_genome = "\nreference:\n{\nid: \""+genome_file.split("_")[0]+"\",\nfastaURL: getLocation() + \"/data/"+genome_file+"\"\n},\ntracks:\n[\n\n"
        return reference_genome

    def add_variant_track(self, variant_file):
        variant_track = "{\ntype: \"variant\",\nformat: \"vcf\",\nurl: getLocation() + \"/data/"+variant_file+".gz\",\nindexURL: getLocation() + \"/data/"+variant_file+".gz.tbi\",\nname: \"snps.vcf\", \nsquishedCallHeight: 1, \nexpandedCallHeight: 4, \ndisplayMode: \"squished\", \nvisibilityWindow: 30000 \n} \n]"
        return variant_track          

    def add_gene_track(self, gene_file):
        gene_track = "{ \nname: \"Genes\",\ntype: \"annotation\",\nformat: \"bed\",\nurl: getLocation() + \"/data/"+gene_file+".gz\",\nindexURL: getLocation() + \"/data/" +gene_file+".gz.tbi\",\norder: Number.MAX_VALUE,\nvisibilityWindow: 300000000,\ndisplayMode: \"EXPANDED\"\n},"
        return gene_track

    def add_javascript_code(self, gene_file, variant_file, genome_file):
        jscode = "\n<script type=\"text/javascript\"> \nfunction getLocation() { \n return (location.href).replace(\"/index.html\",\"\") \n} \ndocument.addEventListener(\"DOMContentLoaded\", function () { \nvar options = \n{"
        jscode += self.add_reference_genome(genome_file)
        #jscode += self.add_gene_track(gene_file)
        jscode += self.add_variant_track(variant_file)
        jscode += "\n}; \nvar igvDiv = document.getElementById(\"igvDiv\"); \nigv.createBrowser(igvDiv, options) \n.then(function (browser) { \nconsole.log(\"Created IGV browser\"); \n})\n})"
        return jscode

    def add_footer(self):
        footer = "\n</script></body>\n</html>\n\n"
        return footer

    def create_html(self, output_dir, gene_file, variant_file, genome_file):
        '''
        function for creating index.html file with track information
        '''
        htmlfile = self.add_header(genome_file)
        htmlfile += self.add_javascript_code(gene_file, variant_file, genome_file)
        htmlfile += self.add_footer()
        try:
            with open(output_dir+"/igv_output/index.html", "w") as outfile:
                outfile.write(htmlfile)
        except IOError:
            print("can't create index.html file")
