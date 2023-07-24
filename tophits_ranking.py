import numpy as np
import scipy.sparse as sp
import pandas as pd
import tensorly as tl
from tensorly.decomposition import tucker

# Function to create a sparse tensor from the Twitter dataset
def create_sparse_tensor(data):
    # Filter rows with 'type' column value as 'twitter'
    data = data[data['type'] == 'twitter']

    # Extract unique users/channels from the dataset
    users_channels = data['link'].apply(lambda x: x.split('/')[-1])
    users_channels = users_channels.unique()

    # Create a dictionary to map users/channels to unique IDs
    user_channel_to_id = {user_channel: idx for idx, user_channel in enumerate(users_channels)}

    # Create an empty sparse tensor
    tensor_shape = (len(user_channel_to_id), len(user_channel_to_id))
    tensor = sp.dok_matrix(tensor_shape, dtype=np.int32)

    # Fill the sparse tensor based on mentions in the dataset
    for _, row in data.iterrows():
        source_user_channel = row['link'].split('/')[-1]
        mentioned_users_channels = row['text'].split()  # Extract mentions from the 'text' column

        for mentioned_user_channel in mentioned_users_channels:
            if mentioned_user_channel.startswith('@'):
                mentioned_user_channel = mentioned_user_channel[1:]  # Remove the '@' symbol
                if mentioned_user_channel in user_channel_to_id:
                    tensor[user_channel_to_id[source_user_channel], user_channel_to_id[mentioned_user_channel]] += 1

    return tensor, user_channel_to_id

# Function to perform Tucker decomposition on the tensor
def tucker_decomposition(tensor, ranks):
    # Convert the sparse tensor to a dense tensor
    tensor_dense = tensor.toarray()

    # Perform Tucker decomposition
    decomposed_tensor = tucker(tensor_dense, ranks)

    return decomposed_tensor

# Function to calculate TOPHITS scores
def calculate_tophits_scores(tensor, ranks, user_channel_to_id):
    # Perform Tucker decomposition
    decomposed_tensor = tucker_decomposition(tensor, ranks)

    # Obtain the factor matrices from the decomposed tensor
    factor_matrices = decomposed_tensor[1]  # Update index to access the factor matrices

    # Perform calculations to obtain authority and hub scores
    authorities = np.sum(factor_matrices[0], axis=0)  # Sum along axis 0 (users/channels)
    hubs = np.sum(factor_matrices[1], axis=0)  # Sum along axis 0 (users/channels)

    return authorities, hubs

# Load the Twitter dataset (replace 'Crypto_twitter_full.csv' with your dataset file path)
data = pd.read_csv('Crypto_twitter_full.csv', encoding='latin-1', dtype={'text': str})

# Create a sparse tensor from the Twitter dataset and obtain user/channel mappings
tensor, user_channel_to_id = create_sparse_tensor(data)

# Set the ranks for Tucker decomposition
ranks = [73, 10]  # Update with appropriate ranks based on your data, the first value should match the number of unique channels


# Calculate TOPHITS scores
authorities, hubs = calculate_tophits_scores(tensor, ranks, user_channel_to_id)

# Map channel IDs back to channel names
channels = data['link'].apply(lambda x: x.split('/')[-1]).unique()

# Remove the last two channels to match the number of authorities
if len(authorities) < len(channels):
    channels = channels[:-2]

# Ensure the size of 'authorities' is consistent with the number of unique channels
if len(authorities) != len(channels):
    print("Error: The number of authorities does not match the number of unique channels.")
    print(f"Number of authorities: {len(authorities)}")
    print(f"Number of unique channels: {len(channels)}")
    exit()

# Sort the channels based on authority scores to get the ranked channels
ranked_channels = [channel for channel, _ in sorted(user_channel_to_id.items(), key=lambda x: authorities[x[1]], reverse=True)]

# Print the number of occurrences of each channel in the dataset
channel_counts = data['link'].apply(lambda x: x.split('/')[-1]).value_counts()
print("Number of occurrences of each channel:")
print(channel_counts)

# Print the ranked channels
print("Ranked Channels:")
for rank, channel in enumerate(ranked_channels, start=1):
    print(f"Rank {rank}: {channel}")

# Save the ranked channels to a CSV file
ranked_channels_df = pd.DataFrame({'Ranked Channels': ranked_channels})
ranked_channels_df.to_csv('Ranked_Channels.csv', index=False)