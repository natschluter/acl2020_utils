####################################################################
# A simple program to extract the review load counts per reviewer 
# wrt submission type.  You can generate the input csv files in the 
# Spreadsheet Maker on softconf.
# Contact Natalie nael@itu.dk with any questions
####################################################################

import csv, collections, argparse

def main(submissions_file, assignments_file, output_counts_file):
    with open(submissions_file, 'r') as sfile:
        data = csv.reader(sfile, delimiter=',', quotechar='"')
        smap={d[0]:d[11] for d in data}
        smap.pop('Submission ID', None)
    with open(assignments_file, 'r') as afile:
        data = csv.reader(afile, delimiter=',', quotechar='"')
        amap={d[2]:dict(collections.Counter([smap[x] for x in d[3:-1]])) for d in data}
        amap.pop('Username', None)
        submission_types=['Long','Short']
        with open(output_counts_file,'w') as ofile:
            ofile.write('Username\t'+'\t'.join(submission_types)+'\n')
            for user in amap:
                ofile.write(user)
                for t in submission_types:
                    if t in amap[user]:
                        ofile.write('\t'+str(amap[user][t]))
                    else:
                        ofile.write('\t')
                ofile.write('\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--submissions_file", type=str, required=True, help="The Submission Information csv formatted file from softconf")
    parser.add_argument("--assignments_file", type=str, required=True, help="The Assignment Information csv formatted file from softconf")
    parser.add_argument("--output_file", type=str, required=True, help="The output file for submission type counts (will be tab separated)")
    
    args = parser.parse_args()
    main(args.submissions_file, args.assignments_file, args.output_file)
        