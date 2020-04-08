import uuid
import os
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace
import shutil 

class htmlreportutils:
    def __init__(self):
        self.organism_dict = {}
        pass

    def create_html_report(self, callback_url, output_dir, workspace_name):
        '''
         function for creating html report
        '''

        dfu = DataFileUtil(callback_url)
        report_name = 'kb_gsea_report_' + str(uuid.uuid4())
        report = KBaseReport(callback_url)
        report_dir = "localhost" 
        #htmlstring = "<a href=" + report_dir + "/jbrowse/index.html>report link</a>"
        htmlstring = "<a href='./igv_output/index.html'>report link</a>"
        index_file_path = output_dir + "/index.html"
        html_file = open(index_file_path, "wt")
        n = html_file.write(htmlstring)
        html_file.close()
        # Source path 
        #source = "/kb/module/deps/jbrowse"
  
        # Destination path 
        #destination = output_dir +"/jbrowse"
  
        #dest = shutil.copytree(source, destination) 
        #os.system("cp -r " + source +" "+ destination)

        report_shock_id = dfu.file_to_shock({'file_path': output_dir,
                                            'pack': 'zip'})['shock_id']

        html_file = {
            'shock_id': report_shock_id,
            'name': 'index.html',
            'label': 'index.html',
            'description': 'HTMLL report for GSEA'
            }
        
        report_info = report.create_extended_report({
                        'direct_html_link_index': 0,
                        'html_links': [html_file],
                        'report_object_name': report_name,
                        'workspace_name': workspace_name
                    })
        return {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }

