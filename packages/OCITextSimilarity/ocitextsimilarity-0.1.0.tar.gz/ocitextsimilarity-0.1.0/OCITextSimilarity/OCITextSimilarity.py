from langchain_community.embeddings.oci_generative_ai import OCIGenAIEmbeddings

class OCITextSimilarity:
    def __init__(self, embed_model_id, oci_endpoint, oci_compartment_id, oci_auth_profile):
        self.embed_model_id = embed_model_id
        self.oci_endpoint = oci_endpoint
        self.oci_compartment_id = oci_compartment_id
        self.oci_auth_profile = oci_auth_profile

    
    def generate_embeddings(self, input_text):
        embeddings_doc = OCIGenAIEmbeddings(
            model_id = self.embed_model_id,
            service_endpoint=self.oci_endpoint,
            model_kwargs= {"input_type": "SEARCH_DOCUMENT"},
            compartment_id= self.oci_compartment_id,
            auth_profile=self.oci_auth_profile
        )
        return embeddings_doc.embed_query(input_text)
    
    @staticmethod
    def straight_cosine_similarity(A, B):
        dot_product = sum(a*b for a,b in zip(A,B))
        magnitude_A = sum(a*a for a in A) ** 0.5
        magnitude_B = sum(b*b for b in B) ** 0.5
        cosine_similarity = dot_product / (magnitude_A * magnitude_B)
        return cosine_similarity
    
    def text_similarity(self, text1, text2):
        vec_1 = self.generate_embeddings(text1)
        vec_2 = self.generate_embeddings(text2)
        return self.straight_cosine_similarity(vec_1, vec_2)