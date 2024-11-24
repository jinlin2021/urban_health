from sklearn.metrics.pairwise import cosine_similarity


""" def calculate_similarity(similarity_df, community_id_1, community_id_2):
    
    result = similarity_df[
        ((similarity_df['from'] == community_id_1) & (similarity_df['to'] == community_id_2)) |
        ((similarity_df['from'] == community_id_2) & (similarity_df['to'] == community_id_1))
    ]
    
    if not result.empty:
        similarity_value = result.iloc[0]['cosine_similarity']
        return similarity_value
    else:
        return None 

 """

import pandas as pd

def calculate_similarity(similarity_df, community_id_1, community_id_2):
    """根据社区ID查找相似度，并返回最相似和最不相似的社区ID和相似度"""
    def get_similarity(df, community_id):
        similarities = df[(df['from'] == community_id) | (df['to'] == community_id)]
        similarities = similarities[(similarities['from'] != similarities['to'])]
        if similarities.empty:
            return None, None
        similarities['target'] = similarities.apply(lambda row: row['to'] if row['from'] == community_id else row['from'], axis=1)
        most_similar = similarities.loc[similarities['cosine_similarity'].idxmax()]
        least_similar = similarities.loc[similarities['cosine_similarity'].idxmin()]
        return {'id': most_similar['target'], 'similarity': most_similar['cosine_similarity']}, {'id': least_similar['target'], 'similarity': least_similar['cosine_similarity']}
    
    result = similarity_df[
        ((similarity_df['from'] == community_id_1) & (similarity_df['to'] == community_id_2)) |
        ((similarity_df['from'] == community_id_2) & (similarity_df['to'] == community_id_1))
    ]
    similarity_value = result.iloc[0]['cosine_similarity'] if not result.empty else None

    most_similar_1, least_similar_1 = get_similarity(similarity_df, community_id_1)
    most_similar_2, least_similar_2 = get_similarity(similarity_df, community_id_2)

    return {
        'similarity_value': similarity_value,
        'most_similar_1': most_similar_1,
        'least_similar_1': least_similar_1,
        'most_similar_2': most_similar_2,
        'least_similar_2': least_similar_2
    }