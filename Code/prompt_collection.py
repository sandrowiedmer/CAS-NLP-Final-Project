from parameters import MARKET, PRODUCTS

system_prompt = f"You are a helpful assistant with deep knowledge about the {MARKET} and corresponding manufacturing processes. Please help me do a market analysis for the {MARKET}, relevant for a company developing and offering {PRODUCTS}. Please answer in max. 100 words, with not to much stop words and no fillers. As much as possible only in bullet points."



#prompts list, ev. generic vs market specific prompts


user_prompts_full_set = [
    f"1: List all the steps of semiconductor manufacturing, with indication if it is back end BEOL or front end FEOL. 2: in which of these steps X-rays are used and why - 2.a) today and 2.b) potentially in the future",
    f"Which companies are serving the semiconductor manufacturers with {PRODUCTS}, and which companies are serving the OEMS active in {MARKET}?",
    f"Which other inspection technologies beside X-ray are used and at which steps of semiconductor manufacturing? For each of them: Why not X-ray: What are the pains of the current non-X-ray method and which advantages would using X-rays instead have?",
    f"Tell me more about X-ray lithography XRL, X-ray diffraction XRD and X-ray fluorescence XRF.",
    f"What else regarding the {MARKET} could be of interest for a company developing and selling {PRODUCTS}?",
    f"Tell me about trends, relevant for us, what is the market potential of X-ray inspection in {MARKET}? What are the hurdles for entering the {MARKET}",
    f"Who are you and which role are you playing?",
]

#4. Which companies active in the semiconductor market are buying X-ray sources, today and potentially in the future? Please give for each if it is a semiconductor manufacturer itself or an OEM serving the semiconductor manufacturer.


# user_prompts = full_set indices, or:
user_prompts = [
    f"Tell me about trends, relevant for us, what is the market potential of X-ray inspection in {MARKET}? What are the hurdles for entering the {MARKET}",
]

#new: front end FEOL and back end BEOL

# Zero Shot

# Few Shot

#ReAct



#CoT