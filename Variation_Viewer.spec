/*
A KBase module: Variation_Viewer
*/

module Variation_Viewer {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    typedef structure{
        string vcf_ref;
        string workspace_name;
    } InputParams;


    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */

    funcdef run_Variation_Viewer(InputParams params) returns (ReportResults output) authentication required;

};
