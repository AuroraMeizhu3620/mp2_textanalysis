import sys
sys.path.insert(0, 'functions/1.text_cleansing')
from text_cleansing import text_cleansing

result = text_cleansing('data/example.txt')
print(result)
