import pandas as pd
import numpy as np
def merge_bell_shaped_with_spacers_pandas(original_chunks, bell_shaped_chunks):
    # Divide the last chunk for spacing
    divided_spacer = np.array_split(original_chunks[-1], len(bell_shaped_chunks))
    
    final_chunks = pd.Series(dtype=object)  # Initialize an empty Series to hold the final chunks
    for i, bell_chunk in enumerate(bell_shaped_chunks):
        # Append the bell-shaped chunk
        final_chunks = final_chunks.append(bell_chunk)
        
        # Check if there's a corresponding spacer
        if i < len(divided_spacer):
            # Append the spacer, converting to Series to ensure index preservation
            final_chunks = final_chunks.append(pd.Series(divided_spacer[i]))
    
    return final_chunks