from parameters import MARKET, PRODUCTS
# insert {MARKET}; {PRODUCTS}

system_prompt = f"You are a helpful assistant with in-depth knowledge of the {MARKET} and related manufacturing processes. Please help me to conduct a market analysis for the {MARKET} relevant to a company that develops and supplies {PRODUCTS}. Please answer briefly and concisely. If possible, use bullet points only."

user_prompts = [
    "1: Name all the steps in semiconductor manufacturing, numbered, and state whether they are the “Back End of Line” (BEOL) or the “Front End of Line” (FEOL). 2: In which of these steps are X-rays used and why - 2.a) today and 2.b) possibly in the future",
    f"Which companies supply the semiconductor manufacturers with {PRODUCTS}, and which companies supply the OEMs active in the {MARKET} with {PRODUCTS}? Which are the 5 largest semiconductor manufacturers?",
    "Which inspection technologies other than X-ray are used in which steps of semiconductor manufacturing? For each of these processes: Why not X-ray? What are the disadvantages of the current non-X-ray method and what would be the advantages of using X-rays instead?",
    "Tell me more about X-ray lithography XRL, X-ray diffraction XRD and X-ray fluorescence XRF. What are the opportunities, requirements and challenges (technical and economical)?",
    f"What else could be of interest with regard to the {MARKET} for a company that develops and sells {PRODUCTS}?",
    f"What are the trends and market potential of X-ray inspection in the {MARKET}? What are the hurdles to entering the {MARKET} when offering {PRODUCTS}?",
    f"Conduct a {MARKET} analysis, relevant to a company that develops and offers {PRODUCTS}, with all the steps that usually go with it.",
    "Who are you and which role are you playing?",
]

