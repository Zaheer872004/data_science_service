
import re # Regular expressions

class MessageUtil:
  
  
  def isBankSms(self,message):
    words_to_search = ['spent', 'purchase', 'buy', 'payment', 'transaction', 'debit', 'charged','used']
    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in words_to_search) + r')\b'
    return bool(re.search(pattern, message, flags=re.IGNORECASE))
