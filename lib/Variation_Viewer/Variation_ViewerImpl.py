# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid

from Variation_Viewer.Utils.htmlreportutils import htmlreportutils
from Variation_Viewer.Utils.variationutils import variationutils
from Variation_Viewer.Utils.downloaddatautils import downloaddatautils
from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class Variation_Viewer:
    '''
    Module Name:
    Variation_Viewer

    Module Description:
    A KBase module: Variation_Viewer
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.hr = htmlreportutils()
        self.vu = variationutils()
        self.du = downloaddatautils()
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_Variation_Viewer(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of type "InputParams" -> structure: parameter
           "vcf_ref" of String, parameter "workspace_name" of String,
           parameter "genome_or_assembly_ref" of String
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_Variation_Viewer
        workspace = params['workspace_name']
        outputdir = self.shared_folder + '/' + str(uuid.uuid1())
        os.mkdir(outputdir)
        genome_info = self.du.download_genome(params)
        genome_file = genome_info['path']
        params['variation_name'] = "snps.vcf"   #hardcode for testing
        vcf_file = self.du.download_vcf(params)
        #exit(vcf_file)   return shock id but vcf file name needed

         # Source path
        source = "/kb/module/deps/igv_output/"

        # Destination path
        destination = outputdir +"/igv_output"
        
        os.system("cp -r " + source +" "+ destination)
        self.vu.copy_file(genome_file, outputdir+"/igv_output/data/") #hardcode for testing
        self.vu.prepare_genome(outputdir, genome_file.split("/")[-1]) #hardcode for testing
        self.vu.prepare_vcf(outputdir,"original_snps.vcf")  #hardcode for testing
        self.vu.prepare_vcf(outputdir,"GCA_009858895.3_ASM985889v3_genomic.bed") #hardcode for testing
        self.vu.create_html(outputdir, "GCA_009858895.3_ASM985889v3_genomic.bed", "original_snps.vcf",genome_file.split("/")[-1] )  #hardcoded for testing
        
        output = self.hr.create_html_report(self.callback_url, outputdir, workspace) 
        report = KBaseReport(self.callback_url)

        '''
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['parameter_1']},
                                                'workspace_name': params['workspace_name']})
                                                
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }'''
        #END run_Variation_Viewer

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_Variation_Viewer return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
