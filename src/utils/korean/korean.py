def is_only_cho(words: str) -> bool:
    chos = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 
            'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 
            'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ']
    result = True
    for character in words:
        result = result & (character in chos)

    return result