import uuid
import os
import json
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace
import shutil 

class variationutils:
    def __init__(self):
        self.organism_dict = {}
        pass

    def prepare_genome(self, output_dir, genome_file):
        '''
        function for preparing genome
        '''
        cmd = "/jbrowse/bin/prepare-refseqs.pl --fasta " + "/kb/module/work/tmp/*.fa_assembly.fa --out " + output_dir + "/jbrowse/data"
        #cmd = "/jbrowse/bin/prepare-refseqs.pl --fasta " + "/kb/module/test/sample_data/GCA_009858895.3_ASM985889v3_genomic.gbff_genome_assembly.fa_assembly.fa --out " + output_dir + "/jbrowse/data"
        os.system(cmd)

    def prepare_vcf(self, output_dir, vcf_file):
        '''
        function for preparing vcf file
        '''
        #os.system("cp /kb/module/test/sample_data/snps.vcf " + output_dir + "/jbrowse/data")
        os.system("cp /kb/module/work/tmp/*_vcf/original_snps.vcf " + output_dir + "/jbrowse/data")
        zipcmd = "bgzip "  + output_dir + "/jbrowse/data/original_snps.vcf"
        os.system(zipcmd)
        indexcmd = "tabix -p vcf " + output_dir + "/jbrowse/data/original_snps.vcf.gz"
        os.system(indexcmd)

    def updateJson(self, output_dir, trackname):
        '''
        function for updating json file with track information
        '''
        jsonfile = output_dir + "/jbrowse/data/trackList.json"
        data = {}
        with open(jsonfile) as json_file:
           data = json.load(json_file)
           data['tracks'].append({
           'label': trackname,
           'key': trackname,
           'storeClass': 'JBrowse/Store/SeqFeature/VCFTabix',
           'urlTemplate'   : trackname,
           'type'          : 'JBrowse/View/Track/HTMLVariants'
           })
       
        with open(jsonfile, 'w') as outfile:
           json.dump(data, outfile) 
