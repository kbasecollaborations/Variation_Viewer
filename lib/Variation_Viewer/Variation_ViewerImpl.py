# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid
import shutil 
from Variation_Viewer.Utils.htmlreportutils import htmlreportutils
from Variation_Viewer.Utils.variationutils import variationutils
from Variation_Viewer.Utils.downloaddatautils import downloaddatautils
from Variation_Viewer.Utils.genomeutils import genomeutils
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
        self.gu = genomeutils()
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
        self.vu.validate_params(params)
        outputdir = self.shared_folder + '/' + str(uuid.uuid1())
        os.mkdir(outputdir)

        logging.info("Downlading assembly ...")
        genome_info = self.du.download_genome(params)
        genome_path = genome_info['path']
        genome_file = genome_path.split("/")[-1]

        logging.info("downloading variants ...")
        params['variation_name'] = "snps.vcf"
        vcf_info = self.du.download_vcf(params)
        vcf_path = vcf_info['path']
        vcf_file = vcf_path.split("/")[-1]

        # igv tool  path
        src = "/kb/module/deps/igv_output"
        dest = outputdir +"/igv_output"

        try:
           logging.info('Copying directory: %s to %s', src, dest)
           shutil.copytree(src, dest)
        except (shutil.Error, OSError) as e:
           raise ActionError('Unable to copy %s to %s: %s' % (src, dest, str(e)))  

        #shutil.copytree(src,dest)
        self.vu.copy_file(genome_path, outputdir+"/igv_output/data/"+genome_file)
        self.vu.copy_file(vcf_path, outputdir+"/igv_output/data/"+vcf_file)

        logging.info("prepare input data ...")

        self.vu.prepare_genome(outputdir, genome_file)
        self.vu.prepare_vcf(outputdir, vcf_file)

        #gff_file = "/kb/module/test/sample_data/GCA_009858895.3_ASM985889v3_genomic.gff"  #hardcode for testing
        #bed_file = self.gu.gff2bed(gff_file,outputdir)
        #src_path = "/kb/module/test/sample_data"                                          #hardcode for testing
        #self.vu.copy_file(src_path+"/"+bed_file,outputdir + "/igv_output/data/")
        #self.vu.prepare_vcf(outputdir,bed_file)
        
        bed_file = "dummy name"  #will be added for organism with genome
        logging.info("prepare input data ...")
        self.vu.create_html(outputdir, bed_file, vcf_file, genome_file)

        logging.info("creating html report ...")
        output = self.hr.create_html_report(self.callback_url, outputdir, workspace) 
        report = KBaseReport(self.callback_url)

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
