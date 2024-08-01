import pandas as pd
import re
from typing import Dict, List
from transformers import BertTokenizer, BertModel, logging as transformers_logging
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings

from .content_based_orm import SKUMASTER, Session, ICCAT, ICDEPT, TRANSTKD, GOODSMASTER


def load_data():
    data = {}
    try:
        with Session() as session:
            sku_data = pd.DataFrame([s.__dict__ for s in session.query(SKUMASTER).all()])
            iccat_data = pd.DataFrame([i.__dict__ for i in session.query(ICCAT).all()])
            icdept_data = pd.DataFrame([i.__dict__ for i in session.query(ICDEPT).all()])
            transtkd_data = pd.DataFrame([t.__dict__ for t in session.query(TRANSTKD).all()])
            goodmaster_data = pd.DataFrame([g.__dict__ for g in session.query(GOODSMASTER).all()])

        # Drop SQLAlchemy internal columns
        for df in [sku_data, iccat_data, icdept_data, transtkd_data, goodmaster_data]:
            df.drop(columns=['_sa_instance_state'], inplace=True)

        # Merge the dataframes
        merged_df = pd.merge(transtkd_data, goodmaster_data, left_on='TRD_GOODS', right_on='GOODS_KEY')

        # Select and rename the required columns
        trdgood_df = merged_df[['GOODS_KEY', 'GOODS_CODE', 'GOODS_SKU', 'GOODS_ENABLE', 'GOODS_P_ENABLE',
                                'TRD_TRH', 'TRD_SH_NAME', 'TRD_GOODS', 'TRD_KEYIN', 'TRD_NM_PRC', 'TRD_QTY',
                                'TRD_UTQQTY', 'TRD_UTQNAME']]

        # Drop rows where GOODS_ENABLE and GOODS_P_ENABLE are both 'N'
        trdgood_df = trdgood_df[~((trdgood_df['GOODS_ENABLE'] == 'N') | (trdgood_df['GOODS_P_ENABLE'] == 'N'))]

        # Merge with skumaster_df
        merged_sku = pd.merge(trdgood_df, sku_data, left_on='GOODS_SKU', right_on='SKU_KEY')

        # Merge with iccat_df
        iccat_df = iccat_data[['ICCAT_KEY', 'ICCAT_CODE', 'ICCAT_NAME']]
        merged_iccat = pd.merge(merged_sku, iccat_df, left_on='SKU_ICCAT', right_on='ICCAT_KEY')

        # Merge with icdept_df
        icdept_df = icdept_data[['ICDEPT_KEY', 'ICDEPT_CODE', 'ICDEPT_THAIDESC']]
        merged_icdept = pd.merge(merged_iccat, icdept_df, left_on='SKU_ICDEPT', right_on='ICDEPT_KEY')

        Final_data = merged_icdept

        # Display the final dataframe
        print(Final_data.head())

        data = {
            'TRANSTKD': transtkd_data,
            'SKUMASTER': sku_data,
            'ICCAT': iccat_data,
            'ICDEPT': icdept_data,
            'GOODSMASTER': goodmaster_data,
            'FINAL_DATA': Final_data
        }
    except Exception as e:
        print(f"An error occurred while loading data: {e}")

    return data


class ContentBased:
    def __init__(self, data: Dict[str, pd.DataFrame]):
        # Suppress specific warnings
        warnings.filterwarnings("ignore",
                                message="A parameter name that contains `beta` will be renamed internally to `bias`.")
        warnings.filterwarnings("ignore",
                                message="A parameter name that contains `gamma` will be renamed internally to `weight`.")

        # Set transformers library logging level to ERROR
        transformers_logging.set_verbosity_error()

        self.trans_data = data['TRANSTKD']
        self.sku_data = data['FINAL_DATA']
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.model = BertModel.from_pretrained('bert-base-multilingual-cased')
        self.data = self.preprocessing_data()

    def preprocessing_data(self):
        grouped_df = self.sku_data.groupby('SKU_NAME', as_index=False).agg({
            'TRD_QTY': 'sum',
            'GOODS_CODE': 'first',
            'ICCAT_NAME': 'first',
            'ICDEPT_THAIDESC': 'first'
        })

        # Split the ICDEPT_THAIDESC into individual subcategories
        grouped_df['ICDEPT_THAIDESC'] = grouped_df['ICDEPT_THAIDESC'].apply(lambda x: x.split(','))

        # Flatten the DataFrame so each subcategory has its own row
        exploded_df = grouped_df.explode('ICDEPT_THAIDESC').reset_index(drop=True)

        # Create the 'tags' column
        exploded_df['tags'] = exploded_df['SKU_NAME'] + ' ' + exploded_df['ICCAT_NAME'] + ' ' + exploded_df[
            'ICDEPT_THAIDESC']

        # Calculate embeddings for each tag
        exploded_df['embedding'] = exploded_df['tags'].apply(self.get_embedding)

        return exploded_df

    def get_embedding(self, text: str):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()

    def calculate_similarity(self, input_text: str):
        input_embedding = self.get_embedding(input_text)
        cosine_similarities = cosine_similarity(input_embedding, np.vstack(self.data['embedding'].values)).flatten()
        return cosine_similarities

    def recommend(self, user_preference: Dict[str, List[str]], top_n: int = 10) -> List[str]:
        user_input_text = " ".join(user_preference['categories'] + user_preference['subcategories'])
        cosine_similarities = self.calculate_similarity(user_input_text)
        self.data['similarity'] = cosine_similarities

        grouped_recommendations = (self.data
                                   .sort_values(by=['ICCAT_NAME', 'ICDEPT_THAIDESC', 'TRD_QTY', 'similarity'],
                                                ascending=[True, True, False, False])
                                   .groupby(['ICCAT_NAME', 'ICDEPT_THAIDESC'])
                                   .head(top_n))

        recommendations = (grouped_recommendations
                           .sort_values(by=['similarity', 'TRD_QTY'], ascending=False)
                           .head(top_n)
                           .reset_index(drop=True))

        recommendations_list = (
                recommendations['SKU_NAME'] + ' (' + recommendations['ICCAT_NAME'] + ' - ' + recommendations[
            'ICDEPT_THAIDESC'] + ')').tolist()

        return recommendations_list
