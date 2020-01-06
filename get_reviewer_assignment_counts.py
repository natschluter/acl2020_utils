####################################################################
# A simple program to extract the review load counts per reviewer 
# wrt submission type.  You can generate the input csv files in the 
# Spreadsheet Maker on softconf.
# The output is a tab separated file with a header: Username\tLong\tShort
# and following lines [username]\tlong_paper_count\tshort_paper_count
# Contact Natalie nael@itu.dk with any questions
####################################################################

import csv, collections, argparse

def main(submissions_file, assignments_file, output_counts_file):
    with open(submissions_file, 'r') as sfile:
        csv_reader = csv.reader(sfile, delimiter=',', quotechar='"')
        data=list(csv_reader)
        subm_type_index=data[0].index('Submission Type')
        smap={d[0]:d[subm_type_index] for d in data[1:]}  
        #print(smap)
        smap.pop('Submission ID', None)
    with open(assignments_file, 'r') as afile:
        data = csv.reader(afile, delimiter=',', quotechar='"')
        amap={}
        for d in data:
            for x in d[3:-1]:
                if x in smap:
                    amap[d[2]]=dict(collections.Counter([smap[x] for x in d[3:-1]]))
                else:
                    print('Submission', x, 'is missing from assignments')
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
    parser.add_argument("--assignments_file", type=str, required=True, help="The Assignment Information (by reviewer, no bids) csv formatted file from softconf")
    parser.add_argument("--output_file", type=str, required=True, help="The output file for submission type counts (will be tab separated)")
    
    args = parser.parse_args()
    main(args.submissions_file, args.assignments_file, args.output_file)
        