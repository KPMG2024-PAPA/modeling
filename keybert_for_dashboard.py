# !pip install keybert
# !pip install kiwipiepy

def keyword_extractor(input: str) -> str:
    
    """
    
    유저가 검색을 위해서 텍스트를 입력하면, 명사 위주로 키워드를 추출하여 키워드+키워드+키워드 형태로 반환합니다.
    
    예시:
    날개가 없는 선풍기를 만들고 있습니다. 다이슨과 같이 날개가 없어 소음이 적게 발생하고 무게가 가벼워집니다. 또한, 전력 소비가 줄어들어 에너지 효율이 높아집니다. 
    위와 같은 문장은 다음과 같이 결과가 나오게 됩니다. 
    날개+선풍기+다이슨+날개+소음+발생+무게+전력+소비+에너지+효율
    
    """

    from keybert import KeyBERT
    from kiwipiepy import Kiwi
    from transformers import BertModel

    text=input

    # text="""
    # 날개가 없는 선풍기를 만들고 있습니다. 다이슨과 같이 날개가 없어 소음이 적게 발생하고 무게가 가벼워집니다. 또한, 전력 소비가 줄어들어 에너지 효율이 높아집니다.
    # """

    # text = """
    # 빠르게 충전되는 2차 전지 제품을 개발하고 있습니다. 이 제품은 자동차용 충전식 배터리로, 72시간 이상 지속될 수 있습니다. 또한 배터리의 크기는 배낭보다도 작습니다.
    # """

    model = BertModel.from_pretrained('skt/kobert-base-v1')
    kw_model = KeyBERT(model)

    kiwi = Kiwi()
    
    def noun_extractor(text):
        results = []
        result = kiwi.analyze(text)
        for token, pos, _, _ in result[0][0]:
            if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
                results.append(token)
        return results
    
    nouns = noun_extractor(text)
    nouns
    
    nouns_text = ' '.join(nouns)
    
    stop_words = [
    "발명", "발명품", "제품", "제품을", "상품", "상품을",
    "것", "이것", "저것",
    "우리", "너", "당신",
    "그리고", "하지만", "그러나",
    "있다", "없다",
    "되다", "하다",
    "사용", "사용하는",
    "가능", "가능한",
    "통해", "을 통해",
    "대한", "에 대한",
    "이러한", "저러한",
    "때문에", "때문",
    "구성", "구성된",
    "기술", "기술적",
    "결과", "결과적",
    "이용", "이용한",
    "제공", "제공하는",
    "시스템", "시스템을",
    "다양한", "여러",
    "관련", "관련된",
    "문제", "문제를",
    "해결", "해결하기",
    "목적", "목적으로",
    "이유", "이유로",
    "사례", "사례를",
    "방법", "방법으로",
    "이후", "이후에"
    
    ]
    
    keywords = kw_model.extract_keywords(nouns_text, keyphrase_ngram_range=(1, 1), stop_words=stop_words, top_n=10)
    
    result_keywords = "+".join([keyword[0] for keyword in keywords])
    
    return result_keywords
    