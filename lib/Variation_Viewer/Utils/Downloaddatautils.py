import os
import subprocess

from pprint import pprint,pformat

from installed_clients.VariationUtilClient import VariationUtil
from installed_clients.AssemblyUtilClient import AssemblyUtil


class Downloaddatautils:

    def __init__(self):
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.au = AssemblyUtil(self.callbackURL)
        self.vu = VariationUtil(self.callbackURL)
        pass

    def download_genome(self, params):
        file = self.au.get_assembly_as_fasta({
          'ref': params['genome_or_assembly_ref']
        })
        return file

    def download_vcf(self, params):
        params['input_var_ref'] = params['vcf_ref']
        self.vu.export_variation_as_vcf(params)

