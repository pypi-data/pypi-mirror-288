class Num2Devanagari:
    def __init__(self):
        self.one_to_hundred = ["शुन्य", "एक", "दुई", "तीन", "चार", "पाँच", "छ", "सात", "आठ", "नौ", "दस", "एघार", "बाह्र", "तेह्र", "चौध", "पन्ध्र", "सोह्र", "सत्र", "अठार", "उन्नाइस", "बीस", "एक्काइस", "बाइस", "तेइस", "चौबीस", "पच्चिस", "छब्बीस", "सत्ताइस", "अठ्ठाइस", "उनन्तीस", "तीस", "एकत्तिस", "बत्तिस", "तेत्तिस", "चौँतिस", "पैँतिस", "छत्तिस", "सट्तीस", "अठतीस", "उनन्चालीस", "चालीस", "एकचालीस", "बयालिस", "त्रिचालीस", "चौवालिस", "पैंतालिस", "छयालिस", "सट्चालीस", "अट्चालीस", "उनन्चास", "पचास", "एकाउन्न", "बाउन्न", "त्रिपन्न", "चौवन्न", "पच्पन्न", "छपन्न", "सन्ताउन्न", "अन्ठाउँन्न", "उनान्न्साठी ", "साठी", "एकसट्ठी", "बैसट्ठी", "त्रिसट्ठी", "चौंसट्ठी", "पैंसट्ठी", "छैसट्ठी", "सतसट्ठी", "अठसट्ठी", "उनन्सत्तरी", "सत्तरी", "एकहत्तर", "बहत्तर", "त्रिहत्तर", "चौहत्तर", "पचहत्तर", "छहत्तर", "सतहत्तर", "अठ्हत्तर", "उनास्सी", "अस्सी", "एकासी", "बयासी", "त्रीयासी", "चौरासी", "पचासी", "छयासी", "सतासी", "अठासी", "उनान्नब्बे", "नब्बे", "एकान्नब्बे", "बयान्नब्बे", "त्रियान्नब्बे", "चौरान्नब्बे", "पंचान्नब्बे", "छयान्नब्बे", "सन्तान्‍नब्बे", "अन्ठान्नब्बे", "उनान्सय"]
        self.place_values = ['हजार', 'लाख', 'करोड', 'अर्ब', 'अर्ब', 'नील', 'पद्म', 'शंख']
    # '123456789' -> 12, 34, 56, 789
    def seperate(self, input_number):
        # e.g. 123456789 -> ['789', '56', '34', '12']
        input_number = str(input_number)
        seperated = []
        initial = True

        while(input_number):
            if initial:
                seperated.append(input_number[-3:])
                input_number=input_number[:-3] 
                initial = False
            else:
                seperated.append(input_number[-2:])
                input_number=input_number[:-2]
        return seperated   # ['789', '56', '34', '12']

    def three_digits_to_word(self, digits):
        '''
        Can handle up to 3 digits
        e.g. 
            digit = 957
            <returns> words = ['नौ', 'सय', 'सन्ताउन्न']
        '''
        words = []
        if len(digits) == 3:
            if int(digits[0]) != 0:
                words.append(self.one_to_hundred[int(digits[0])])
                words.append('सय')
            
            if int(digits[1:]) !=0:
                
                words.append(self.one_to_hundred[int(digits[1:])])
        else:
            words.append(self.one_to_hundred[int(digits)])
        return words

    '''
    # Test

    digits_to_test = [0,1,9,10,11,99,100,957]
    for digit in digits_to_test:
        digit = str(digit)
        print(three_digits_to_word(digit))

    ['शुन्य']
    ['एक']
    ['नौ']
    ['दस']
    ['एघार']
    ['उनान्सय']
    ['एक', 'सय']
    ['नौ', 'सय', 'सन्ताउन्न']

    '''

    def words_matrix_to_str(self, words):
        '''
        e.g.
        words = [
            ['बाह्र', 'करोड'],
            ['चौँतिस', 'लाख'],
            ['छपन्न', 'हजार'],
            ['सात', 'सय', 'उनान्नब्बे']
        ]
        '''
        str_value = ''
        for row in words:
            str_value += ' '.join(row) + ' '
        return str_value.strip()

    def convert(self, input_number):
        # e.g. input_number = 123456789
        seperated = self.seperate(input_number)
        # e.g. seperated = ['789', '56', '34', '12']
        
        words = []
        for i,sep in enumerate(seperated):
            if i-1 < 0:
                # e.g. i=0, sep='789'
                # Do not add place value
                words.append(self.three_digits_to_word(sep))
                
            else:
                # e.g. i=1, val=56
                # Add place value
                words.append(self.three_digits_to_word(sep) + [self.place_values[i-1]])
        '''
        words = [['सात', 'सय', 'उनान्नब्बे'],
                ['छपन्न', 'हजार'],
                ['चौँतिस', 'लाख'],
                ['बाह्र', 'करोड']]
        '''
        
        words = words[::-1]
        '''
        words = [
            ['बाह्र', 'करोड'],
            ['चौँतिस', 'लाख'],
            ['छपन्न', 'हजार'],
            ['सात', 'सय', 'उनान्नब्बे']
        ]
        '''
        return self.words_matrix_to_str(words)
    

if __name__ == "__main__":
    num2word = Num2Devanagari()
    # from nepali_number_dataset_generator import digits_to_word
    numbers = [0, 1, 3, 9, 10, 11, 99, 100, 101, 149, 150, 151, 199, 200, 201, 999, 1000, 1001, 1999, 2000, 2001, 9999, 10000, 10001, 123456789]
    for num in numbers:
        print(f'{num} -> {num2word.convert(num)}')