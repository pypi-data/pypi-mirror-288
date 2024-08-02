import argparse
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from .exclude_and_assign_above_threshold import exclude_and_assign_above_threshold
from .sort_and_divide_series_into_n_chunks import sort_and_divide_series_into_n_chunks
from .optimize_chunks_for_normality_pandas import optimize_chunks_for_normality_pandas
from .sort_and_merge_series import sort_and_merge_series
from .merge_bell_shaped_with_spacers_pandas import merge_bell_shaped_with_spacers_pandas

'''
def main():

    parser = argparse.ArgumentParser(description='Run PN_DTW_FE analysis.')
    parser.add_argument('--input', type=str, required=True, help='Input CSV file')
    parser.add_argument('--geneOFinterest', type=str, required=True, help='Gene of Interest')
    parser.add_argument('--threshold', type=int, required=True, help='Threshold value')
    parser.add_argument('--desired_chunks', type=int, required=True, help='Number of desired chunks')
    parser.add_argument('--seed', type=str, required=True, help='Seed values (range or single value)')
    
    args = parser.parse_args()
'''
def PNdtwFE(input_file, geneOFinterest, threshold, desired_chunks, seed=42):
    df35 = pd.read_csv(input_file, sep='\t')
    df35.set_index(df35.columns[0], inplace=True)

    GeneOfInterest = geneOFinterest
    GeneOfInterest_expression = df35.loc[GeneOfInterest]

    threshold = threshold
    desired_chunks = desired_chunks

    below_threshold, above_threshold = exclude_and_assign_above_threshold(GeneOfInterest_expression[1:], threshold)
    total_chunks = desired_chunks + 1
    chunks = sort_and_divide_series_into_n_chunks(below_threshold, total_chunks)

    # Handle seed range
    seed_values = []
    if ':' in seed:
        start, end = map(int, seed.split(':'))
        seed_values = range(start, end+1)
    else:
        seed_values = [int(seed)]

    for seed in seed_values:
        optimized_chunks, best_score = optimize_chunks_for_normality_pandas(chunks[0:desired_chunks], desired_chunks, seed=seed, random=42)
        new_chunks_series = [chunk[GeneOfInterest] for chunk in optimized_chunks]
        bell_shaped_chunks = [sort_and_merge_series(chunk) for chunk in new_chunks_series]
        final_chunks_with_spacers = merge_bell_shaped_with_spacers_pandas(chunks, bell_shaped_chunks)
        final_chunks_with_spacers_series = pd.concat([above_threshold, final_chunks_with_spacers])
        sorted_row_indices = final_chunks_with_spacers_series.index.tolist()
        df_35 = df35[sorted_row_indices]

        tor1_ = df_35.loc[GeneOfInterest]
        
        df_sorted = df_35
        print(df_sorted.shape)
        '''
        df = pd.read_csv(args.input, sep='\t')
        df.set_index(df.columns[0], inplace=True)
        df_sorted['gene_name'] = df_sorted.index.map(df['gene_name'])
        cols = ['gene_name'] + [col for col in df_sorted.columns if col != 'gene_name']
        df_sorted = df_sorted.reindex(columns=cols)
        '''

        df_sorted = df_sorted.reset_index()
        tor1_expression = df_sorted[df_sorted['attribution'] == GeneOfInterest].iloc[:, 1:].values.flatten()

        gene_expressions = []
        for index, row in df_sorted.iterrows():
            gene_expressions.append(row)

        pattern_similarities = {}
        paths = {}
        #for i, gene_expression in enumerate(gene_expressions, start=1):
        #    distance, path = fastdtw(tor1_expression, gene_expression[1:], dist=euclidean)
        #    pattern_similarities[f'{gene_expression[0]}'] = distance

        for i, gene_expression in enumerate(gene_expressions, start=1):
            #print(np.array(gene_expression.iloc[1:].values))
            #print(gene_expression)
            #print(tor1_expression)
            #print(len(tor1_expression))
            #print('\n')
            if tor1_expression.ndim != 1 or gene_expression.ndim != 1:
                print(f"Error: One of the input arrays is not 1-D.")
                continue
            distance, path = fastdtw(np.array(tor1_expression).flatten(), np.array(gene_expression.iloc[1:].values).flatten(), dist=euclidean)
            gene_name = gene_expression[0]  # Assuming the gene ID is in the first column
            #gene_name = gene_id
            
            pattern_similarities[gene_name] = distance
            paths[gene_name] = path  # Storing path

        # Sorting genes by their DTW distance to tor1_expression (lower distance means more similar)
        sorted_distances = dict(sorted(pattern_similarities.items(), key=lambda item: item[1]))

        # Creating list of dictionaries for DataFrame
        data_rows = [{'gene_name': gene_name, 'distance': sorted_distances[gene_name], 'path': paths[gene_name]} 
                     for gene_name in sorted_distances]

        #sorted_pattern_similarities = dict(sorted(pattern_similarities.items(), key=lambda item: item[1]))
        #data_rows = [{'Ptr': key, 'distance': value} for key, value in sorted_pattern_similarities.items()]
        #data_rows = [{'gene_name': gene_name, 'distance': sorted_pattern_similarities[gene_name], 'path': paths[gene_name]} 
        #     for gene_name in sorted_pattern_similarities]
        df_similarities = pd.DataFrame(data_rows)
        output_filename = f"Genes_ranking_with_seed_{seed}_DTW.txt"
        df_similarities.to_csv(output_filename, sep="\t", index=False)
        print(f"Analysis completed for seed {seed}. Output saved to {output_filename}.")

def main():
    parser = argparse.ArgumentParser(description='Run PN_DTW_FE analysis.')
    parser.add_argument('--input', type=str, required=True, help='Input CSV file')
    parser.add_argument('--geneOFinterest', type=str, required=True, help='Gene of Interest')
    parser.add_argument('--threshold', type=int, required=True, help='Threshold value')
    parser.add_argument('--desired_chunks', type=int, required=True, help='Number of desired chunks')
    parser.add_argument('--seed', type=str, required=True, help='Seed values (range or single value)')
    
    args = parser.parse_args()
    PNdtwFE(args.input, args.geneOFinterest, args.threshold, args.desired_chunks, args.seed)

if __name__ == "__main__":
    main()